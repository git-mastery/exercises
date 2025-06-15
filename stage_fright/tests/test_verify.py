from git_autograder import GitAutograderStatus, GitAutograderTestLoader, assert_output

from ..verify import NOT_ADDED, verify

REPOSITORY_NAME = "stage-fright"

loader = GitAutograderTestLoader(__file__, REPOSITORY_NAME, verify)


def test_missing_add():
    with loader.load("specs/missing_add.yml", "start") as output:
        names = ["alice", "bob", "joe"]
        assert_output(
            output,
            GitAutograderStatus.UNSUCCESSFUL,
            [NOT_ADDED.format(file=f"{name}.txt") for name in names],
        )


def test_added_all():
    with loader.load("specs/added_all.yml", "start") as output:
        assert_output(
            output,
            GitAutograderStatus.SUCCESSFUL,
        )
