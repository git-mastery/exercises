from git_autograder import (
    GitAutograderExercise,
    GitAutograderInvalidStateException,
    GitAutograderOutput,
    GitAutograderStatus,
    GitAutograderWrongAnswerException,
)

UNCOMMITTED_CHANGES = "You still have uncommitted changes. Commit them first on the appropriate branch first!"
NOT_ON_MAIN = (
    "You aren't currently on the main branch. Checkout to that branch and try again!"
)
DETACHED_HEAD = "You should not be in a detached HEAD state! Use git checkout main to get back to main"
MISSING_MERGES = "You are missing some merges"
WRONG_MERGE_ORDER = "You should have merged {branch_name} first. The expected order is feature/login, feature/dashboard, feature/payments"


def verify(exercise: GitAutograderExercise) -> GitAutograderOutput:
    main_branch = exercise.repo.branches.branch("main")
    if exercise.repo.repo.is_dirty():
        raise exercise.wrong_answer([UNCOMMITTED_CHANGES])

    try:
        if exercise.repo.repo.active_branch.name != "main":
            raise exercise.wrong_answer([NOT_ON_MAIN])
    except TypeError:
        raise exercise.wrong_answer([DETACHED_HEAD])

    try:
        # Merge commits exhibit the behavior of having 2 parents (from/to)
        main_reflog = main_branch.reflog[::-1]
        expected_order = ["feature/payments", "feature/dashboard", "feature/login"][
            ::-1
        ]
        i = 0
        for entry in main_reflog:
            if not entry.action.startswith("merge") or i >= len(expected_order):
                continue
            merged_branch = entry.action[len("merge ") :]
            if merged_branch != expected_order[i]:
                raise exercise.wrong_answer(
                    [WRONG_MERGE_ORDER.format(branch_name=expected_order[i])]
                )
            else:
                i += 1

        if i < len(expected_order):
            raise exercise.wrong_answer([MISSING_MERGES])

        return exercise.to_output(
            ["Great work with using git merge fix the bugs!"],
            GitAutograderStatus.SUCCESSFUL,
        )
    except (GitAutograderWrongAnswerException, GitAutograderInvalidStateException):
        raise
    except Exception:
        raise exercise.wrong_answer(["Something bad happened"])
    finally:
        main_branch.checkout()
