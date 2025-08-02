from git_autograder import GitAutograderStatus, GitAutograderTestLoader, assert_output

from ..verify import MISSING_UPSTREAM_REMOTE, WRONG_UPSTREAM_URL, verify

REPOSITORY_NAME = "link-me"

loader = GitAutograderTestLoader(__file__, REPOSITORY_NAME, verify)


def test_valid():
    with loader.load("specs/valid.yml", "start") as output:
        assert_output(output, GitAutograderStatus.SUCCESSFUL)


def test_valid_ssh():
    with loader.load("specs/valid_ssh.yml", "start") as output:
        assert_output(output, GitAutograderStatus.SUCCESSFUL)


def test_invalid_ssh():
    with loader.load("specs/invalid_ssh.yml", "start") as output:
        assert_output(output, GitAutograderStatus.UNSUCCESSFUL, [WRONG_UPSTREAM_URL])


def test_wrong_url():
    with loader.load("specs/wrong_url.yml", "start") as output:
        assert_output(output, GitAutograderStatus.UNSUCCESSFUL, [WRONG_UPSTREAM_URL])


def test_wrong_name():
    with loader.load("specs/wrong_name.yml", "start") as output:
        assert_output(
            output, GitAutograderStatus.UNSUCCESSFUL, [MISSING_UPSTREAM_REMOTE]
        )
