from git_autograder import GitAutograderStatus, GitAutograderTestLoader, assert_output

from ..verify import (
    FAST_FORWARD_REQUIRED,
    ONLY_WITH_SALLY_MERGED,
    verify,
)

REPOSITORY_NAME = "branch-forward"

loader = GitAutograderTestLoader(__file__, REPOSITORY_NAME, verify)


def test_success():
    with loader.load("specs/base.yml", "start") as output:
        assert_output(output, GitAutograderStatus.SUCCESSFUL)


def test_no_merges():
    with loader.load("specs/no_merges.yml", "start") as output:
        assert_output(
            output,
            GitAutograderStatus.UNSUCCESSFUL,
            [ONLY_WITH_SALLY_MERGED],
        )


def test_other_branch_non_ff():
    with loader.load("specs/other_branch_non_ff.yml", "start") as output:
        assert_output(
            output,
            GitAutograderStatus.UNSUCCESSFUL,
            [ONLY_WITH_SALLY_MERGED],
        )


def test_other_branch_ff():
    with loader.load("specs/other_branch_ff.yml", "start") as output:
        assert_output(
            output,
            GitAutograderStatus.UNSUCCESSFUL,
            [ONLY_WITH_SALLY_MERGED],
        )


def test_merge_with_sally_no_ff():
    with loader.load("specs/merge_with_sally_no_ff.yml", "start") as output:
        assert_output(
            output,
            GitAutograderStatus.UNSUCCESSFUL,
            [FAST_FORWARD_REQUIRED],
        )
