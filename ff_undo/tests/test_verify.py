from git_autograder import GitAutograderTestLoader, assert_output
from git_autograder.status import GitAutograderStatus
from ..verify import ( 
    MERGE_NOT_UNDONE,
    MAIN_COMMITS_INCORRECT,
    OTHERS_COMMITS_INCORRECT,
    OTHERS_BRANCH_MISSING,
    verify
)

REPOSITORY_NAME = "ff-undo"

loader = GitAutograderTestLoader(__file__, REPOSITORY_NAME, verify)

def test_correct_solution():
    with loader.load("specs/base.yml") as output:
        assert_output(output, GitAutograderStatus.SUCCESSFUL)


def test_merge_not_undone():
    with loader.load("specs/merge_not_undone.yml") as output:
        assert_output(output, GitAutograderStatus.UNSUCCESSFUL, [MERGE_NOT_UNDONE])


def test_branch_missing():
    with loader.load("specs/branch_missing.yml") as output:
        assert_output(output, GitAutograderStatus.UNSUCCESSFUL, [OTHERS_BRANCH_MISSING])


def test_main_commits_incorrect():
    with loader.load("specs/main_commits_incorrect.yml") as output:
        assert_output(output, GitAutograderStatus.UNSUCCESSFUL, [MAIN_COMMITS_INCORRECT])


def test_others_commits_incorrect():
    with loader.load("specs/others_commits_incorrect.yml") as output:
        assert_output(output, GitAutograderStatus.UNSUCCESSFUL, [OTHERS_COMMITS_INCORRECT])
