import os
from typing import List

from git_autograder import GitAutograderOutput, GitAutograderRepo


def verify(repo: GitAutograderRepo) -> GitAutograderOutput:
    comments: List[str] = []
    main_branch = repo.branches.branch("main")
    main_branch.latest_commit.checkout()

    # Read the file and parse it
    print(os.getcwd())

    main_branch.checkout()

    return repo.to_output(comments)
