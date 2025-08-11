from git_autograder import (
    GitAutograderOutput,
    GitAutograderExercise,
    GitAutograderStatus,
)


def verify(exercise: GitAutograderExercise) -> GitAutograderOutput:
    # INSERT YOUR GRADING CODE HERE

    return exercise.to_output([], GitAutograderStatus.SUCCESSFUL)
