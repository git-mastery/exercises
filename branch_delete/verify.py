from git_autograder import (
    GitAutograderExercise,
    GitAutograderOutput,
    GitAutograderStatus,
)

OPTIMIZATION_APPROACH_1_EXISTS = (
    "Branch 'optimization-approach-1' still exists! Remember to delete it"
)
OPTIMIZATION_APPROACH_2_EXISTS = (
    "Branch 'optimization-approach-2' still exists! Remember to delete it"
)
OPTIMIZATION_APPROACH_2_MERGED = (
    "Branch 'optimization-approach-2' was merged into 'main', but it shouldn't be"
)
PROGRESS_RESET = "Reset your progress using 'gitmastery progress reset' to try again!"


def verify(exercise: GitAutograderExercise) -> GitAutograderOutput:
    if exercise.repo.branches.has_branch("optimization-approach-1"):
        raise exercise.wrong_answer([OPTIMIZATION_APPROACH_1_EXISTS])

    if exercise.repo.branches.has_branch("optimization-approach-2"):
        raise exercise.wrong_answer([OPTIMIZATION_APPROACH_2_EXISTS])

    main_reflog = exercise.repo.branches.branch("main").reflog
    merge_logs = [entry for entry in main_reflog if entry.action.startswith("merge")]
    merge_order = [entry.action[len("merge ") :] for entry in merge_logs][::-1]
    for merge in merge_order:
        if merge == "optimization-approach-2":
            raise exercise.wrong_answer([OPTIMIZATION_APPROACH_2_MERGED])

    return exercise.to_output(
        ["Great job using git branch to delete both merged and unmerged branches!"],
        GitAutograderStatus.SUCCESSFUL,
    )
