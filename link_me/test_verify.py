from exercise_utils.test import GitAutograderTestLoader, assert_output
from git_autograder import GitAutograderStatus

from .verify import MISSING_UPSTREAM_REMOTE, WRONG_UPSTREAM_URL, verify

REPOSITORY_NAME = "link-me"

loader = GitAutograderTestLoader(REPOSITORY_NAME, verify)


def test_valid():
    with loader.start() as (test, rs):
        rs.git.remote_add("upstream", "https://github.com/git-mastery/link-me.git")

        output = test.run()
        assert_output(output, GitAutograderStatus.SUCCESSFUL)


def test_valid_ssh():
    with loader.start() as (test, rs):
        rs.git.remote_add("upstream", "git@github.com:git-mastery/link-me.git")

        output = test.run()
        assert_output(output, GitAutograderStatus.SUCCESSFUL)


def test_invalid_ssh():
    with loader.start() as (test, rs):
        rs.git.remote_add("upstream", "git@github.com/git-mastery/link-me.git")

        output = test.run()
        assert_output(output, GitAutograderStatus.UNSUCCESSFUL, [WRONG_UPSTREAM_URL])


def test_wrong_url():
    with loader.start() as (test, rs):
        rs.git.remote_add("upstream", "git@github.com/git-mastery/exercises.git")

        output = test.run()
        assert_output(output, GitAutograderStatus.UNSUCCESSFUL, [WRONG_UPSTREAM_URL])


def test_long_url():
    with loader.start() as (test, rs):
        rs.git.remote_add(
            "upstream", "git@github.com/git-mastery/path/part/link-me.git"
        )

        output = test.run()
        assert_output(output, GitAutograderStatus.UNSUCCESSFUL, [WRONG_UPSTREAM_URL])


def test_wrong_name():
    with loader.start() as (test, rs):
        rs.git.remote_add("origin", "https://github.com/git-mastery/link-me")

        output = test.run()
        assert_output(
            output, GitAutograderStatus.UNSUCCESSFUL, [MISSING_UPSTREAM_REMOTE]
        )
