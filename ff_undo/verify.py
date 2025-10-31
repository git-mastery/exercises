from git_autograder import (
    GitAutograderOutput,
    GitAutograderExercise,
    GitAutograderStatus,
)

MERGE_NOT_UNDONE = (
    "The merge commit 'Introduce others' is still present. "
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

    # Check if branch others exists
    if not exercise.repo.branches.has_branch("others"):
        raise exercise.wrong_answer([OTHERS_BRANCH_MISSING])

    # Take all commit messages on main
    commit_messages_in_main = [c.message.strip() for c in exercise.repo.repo.iter_commits("main")]

    # Take all commit messages on others
    commit_messages_in_others = [c.message.strip() for c in exercise.repo.repo.iter_commits("others")]

    # Check that the merge commit is not present on main
    has_birdperson_in_main = any("Add Birdperson" in msg for msg in commit_messages_in_main)
    has_cyborg_in_main = any("Add Cyborg to birdperson.txt" in msg for msg in commit_messages_in_main)
    has_tammy_in_main = any("Add Tammy" in msg for msg in commit_messages_in_main)
    if has_birdperson_in_main or has_birdperson_in_main or has_tammy_in_main:
        raise exercise.wrong_answer([MERGE_NOT_UNDONE])

    # Check that commits in main are only the initial 2 commits
    has_rick = any("Add Rick" in msg for msg in commit_messages_in_main)
    has_morty = any("Add Morty" in msg for msg in commit_messages_in_main)
    if len(commit_messages_in_main) != 3 or not (has_rick and has_morty):
        raise exercise.wrong_answer([MAIN_COMMITS_INCORRECT])

    # Check that commits in others are only the initial 3 commits
    has_birdperson = any("Add Birdperson" in msg for msg in commit_messages_in_others)
    has_cyborg = any("Add Cyborg to birdperson.txt" in msg for msg in commit_messages_in_others)
    has_tammy = any("Add Tammy" in msg for msg in commit_messages_in_others)
    if len(commit_messages_in_others) != 6 or not (has_birdperson and has_cyborg and has_tammy):
        raise exercise.wrong_answer([OTHERS_COMMITS_INCORRECT])

    return exercise.to_output(
        ["You have successfully undone the merge of branch 'others'."],
        GitAutograderStatus.SUCCESSFUL,
    )
