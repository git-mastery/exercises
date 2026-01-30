from contextlib import contextmanager
import os
from typing import Iterator, Tuple

from git_autograder import GitAutograderStatus
from exercise_utils.test import GitAutograderTest, GitAutograderTestLoader, assert_output
from repo_smith.repo_smith import RepoSmith

from .verify import(
    verify,
    STU_LOCAL_PRESENT,
    STU_REMOTE_PRESENT,
    RENAMED_LOCAL_MISSING,
    RENAMED_REMOTE_MISSING,
)

REPOSITORY_NAME = "glossary-branch-rename"
BRANCHES = ["ABC", "DEF", "STU", "VWX"]
EXPECTED_NEW_BRANCH_NAME = "S-to-Z"
BRANCH_TO_RENAME = "STU"

loader = GitAutograderTestLoader(REPOSITORY_NAME, verify)

@contextmanager
def base_setup() -> Iterator[Tuple[GitAutograderTest, RepoSmith]]:
    with loader.start(include_remote_repo=True) as (test, rs, rs_remote):
        # get the current set up repo, so that we can navigate back to this
        # directory after setting up "remote" repo, and proceed with "local" repo
        root_path = os.getcwd()

        remote_worktree_dir = rs_remote.repo.working_tree_dir
        if remote_worktree_dir is None:
            raise ValueError("Remote repo has no working tree.")

        remote_worktree = os.fspath(remote_worktree_dir)
        os.chdir(remote_worktree)
        rs_remote.git.commit(message="Empty", allow_empty=True)
        for remote_branch_name in BRANCHES:
            rs_remote.git.branch(remote_branch_name)

        os.chdir(root_path)

        # set up local repo
        rs.git.commit(message="Empty", allow_empty=True)
        rs.git.remote_add("origin", str(remote_worktree_dir))
        rs.git.fetch("origin")

        for remote_branch_names in BRANCHES:
            rs.git.branch(remote_branch_names, f"origin/{remote_branch_names}")
        
        os.chdir(root_path)

        yield test, rs

def test_base():
    with base_setup() as (test, rs):
        rs.git.branch(EXPECTED_NEW_BRANCH_NAME, old_branch=BRANCH_TO_RENAME, move=True)
        rs.git.push("origin", EXPECTED_NEW_BRANCH_NAME)
        rs.git.push("origin", f":{BRANCH_TO_RENAME}")
        
        output = test.run()
        assert_output(output, GitAutograderStatus.SUCCESSFUL)

def test_no_change():
    with base_setup() as (test, rs):
        output = test.run()
        assert_output(
            output,
            GitAutograderStatus.UNSUCCESSFUL,
            [
                STU_LOCAL_PRESENT,
                RENAMED_LOCAL_MISSING,
                STU_REMOTE_PRESENT,
                RENAMED_REMOTE_MISSING
            ]
        )

def test_changed_local_only():
    with base_setup() as (test, rs):
        rs.git.branch(EXPECTED_NEW_BRANCH_NAME, old_branch=BRANCH_TO_RENAME, move=True)
        output = test.run()
        assert_output(
            output,
            GitAutograderStatus.UNSUCCESSFUL,
            [
                STU_REMOTE_PRESENT,
                RENAMED_REMOTE_MISSING
            ]
        )
        
def test_changed_local_wrong_name():
    with base_setup() as (test, rs):
        rs.git.branch("S-to-X", old_branch=BRANCH_TO_RENAME, move=True)
        output = test.run()
        assert_output(
            output,
            GitAutograderStatus.UNSUCCESSFUL,
            [
                RENAMED_LOCAL_MISSING,
                STU_REMOTE_PRESENT,
                RENAMED_REMOTE_MISSING,
            ]
        )

def test_changed_remote_wrong_name():
    with base_setup() as (test, rs):
        rs.git.branch("S-to-X", old_branch=BRANCH_TO_RENAME, move=True)
        rs.git.push("origin", "S-to-X")
        rs.git.push("origin", f":{BRANCH_TO_RENAME}")
        output = test.run()
        assert_output(
            output,
            GitAutograderStatus.UNSUCCESSFUL,
            [
                RENAMED_LOCAL_MISSING,
                RENAMED_REMOTE_MISSING,
             ]
        )
        
def test_local_old_branch_still_exists():
    with base_setup() as (test, rs):
        rs.git.branch(EXPECTED_NEW_BRANCH_NAME)
        rs.git.push("origin", EXPECTED_NEW_BRANCH_NAME)
        rs.git.push("origin", f":{BRANCH_TO_RENAME}")

        output = test.run()
        assert_output(output, GitAutograderStatus.UNSUCCESSFUL,[STU_LOCAL_PRESENT,])

def test_remote_old_branch_still_exists():
    with base_setup() as (test, rs):
        rs.git.branch(EXPECTED_NEW_BRANCH_NAME, old_branch=BRANCH_TO_RENAME, move=True)
        rs.git.push("origin", EXPECTED_NEW_BRANCH_NAME)

        output = test.run()
        assert_output(output, GitAutograderStatus.UNSUCCESSFUL, [STU_REMOTE_PRESENT])
