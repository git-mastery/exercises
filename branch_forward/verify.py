from git_autograder import (
    GitAutograderExercise,
    GitAutograderOutput,
    GitAutograderStatus,
)

FAST_FORWARD_REQUIRED = (
    "You must use a fast-forward merge to bring a branch into 'main'."
)

ONLY_WITH_SALLY_MERGED = (
    "Only one of the two starting branches can be fast-forward merged into 'main'. Do not create new branches."
)

def verify(exercise: GitAutograderExercise) -> GitAutograderOutput:
    main_branch = exercise.repo.branches.branch("main")
    merge_logs = [
        entry for entry in main_branch.reflog if entry.action.startswith("merge ")
    ]

    merged_branches = [entry.action[len("merge ") :] for entry in merge_logs]

    if "with-sally" not in merged_branches:
        raise exercise.wrong_answer([ONLY_WITH_SALLY_MERGED])

    latest_with_sally_merge = next(
        (entry for entry in merge_logs if entry.action == "merge with-sally"), None
    )

    if latest_with_sally_merge is None:
        raise exercise.wrong_answer([FAST_FORWARD_REQUIRED])

    if latest_with_sally_merge.message != "Fast-forward":
        raise exercise.wrong_answer([FAST_FORWARD_REQUIRED])

    if any(branch != "with-sally" for branch in merged_branches):
        raise exercise.wrong_answer([ONLY_WITH_SALLY_MERGED])

    return exercise.to_output(
        ["Great job fast-forward merging only 'with-sally' and cleaning up the branch!"],
        GitAutograderStatus.SUCCESSFUL,
    )

