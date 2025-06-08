from typing import List

from git_autograder import GitAutograderOutput, GitAutograderStatus


def verify() -> GitAutograderOutput:
    res = input("hi: ")
    print(res)

    return GitAutograderOutput(
        status=GitAutograderStatus.SUCCESSFUL,
        started_at=None,
        completed_at=None,
        comments=[],
        exercise_name="remote-control",
    )
