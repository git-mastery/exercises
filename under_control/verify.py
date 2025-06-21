from pathlib import Path

from git_autograder import GitAutograderExercise, GitAutograderOutput
from git_autograder.status import GitAutograderStatus


def verify(exercise: GitAutograderExercise) -> GitAutograderOutput:
    current = Path.cwd()
    for parent in [current] + list(current.parents):
        if (parent / ".gitmastery-exercise.json").is_file():
            if (parent / "control-me" / ".git").is_dir():
                return exercise.to_output(
                    [
                        "You successfully used git init to initialize this folder as a Git repository!"
                    ],
                    GitAutograderStatus.SUCCESSFUL,
                )

    raise exercise.wrong_answer(["This folder isn't a Git repository yet!"])
