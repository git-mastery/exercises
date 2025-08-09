from git_autograder import GitAutograderStatus, GitAutograderTestLoader, assert_output

from ..verify import (
    ALICE_NO_FETCH,
    ALICE_NO_MERGE,
    ALICE_REMOTE_MISSING,
    ALICE_REMOTE_WRONG,
    BOB_MERGE,
    BOB_NO_FETCH,
    BOB_REMOTE_MISSING,
    BOB_REMOTE_WRONG,
    RESET_EXERCISE,
    verify,
)

REPOSITORY_NAME = "fetch-and-pull"

loader = GitAutograderTestLoader(__file__, REPOSITORY_NAME, verify)


def test_base():
    with loader.load("specs/base.yml") as output:
        assert_output(output, GitAutograderStatus.SUCCESSFUL)


def test_alice_no_remote():
    with loader.load("specs/alice_no_remote.yml") as output:
        assert_output(output, GitAutograderStatus.UNSUCCESSFUL, [ALICE_REMOTE_MISSING])


def test_alice_wrong_remote():
    with loader.load("specs/alice_remote_wrong.yml") as output:
        assert_output(output, GitAutograderStatus.UNSUCCESSFUL, [ALICE_REMOTE_WRONG])


def test_alice_no_fetch():
    with loader.load("specs/alice_no_fetch.yml") as output:
        assert_output(output, GitAutograderStatus.UNSUCCESSFUL, [ALICE_NO_FETCH])


def test_alice_no_merge():
    with loader.load("specs/alice_no_merge.yml") as output:
        assert_output(output, GitAutograderStatus.UNSUCCESSFUL, [ALICE_NO_MERGE])


def test_bob_no_remote():
    with loader.load("specs/bob_no_remote.yml") as output:
        assert_output(output, GitAutograderStatus.UNSUCCESSFUL, [BOB_REMOTE_MISSING])


def test_bob_remote_wrong():
    with loader.load("specs/bob_remote_wrong.yml") as output:
        assert_output(output, GitAutograderStatus.UNSUCCESSFUL, [BOB_REMOTE_WRONG])


def test_bob_no_fetch():
    with loader.load("specs/bob_no_fetch.yml") as output:
        assert_output(output, GitAutograderStatus.UNSUCCESSFUL, [BOB_NO_FETCH])


def test_bob_merge():
    with loader.load("specs/bob_merge.yml") as output:
        assert_output(
            output, GitAutograderStatus.UNSUCCESSFUL, [BOB_MERGE, RESET_EXERCISE]
        )
