from exercise_utils.test import GitAutograderTestLoader, assert_output
from git_autograder import GitAutograderStatus

from .verify import (
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

loader = GitAutograderTestLoader(REPOSITORY_NAME, verify)


def test_base():
    with loader.start(clone_from="https://github.com/git-mastery/gm-shapes") as (
        test,
        rs,
    ):
        rs.git.remote_add(
            "alice-upstream", "https://github.com/git-mastery/gm-shapes-alice.git"
        )
        rs.git.remote_add(
            "bob-upstream", "https://github.com/git-mastery/gm-shapes-bob.git"
        )
        rs.git.fetch("alice-upstream")
        rs.git.merge("alice-upstream/main")
        rs.git.fetch("bob-upstream")

        output = test.run()
        assert_output(output, GitAutograderStatus.SUCCESSFUL)


def test_alice_no_remote():
    with loader.start(clone_from="https://github.com/git-mastery/gm-shapes") as (
        test,
        _,
    ):
        output = test.run()
        assert_output(output, GitAutograderStatus.UNSUCCESSFUL, [ALICE_REMOTE_MISSING])


def test_alice_wrong_remote():
    with loader.start(clone_from="https://github.com/git-mastery/gm-shapes") as (
        test,
        rs,
    ):
        rs.git.remote_add(
            "alice-upstream", "https://github.com/git-mastery/gm-shapes-bob.git"
        )

        output = test.run()
        assert_output(output, GitAutograderStatus.UNSUCCESSFUL, [ALICE_REMOTE_WRONG])


def test_alice_no_fetch():
    with loader.start(clone_from="https://github.com/git-mastery/gm-shapes") as (
        test,
        rs,
    ):
        rs.git.remote_add(
            "alice-upstream", "https://github.com/git-mastery/gm-shapes-alice.git"
        )
        rs.git.remote_add(
            "bob-upstream", "https://github.com/git-mastery/gm-shapes-bob.git"
        )
        rs.git.fetch("bob-upstream")

        output = test.run()
        assert_output(output, GitAutograderStatus.UNSUCCESSFUL, [ALICE_NO_FETCH])


def test_alice_no_merge():
    with loader.start(clone_from="https://github.com/git-mastery/gm-shapes") as (
        test,
        rs,
    ):
        rs.git.remote_add(
            "alice-upstream", "https://github.com/git-mastery/gm-shapes-alice.git"
        )
        rs.git.remote_add(
            "bob-upstream", "https://github.com/git-mastery/gm-shapes-bob.git"
        )
        rs.git.fetch("alice-upstream")
        rs.git.fetch("bob-upstream")

        output = test.run()
        assert_output(output, GitAutograderStatus.UNSUCCESSFUL, [ALICE_NO_MERGE])


def test_bob_no_remote():
    with loader.start(clone_from="https://github.com/git-mastery/gm-shapes") as (
        test,
        rs,
    ):
        rs.git.remote_add(
            "alice-upstream", "https://github.com/git-mastery/gm-shapes-alice.git"
        )
        rs.git.fetch("alice-upstream")
        rs.git.merge("alice-upstream/main")

        output = test.run()
        assert_output(output, GitAutograderStatus.UNSUCCESSFUL, [BOB_REMOTE_MISSING])


def test_bob_remote_wrong():
    with loader.start(clone_from="https://github.com/git-mastery/gm-shapes") as (
        test,
        rs,
    ):
        rs.git.remote_add(
            "alice-upstream", "https://github.com/git-mastery/gm-shapes-alice.git"
        )
        rs.git.fetch("alice-upstream")
        rs.git.merge("alice-upstream/main")
        rs.git.remote_add(
            "bob-upstream", "https://github.com/git-mastery/gm-shapes-alice.git"
        )

        output = test.run()
        assert_output(output, GitAutograderStatus.UNSUCCESSFUL, [BOB_REMOTE_WRONG])


def test_bob_no_fetch():
    with loader.start(clone_from="https://github.com/git-mastery/gm-shapes") as (
        test,
        rs,
    ):
        rs.git.remote_add(
            "alice-upstream", "https://github.com/git-mastery/gm-shapes-alice.git"
        )
        rs.git.remote_add(
            "bob-upstream", "https://github.com/git-mastery/gm-shapes-bob.git"
        )
        rs.git.fetch("alice-upstream")
        rs.git.merge("alice-upstream/main")

        output = test.run()
        assert_output(output, GitAutograderStatus.UNSUCCESSFUL, [BOB_NO_FETCH])


def test_bob_merge():
    with loader.start(clone_from="https://github.com/git-mastery/gm-shapes") as (
        test,
        rs,
    ):
        rs.git.remote_add(
            "alice-upstream", "https://github.com/git-mastery/gm-shapes-alice.git"
        )
        rs.git.remote_add(
            "bob-upstream", "https://github.com/git-mastery/gm-shapes-bob.git"
        )
        rs.git.fetch("alice-upstream")
        rs.git.merge("alice-upstream/main")
        rs.git.fetch("bob-upstream")
        rs.git.merge("bob-upstream/main")

        output = test.run()
        assert_output(
            output, GitAutograderStatus.UNSUCCESSFUL, [BOB_MERGE, RESET_EXERCISE]
        )
