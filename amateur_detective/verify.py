from typing import List

from git_autograder import GitAutograderOutput, GitAutograderRepo


def verify(repo: GitAutograderRepo) -> GitAutograderOutput:
    comments: List[str] = []

    # INSERT YOUR GRADING CODE HERE

    return repo.to_output(comments)
