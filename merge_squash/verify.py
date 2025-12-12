from git_autograder import (
    GitAutograderOutput,
    GitAutograderExercise,
    GitAutograderStatus,
)

SQUASH_NOT_USED = (
    "You should be using squash merge, not regular merge."
)

MAIN_COMMITS_INCORRECT = (
    "The main branch does not contain at least one of these commits: 'Add Joey', 'Add Phoebe' or 'Add Ross'."
)

CHANGES_FROM_SUPPORTING_NOT_PRESENT = (
    "The main branch does not contain both files 'mike.txt' and 'janice.txt'."
)


def verify(exercise: GitAutograderExercise) -> GitAutograderOutput:
    main_branch = exercise.repo.branches.branch("main")

    with exercise.repo.files.file_or_none("mike.txt") as mike_file:
        if mike_file is None:
            raise exercise.wrong_answer([CHANGES_FROM_SUPPORTING_NOT_PRESENT])

    with exercise.repo.files.file_or_none("janice.txt") as janice_file:
        if janice_file is None:
            raise exercise.wrong_answer([CHANGES_FROM_SUPPORTING_NOT_PRESENT])

    commit_messages_in_main = [c.commit.message.strip() for c in main_branch.commits]
    merge_commits = [c for c in main_branch.commits if len(c.parents) > 1]

    if merge_commits or ("Squash" not in commit_messages_in_main[0]):
        raise exercise.wrong_answer([SQUASH_NOT_USED])

    if not all(
        msg in commit_messages_in_main for msg in ["Add Joey", "Add Phoebe", "Add Ross"]
    ):
        raise exercise.wrong_answer([MAIN_COMMITS_INCORRECT])

    return exercise.to_output(["Good job performing a merge squash!"], GitAutograderStatus.SUCCESSFUL)
