from git_autograder import (
    GitAutograderOutput,
    GitAutograderExercise,
    GitAutograderStatus,
)

ADD_RICK = "Add Rick"
ADD_MORTY = "Add Morty"
ADD_BIRDPERSON = "Add Birdperson"
ADD_CYBORG = "Add Cyborg to birdperson.txt"
ADD_TAMMY = "Add Tammy"

MERGE_NOT_UNDONE = "The merge has not been undone properly."
MAIN_COMMITS_INCORRECT = "The main branch does not contain the expected commits."
OTHERS_COMMITS_INCORRECT = "The others branch does not contain the expected commits."
OTHERS_BRANCH_MISSING = "Missing branch 'others'."


def verify(exercise: GitAutograderExercise) -> GitAutograderOutput:
    main_branch = exercise.repo.branches.branch("main")
    others_branch = exercise.repo.branches.branch_or_none("others")

    if others_branch is None:
        raise exercise.wrong_answer([OTHERS_BRANCH_MISSING])

    # Verify commits in main branch
    commit_messages_in_main = [c.commit.message.strip() for c in main_branch.commits]
    if any(
        msg in commit_messages_in_main
        for msg in [ADD_BIRDPERSON, ADD_CYBORG, ADD_TAMMY]
    ):
        raise exercise.wrong_answer([MERGE_NOT_UNDONE])

    if len(commit_messages_in_main) != 3 or not all(
        msg in commit_messages_in_main for msg in [ADD_RICK, ADD_MORTY]
    ):
        raise exercise.wrong_answer([MAIN_COMMITS_INCORRECT])

    # Verify commits in others branch
    commit_messages_in_others = [
        c.commit.message.strip() for c in others_branch.commits
    ]
    if len(commit_messages_in_others) != 6 or not all(
        msg in commit_messages_in_others
        for msg in [ADD_BIRDPERSON, ADD_CYBORG, ADD_TAMMY, ADD_RICK, ADD_MORTY]
    ):
        raise exercise.wrong_answer([OTHERS_COMMITS_INCORRECT])

    return exercise.to_output(
        ["You have successfully undone the merge of branch 'others'."],
        GitAutograderStatus.SUCCESSFUL,
    )
