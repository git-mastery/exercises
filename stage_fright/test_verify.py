from exercise_utils.test import GitAutograderTestLoader, assert_output
from git_autograder import GitAutograderStatus

from .verify import NOT_ADDED, verify

REPOSITORY_NAME = "stage-fright"

loader = GitAutograderTestLoader(REPOSITORY_NAME, verify)


def test_missing_add():
    with loader.start() as (test, rs):
        rs.git.commit(message="Empty", allow_empty=True)
        for name in ["alice", "bob", "jim", "joe", "carrey"]:
            rs.files.create_or_update(f"{name}.txt")
        rs.git.add(["jim.txt", "carrey.txt"])

        names = ["alice", "bob", "joe"]
        output = test.run()
        assert_output(
            output,
            GitAutograderStatus.UNSUCCESSFUL,
            [NOT_ADDED.format(file=f"{name}.txt") for name in names],
        )


def test_added_all():
    with loader.start() as (test, rs):
        rs.git.commit(message="Empty", allow_empty=True)
        for name in ["alice", "bob", "jim", "joe", "carrey"]:
            rs.files.create_or_update(f"{name}.txt")
            rs.git.add(f"{name}.txt")

        output = test.run()
        assert_output(
            output,
            GitAutograderStatus.SUCCESSFUL,
        )
