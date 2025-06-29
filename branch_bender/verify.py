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
NO_MERGES = "You need to start merging the feature branches."
WRONG_MERGE_ORDER = "You should have merged {branch_name} first. The expected order is feature/login, then feature/dashboard, and last feature/payments"
FEATURE_LOGIN_MERGE_MISSING = "You should have merged feature/login first."
FEATURE_DASHBOARD_MERGE_MISSING = "You should have merged feature/dashboard next."
FEATURE_PAYMENTS_MERGE_MISSING = "You should have merged feature/payments last."
RESET_MESSAGE = 'Reset the repository using "gitmastery progress reset" and start again'


def verify(exercise: GitAutograderExercise) -> GitAutograderOutput:
    main_branch = exercise.repo.branches.branch("main")
    if exercise.repo.repo.is_dirty():
        raise exercise.wrong_answer([UNCOMMITTED_CHANGES])

    try:
        if exercise.repo.repo.active_branch.name != "main":
            raise exercise.wrong_answer([NOT_ON_MAIN])
    except TypeError:
        raise exercise.wrong_answer([DETACHED_HEAD])

    main_reflog = main_branch.reflog
    merge_logs = [entry for entry in main_reflog if entry.action.startswith("merge")]
    merge_order = [entry.action[len("merge ") :] for entry in merge_logs][::-1]
    if len(merge_order) == 0:
        raise exercise.wrong_answer([NO_MERGES])

    if merge_order[0] != "feature/login":
        raise exercise.wrong_answer([FEATURE_LOGIN_MERGE_MISSING, RESET_MESSAGE])

    if merge_order[1] != "feature/dashboard":
        raise exercise.wrong_answer([FEATURE_DASHBOARD_MERGE_MISSING, RESET_MESSAGE])

    if merge_order[2] != "feature/payments":
        raise exercise.wrong_answer([FEATURE_PAYMENTS_MERGE_MISSING, RESET_MESSAGE])

    return exercise.to_output(
        [
            "Great work with merging the branches in order! Try running the HTML files locally!"
        ],
        GitAutograderStatus.SUCCESSFUL,
    )
