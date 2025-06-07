from git_autograder import GitAutograderStatus, GitAutograderTestLoader

from ..verify import NOT_ADDED, verify

REPOSITORY_NAME = "stage-fright"

loader = GitAutograderTestLoader(__file__, REPOSITORY_NAME, verify)


def test_missing_add():
    with loader.load("specs/missing_add.yml", "start") as output:
        assert output.status == GitAutograderStatus.UNSUCCESSFUL
        names = ["alice", "bob", "joe"]
        for name in names:
            assert NOT_ADDED.format(file=f"{name}.txt") in (output.comments or [])


def test_added_all():
    with loader.load("specs/added_all.yml", "start") as output:
        assert output.status == GitAutograderStatus.SUCCESSFUL
