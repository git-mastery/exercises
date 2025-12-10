from git_autograder import GitAutograderStatus, GitAutograderTestLoader, assert_output

from ..verify import (
    SQUASH_NOT_USED,
    MAIN_COMMITS_INCORRECT,
    CHANGES_FROM_SUPPORTING_NOT_PRESENT,
    verify
)

REPOSITORY_NAME = "merge-squash"

loader = GitAutograderTestLoader(__file__, REPOSITORY_NAME, verify)


def test_base():
    with loader.load("specs/base.yml") as output:
        assert_output(output, GitAutograderStatus.SUCCESSFUL)

def test_non_squash_merge_used():
    with loader.load("specs/non_squash_merge_used.yml") as output:
        assert_output(output, GitAutograderStatus.UNSUCCESSFUL, [SQUASH_NOT_USED])

def test_not_merged():
    with loader.load("specs/not_merged.yml") as output:
        assert_output(output, GitAutograderStatus.UNSUCCESSFUL, [CHANGES_FROM_SUPPORTING_NOT_PRESENT])

def test_missing_main_commits():
    with loader.load("specs/missing_main_commits.yml") as output:
        assert_output(output, GitAutograderStatus.UNSUCCESSFUL, [MAIN_COMMITS_INCORRECT])
