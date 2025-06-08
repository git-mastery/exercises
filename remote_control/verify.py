from typing import List

from git_autograder import GitAutograderOutput, GitAutograderRepo


def verify(repo: GitAutograderRepo) -> GitAutograderOutput:
    comments: List[str] = []

    res = input("hi: ")
    print(res)

    return repo.to_output(comments)
