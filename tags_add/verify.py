from typing import List
from git_autograder.core import GitAutograderExercise, GitAutograderStatus

MSG_NO_TAG = "Tag 'v1.0.0' was not found."
MSG_NOT_AT_HEAD = "Tag 'v1.0.0' does not point to HEAD."

def verify(exercise: GitAutograderExercise):
    """
    Pass condition：
    1) exist 1.0.0 tag
    2) the tag is pointing to current head
    """
    repo = exercise.repo.repo
    target = next((t for t in repo.tags if t.name == "v1.0.0"), None)

    messages: List[str] = []
    status = GitAutograderStatus.SUCCESSFUL

    if target is None:
        messages.append(MSG_NO_TAG)
        status = GitAutograderStatus.FAILED
    elif target.commit.hexsha != repo.head.commit.hexsha:
        messages.append(MSG_NOT_AT_HEAD)
        status = GitAutograderStatus.FAILED

    return exercise.to_output(messages, status)
