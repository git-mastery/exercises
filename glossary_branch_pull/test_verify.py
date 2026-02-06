from contextlib import contextmanager
from typing import Iterator, Tuple

from exercise_utils.test import (
    GitAutograderTest,
    GitAutograderTestLoader,
    assert_output,
)
from git_autograder import GitAutograderStatus
from repo_smith.repo_smith import RepoSmith

from .verify import (
    verify,
    BRANCH_MISSING,
    BRANCH_NOT_TRACKING,
    REMOTE_COMMIT_MISSING,
    LOCAL_COMMIT_MISSING,
)

REPOSITORY_NAME = "glossary-branch-pull"

loader = GitAutograderTestLoader(REPOSITORY_NAME, verify)


@contextmanager
def base_setup() -> Iterator[Tuple[GitAutograderTest, RepoSmith]]:
    with loader.start(include_remote_repo=True) as (test, rs, rs_remote):
        remote_path = str(rs_remote.repo.git_dir)
        rs.git.remote_add("origin", remote_path)

        rs.git.commit(allow_empty=True, message="Initial commit")

        rs.git.checkout("ABC", branch=True)
        rs.git.commit(allow_empty=True, message="Add 'cache'")
        rs.git.push("origin", "ABC", set_upstream=True)
        rs.git.reset("HEAD~1", hard=True)

        rs.git.checkout("DEF", branch=True)
        rs.git.commit(allow_empty=True, message="Add 'exception'")
        rs.git.push("origin", "DEF", set_upstream=True)
        rs.git.reset("HEAD~1", hard=True)
        rs.git.commit(allow_empty=True, message="Add 'documentation'")

        yield (test, rs)


def test_no_changes():
    with base_setup() as (test, rs):
        output = test.run()
        assert_output(
            output,
            GitAutograderStatus.UNSUCCESSFUL,
            [
                BRANCH_MISSING.format(branch="STU"),
                BRANCH_MISSING.format(branch="VWX"),
                REMOTE_COMMIT_MISSING.format(branch="ABC"),
                REMOTE_COMMIT_MISSING.format(branch="DEF"),
            ],
        )


def test_branch_not_tracking():
    with base_setup() as (test, rs):
        rs.git.checkout("STU", branch=True)
        rs.git.checkout("VWX", branch=True)

        output = test.run()
        assert_output(
            output,
            GitAutograderStatus.UNSUCCESSFUL,
            [
                BRANCH_NOT_TRACKING.format(branch="STU"),
                BRANCH_NOT_TRACKING.format(branch="VWX"),
                REMOTE_COMMIT_MISSING.format(branch="ABC"),
                REMOTE_COMMIT_MISSING.format(branch="DEF"),
            ],
        )


def test_def_local_commit_missing():
    with base_setup() as (test, rs):
        rs.git.checkout("STU", branch=True)
        rs.git.push("origin", "STU")

        rs.git.checkout("VWX", branch=True)
        rs.git.push("origin", "VWX")

        rs.git.checkout("ABC")
        rs.git.commit(allow_empty=True, message="Add 'cache'")

        rs.git.checkout("DEF")
        rs.git.reset("HEAD~1", hard=True)
        rs.git.fetch("origin")
        rs.git.merge("origin/DEF")

        output = test.run()
        assert_output(output, GitAutograderStatus.UNSUCCESSFUL, [LOCAL_COMMIT_MISSING])


def test_successful_changes():
    with base_setup() as (test, rs):
        rs.git.checkout("VWX", branch=True)
        rs.git.push("origin", "VWX", set_upstream=True)

        rs.git.checkout("STU", branch=True)
        rs.git.push("origin", "STU", set_upstream=True)

        rs.git.checkout("ABC")
        rs.git.fetch("origin")
        rs.git.merge("origin/ABC")

        rs.git.checkout("DEF")
        rs.git.fetch("origin")
        rs.git.merge("origin/DEF")

        output = test.run()
        assert_output(output, GitAutograderStatus.SUCCESSFUL)
