from git_autograder import (
    GitAutograderOutput,
    GitAutograderExercise,
    GitAutograderStatus,
)

ADD_JOEY = "Add Joey"
ADD_PHOEBE = "Add Phoebe"
ADD_ROSS = "Add Ross"

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

    commit_messages_in_main = [c.commit.message.strip() for c in main_branch.commits]

    merge_commits = [c for c in main_branch.commits if len(c.parents) > 1]
    if merge_commits:
        print("Yo" + merge_commits[0].commit.message)
        print(commit_messages_in_main)
        print(merge_commits[0].parents[0].commit.message)
        print(merge_commits[0].parents[1].commit.message)
        print(main_branch.commits[0].stats.files)
        raise exercise.wrong_answer([SQUASH_NOT_USED])

    with exercise.repo.files.file_or_none("mike.txt") as mike_file:
        if mike_file is None:
            raise exercise.wrong_answer([CHANGES_FROM_SUPPORTING_NOT_PRESENT])

    with exercise.repo.files.file_or_none("janice.txt") as janice_file:
        if janice_file is None:
            raise exercise.wrong_answer([CHANGES_FROM_SUPPORTING_NOT_PRESENT])

    if not all(
        msg in commit_messages_in_main for msg in [ADD_JOEY, ADD_PHOEBE, ADD_ROSS]
    ):
        raise exercise.wrong_answer([MAIN_COMMITS_INCORRECT])

    return exercise.to_output([], GitAutograderStatus.SUCCESSFUL)
