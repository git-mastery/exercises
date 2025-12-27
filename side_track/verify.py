import io
import os
import sys
from contextlib import redirect_stdout
from pathlib import Path
from typing import Any, Dict, Optional, cast

from git_autograder import (
    GitAutograderExercise,
    GitAutograderInvalidStateException,
    GitAutograderOutput,
    GitAutograderRepo,
    GitAutograderStatus,
    GitAutograderWrongAnswerException,
)

MISSING_BUG_FIX_BRANCH = "You are missing the bug-fix branch"
MISSING_COMMITS = "You do not have 2 commits on the bug-fix branch"
UNCOMMITTED_CHANGES = "You still have uncommitted changes. Commit them first on the appropriate branch first!"
NOT_ON_MAIN = (
    "You aren't currently on the main branch. Checkout to that branch and try again!"
)
DETACHED_HEAD = "You should not be in a detached HEAD state! Run git checkout main to get back to main"
GREET_NOT_FIXED = "You have not fixed the greet function in greet.py"
CALCULATOR_NOT_FIXED = "You have not fixed the add function in calculator.py"


def execute_function(
    filepath: str | Path, func_name: str, args: Dict[str, Any]
) -> Optional[Any]:
    with open(filepath, "r") as f:
        sys.dont_write_bytecode = True
        code = f.read()
        namespace: Dict = {}
        exec(code, namespace)
        result = namespace[func_name](**args)
        sys.dont_write_bytecode = False
        return result


def verify(exercise: GitAutograderExercise) -> GitAutograderOutput:
    main_branch = exercise.repo.branches.branch("main")
    if exercise.repo.repo.is_dirty():
        raise exercise.wrong_answer([UNCOMMITTED_CHANGES])

    try:
        if exercise.repo.repo.active_branch.name != "main":
            raise exercise.wrong_answer([NOT_ON_MAIN])
    except TypeError:
        raise exercise.wrong_answer([DETACHED_HEAD])

    if not exercise.repo.branches.has_branch("bug-fix"):
        raise exercise.wrong_answer([MISSING_BUG_FIX_BRANCH])

    try:
        bug_fix_branch = exercise.repo.branches.branch("bug-fix")
        bug_fix_branch.checkout()
        if len(bug_fix_branch.user_commits) < 2:
            raise exercise.wrong_answer([MISSING_COMMITS])

        repo_path: str | os.PathLike = cast(GitAutograderRepo, exercise.repo).repo_path
        # Ensure that they applied the right fix by testing the greet function
        fixed_greet = True
        for name in ["James", "Hi", "Alice", "Bob"]:
            buf = io.StringIO()
            with redirect_stdout(buf):
                execute_function(Path(repo_path) / "greet.py", "greet", {"name": name})
            print(buf.getvalue().strip())
            if buf.getvalue().strip() != f"Hi {name}":
                fixed_greet = False
                break

        fixed_calculator = True
        for a, b in zip([1, 2, 3, 4, 5], [11, 123, 9, 10, 1]):
            result = execute_function(
                Path(repo_path) / "calculator.py", "add", {"a": a, "b": b}
            )
            if result is None:
                fixed_calculator = False
                break
            if result != a + b:
                fixed_calculator = False
                break

        comments = []
        if not fixed_greet:
            comments.append(GREET_NOT_FIXED)
        if not fixed_calculator:
            comments.append(CALCULATOR_NOT_FIXED)

        if comments:
            raise exercise.wrong_answer(comments)

        return exercise.to_output(
            ["Great work with using git branch and git checkout to fix the bugs!"],
            GitAutograderStatus.SUCCESSFUL,
        )
    except (GitAutograderWrongAnswerException, GitAutograderInvalidStateException):
        raise
    except Exception:
        raise exercise.wrong_answer(["Something bad happened"])
    finally:
        main_branch.checkout()
