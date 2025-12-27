from exercise_utils.test import GitAutograderTestLoader, assert_output
from git_autograder.status import GitAutograderStatus

from .verify import EXTRA_FILES_UNSTAGED, MISSING_FILES_UNSTAGED, verify

REPOSITORY_NAME = "staging-intervention"

loader = GitAutograderTestLoader(REPOSITORY_NAME, verify)


def test_base():
    with loader.start() as (test, rs):
        rs.git.commit(allow_empty=True, message="Empty")
        names = ["josh", "adam", "mary", "jane", "charlie", "kristen", "alice", "john"]
        for name in names:
            rs.files.create_or_update(f"{name}.txt")
            rs.git.add(f"{name}.txt")
        rs.git.restore(["josh.txt", "adam.txt", "mary.txt"], staged=True)

        output = test.run()
        assert_output(output, GitAutograderStatus.SUCCESSFUL)


def test_extra_unstaged():
    with loader.start() as (test, rs):
        rs.git.commit(allow_empty=True, message="Empty")
        names = ["josh", "adam", "mary", "jane", "charlie", "kristen", "alice", "john"]
        for name in names:
            rs.files.create_or_update(f"{name}.txt")
            rs.git.add(f"{name}.txt")
        rs.git.restore(
            ["josh.txt", "adam.txt", "mary.txt", "kristen.txt", "john.txt"], staged=True
        )

        output = test.run()
        assert_output(output, GitAutograderStatus.UNSUCCESSFUL, [EXTRA_FILES_UNSTAGED])


def test_missing_unstaged():
    with loader.start() as (test, rs):
        rs.git.commit(allow_empty=True, message="Empty")
        names = ["josh", "adam", "mary", "jane", "charlie", "kristen", "alice", "john"]
        for name in names:
            rs.files.create_or_update(f"{name}.txt")
            rs.git.add(f"{name}.txt")
        rs.git.restore(["josh.txt", "adam.txt"], staged=True)

        output = test.run()
        assert_output(
            output, GitAutograderStatus.UNSUCCESSFUL, [MISSING_FILES_UNSTAGED]
        )


def test_mixed_unstaged():
    with loader.start() as (test, rs):
        rs.git.commit(allow_empty=True, message="Empty")
        names = ["josh", "adam", "mary", "jane", "charlie", "kristen", "alice", "john"]
        for name in names:
            rs.files.create_or_update(f"{name}.txt")
            rs.git.add(f"{name}.txt")
        rs.git.restore(["josh.txt", "adam.txt", "alice.txt"], staged=True)

        output = test.run()
        assert_output(
            output,
            GitAutograderStatus.UNSUCCESSFUL,
            [EXTRA_FILES_UNSTAGED, MISSING_FILES_UNSTAGED],
        )
