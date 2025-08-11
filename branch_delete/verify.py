from git_autograder import (
    GitAutograderExercise,
    GitAutograderOutput,
    GitAutograderStatus,
)

FIX_SCROLLING_BUG_EXISTS = (
    "Branch 'fix-scrolling-bug' still exists! Remember to delete it"
)
IMPROVE_LOADING_EXISTS = "Branch 'improve-loading' still exists! Remember to delete it"
IMPROVE_LOADING_MERGED = (
    "Branch 'improve-loading' was merged into 'main', but it shouldn't be"
)
PROGRESS_RESET = "Reset your progress using 'gitmastery progress reset' to try again!"


def verify(exercise: GitAutograderExercise) -> GitAutograderOutput:
    if exercise.repo.branches.has_branch("fix-scrolling-bug"):
        raise exercise.wrong_answer([FIX_SCROLLING_BUG_EXISTS])

    if exercise.repo.branches.has_branch("improve-loading"):
        raise exercise.wrong_answer([IMPROVE_LOADING_EXISTS])

    main_reflog = exercise.repo.branches.branch("main").reflog
    merge_logs = [entry for entry in main_reflog if entry.action.startswith("merge")]
    merge_order = [entry.action[len("merge ") :] for entry in merge_logs][::-1]
    for merge in merge_order:
        if merge == "improve-loading":
            raise exercise.wrong_answer([IMPROVE_LOADING_MERGED])

    return exercise.to_output(
        ["Great job using git branch to delete both merged and unmerged branches!"],
        GitAutograderStatus.SUCCESSFUL,
    )
