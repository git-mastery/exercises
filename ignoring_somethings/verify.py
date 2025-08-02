import tempfile
from pathlib import Path
from typing import List

from git import Repo
from git_autograder import (
    GitAutograderExercise,
    GitAutograderOutput,
    GitAutograderStatus,
)

MISSING_COMMITS = "You have not made any commits yet!"
STILL_IGNORING_FILE_22 = "You are still ignoring many/file22.txt."
STILL_HIDING = (
    "You are still ignoring why_am_i_hidden.txt. Find where the file is and fix that."
)
NOT_IGNORING_IGNORE_ME = "You are not ignoring ignore_me.txt"
NOT_IGNORING_RUNAWAY = (
    "You are not ignoring runaway.txt. Find where the file is and fix that."
)
NOT_PATTERN_MATCHING_RUNAWAY = (
    "You should be using ** to match all subfolders to ignore runaway.txt."
)
MISSING_GITIGNORE = "You are missing the .gitignore file! Try to reset the exercise using gitmastery progress reset"


def verify(exercise: GitAutograderExercise) -> GitAutograderOutput:
    main_branch = exercise.repo.branches.branch("main")

    if len(main_branch.user_commits) == 0:
        raise exercise.wrong_answer([MISSING_COMMITS])

    with main_branch.latest_commit.file(".gitignore") as gitignore_file:
        if gitignore_file is None:
            raise exercise.wrong_answer([MISSING_GITIGNORE])
        gitignore_file_contents = gitignore_file

    # Verify the state of the ignore by recreating the necessary files and checking if
    # Git ignores them directly in a separate temporary Git repository
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        (tmp_path / ".gitignore").write_text(gitignore_file_contents)

        simulated_files = [
            "many/file22.txt",
            "why_am_i_hidden.txt",
            "ignore_me.txt",
            "this/is/very/nested/runaway.txt",
        ]
        for file in simulated_files:
            (tmp_path / file).parent.mkdir(parents=True, exist_ok=True)
            (tmp_path / file).touch()

        test_repo: Repo = Repo.init(tmp_path)
        ignored = {f for f in simulated_files if test_repo.ignored(f)}

        comments: List[str] = []
        if "many/file22.txt" in ignored:
            comments.append(STILL_IGNORING_FILE_22)

        if "why_am_i_hidden.txt" in ignored:
            comments.append(STILL_HIDING)

        if "ignore_me.txt" not in ignored:
            comments.append(NOT_IGNORING_IGNORE_ME)

        if "this/is/very/nested/runaway.txt" not in ignored:
            comments.append(NOT_IGNORING_RUNAWAY)
        elif "this/**/runaway.txt" not in gitignore_file_contents.splitlines():
            comments.append(NOT_PATTERN_MATCHING_RUNAWAY)

        if comments:
            raise exercise.wrong_answer(comments)

        return exercise.to_output(
            ["Great work using .gitignore!"], status=GitAutograderStatus.SUCCESSFUL
        )
