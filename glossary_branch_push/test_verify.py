from contextlib import contextmanager
from typing import Iterator, Tuple
import tempfile
import os

from exercise_utils.test import (
    GitAutograderTest,
    GitAutograderTestLoader,
    assert_output,
)
from git_autograder import GitAutograderStatus
from repo_smith.repo_smith import RepoSmith
from repo_smith.steps.bash_step import BashStep

from .verify import PQR_BRANCH_NOT_PUSHED, verify

REPOSITORY_NAME = "glossary-branch-push"

loader = GitAutograderTestLoader(REPOSITORY_NAME, verify)


@contextmanager
def base_setup() -> Iterator[Tuple[GitAutograderTest, RepoSmith]]:
    with loader.start() as (test, rs):
        rs.git.commit(message="Initial commit", allow_empty=True)
        
        # Create a bare repo to use as remote
        remote_dir = tempfile.mkdtemp()
        remote_path = os.path.join(remote_dir, "remote.git")
        os.makedirs(remote_path)
        BashStep(name=None, description=None, id=None, body=f"git init --bare {remote_path}").execute(rs.repo)
        
        rs.git.remote_add("origin", remote_path)
        
        rs.git.checkout("PQR", branch=True)
        rs.files.create_or_update("r.txt", "refactoring: Improving the code without changing what it does... in theory.\n")
        rs.git.add(all=True)
        rs.git.commit(message="Add 'refactoring'")
        rs.git.checkout("main")

        yield test, rs


def test_base():
    with base_setup() as (test, rs):
        BashStep(name=None, description=None, id=None, body="git push origin PQR").execute(rs.repo)

        output = test.run()
        assert_output(output, GitAutograderStatus.SUCCESSFUL)


def test_pqr_not_pushed():
    with base_setup() as (test, rs):
        output = test.run()
        assert_output(
            output,
            GitAutograderStatus.UNSUCCESSFUL,
            [PQR_BRANCH_NOT_PUSHED],
        )
