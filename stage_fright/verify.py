from typing import List

from git_autograder import GitAutograderOutput, GitAutograderRepo


def verify(repo: GitAutograderRepo) -> GitAutograderOutput:
    comments: List[str] = []

    staged_diff = repo.repo.index.diff("HEAD")

    for diff_item in staged_diff:
        print(diff_item.a_path)

    return repo.to_output(comments)
