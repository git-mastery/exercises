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

MERGE_NOT_UNDONE = (
    "You need to undo the merge."
)
MAIN_COMMITS_INCORRECT = (
    "The main branch does not contain the expected commits "
    "The main branch does not contain both commits 'Add Rick' and 'Add Morty'."
)
OTHERS_COMMITS_INCORRECT = (
    "The others branch does not contain the expected commits "
    "'Add Birdperson', 'Add Cyborg to birdperson.txt', and 'Add Tammy'."
)
OTHERS_BRANCH_MISSING = (
    "The branch 'others' no longer exists. You should not delete it, only undo the merge on main."
)

def verify(exercise: GitAutograderExercise) -> GitAutograderOutput:
    # Get branches
    main_branch = exercise.repo.branches.branch("main")
    others_branch = exercise.repo.branches.branch_or_none("others")

    # Check if branch others exists
    if others_branch is None:
        raise exercise.wrong_answer([OTHERS_BRANCH_MISSING])

    # Take all commit messages on main
    commit_messages_in_main = [c.commit.message.strip() for c in main_branch.commits]

    # Take all commit messages on others
    commit_messages_in_others = [c.commit.message.strip() for c in others_branch.commits]

    # Check that the merge commit is not present on main
    if any(msg in commit_messages_in_main for msg in [ADD_BIRDPERSON, ADD_CYBORG, ADD_TAMMY]):
        raise exercise.wrong_answer([MERGE_NOT_UNDONE])

    # Check that commits in main are only the initial 2 commits
    if len(commit_messages_in_main) != 2 or not all(
        msg in commit_messages_in_main for msg in [ADD_RICK, ADD_MORTY]
    ):
        raise exercise.wrong_answer([MAIN_COMMITS_INCORRECT])

    # Check that commits in others are only the initial 3 commits
    if len(commit_messages_in_others) != 5 or not all(
        msg in commit_messages_in_others for msg in [ADD_BIRDPERSON, ADD_CYBORG, ADD_TAMMY]
    ):
        raise exercise.wrong_answer([OTHERS_COMMITS_INCORRECT])

    return exercise.to_output(
        ["You have successfully undone the merge of branch 'others'."],
        GitAutograderStatus.SUCCESSFUL,
    )
