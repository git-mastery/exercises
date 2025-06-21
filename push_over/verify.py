import os

from git_autograder import (
    GitAutograderExercise,
    GitAutograderOutput,
    GitAutograderStatus,
)

MISSING_REPO = "You should have {repo} in your exercise folder. You might want to re-download the exercise."
MISSING_COMMIT = "You should have made a separate commit!"
MISSING_COMMIT_REMOTE = (
    "You might have forgotten to push your commit to the remote repository."
)


def verify(exercise: GitAutograderExercise) -> GitAutograderOutput:
    repo_name = exercise.config.exercise_repo.repo_name

    if not os.path.isdir(repo_name):
        raise exercise.wrong_answer([MISSING_REPO.format(repo=repo_name)])

    main_branch = exercise.repo.branches.branch("main")
    if len(main_branch.commits) == 1:
        raise exercise.wrong_answer([MISSING_COMMIT])

    origin_remote = exercise.repo.remotes.remote("origin")
    origin_remote.remote.fetch()
    remote_branch = exercise.repo.repo.refs["origin/main"]
    remote_commits = list(exercise.repo.repo.iter_commits(remote_branch))

    if len(remote_commits) == 1:
        raise exercise.wrong_answer([MISSING_COMMIT_REMOTE])

    return exercise.to_output(
        ["Great work pushing changes to the remote!"],
        GitAutograderStatus.SUCCESSFUL,
    )
