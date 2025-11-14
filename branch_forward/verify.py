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

    if not merge_logs:
        raise exercise.wrong_answer([FAST_FORWARD_REQUIRED])

    main_commits = list(main_branch.commits)
    if any(len(commit.parents) > 1 for commit in main_commits):
        raise exercise.wrong_answer([FAST_FORWARD_REQUIRED])

    if any(entry.message != "Fast-forward" for entry in merge_logs):
        raise exercise.wrong_answer([FAST_FORWARD_REQUIRED])

    merged_branches = [entry.action[len("merge ") :] for entry in merge_logs]

    if "with-sally" not in merged_branches:
        raise exercise.wrong_answer([ONLY_WITH_SALLY_MERGED])

    if any(branch != "with-sally" for branch in merged_branches):
        raise exercise.wrong_answer([ONLY_WITH_SALLY_MERGED])

    return exercise.to_output(
        ["Great job fast-forward merging only 'with-sally' and cleaning up the branch!"],
        GitAutograderStatus.SUCCESSFUL,
    )
