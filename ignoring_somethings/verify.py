import os

import tempfile
from pathlib import Path
from typing import List

from git import Repo
from git_autograder import (
    GitAutograderExercise,
    GitAutograderOutput,
    GitAutograderStatus,
)

MISSING_COMMITS = "You have not committed the relevant changes yet!"
STILL_IGNORING_FILE_22 = "You are still ignoring many/file22.txt."
STILL_HIDING = (
    "You are still ignoring why_am_i_hidden.txt. Find where the file is and fix that."
)
NOT_IGNORING_IGNORE_ME = "You are not ignoring ignore_me.txt"
NOT_IGNORING_RUNAWAY = (
    "You are not ignoring runaway.txt. Find where the file is and fix that."
)
NOT_PATTERN_MATCHING_RUNAWAY = (
    "You should be using ** to match all subfolders to ignore runaway.txt."
)
NOT_IGNORING_REST_OF_MANY = (
    "You should be ignoring the rest of many/* except many/file22.txt!"
)
IGNORING_FIND_ME = "You should not be ignoring this/is/very/nested/find_me.txt!"
MISSING_GITIGNORE = "You are missing the .gitignore file! Try to reset the exercise using gitmastery progress reset"


def verify(exercise: GitAutograderExercise) -> GitAutograderOutput:
    main_branch = exercise.repo.branches.branch("main")

    exercise_dir = exercise.exercise_path
    repo_name = exercise.config.exercise_repo.repo_name
    repo_folder_path = os.path.join(exercise_dir, repo_name)
    gitignore_file_path = os.path.join(repo_folder_path, ".gitignore")

    if not os.path.isfile(gitignore_file_path):
        raise exercise.wrong_answer([MISSING_GITIGNORE])

    with open(gitignore_file_path, "r", encoding="utf-8") as gitignore_file:
        gitignore_file_contents = gitignore_file.read()

    no_user_commit = len(main_branch.user_commits) == 0

    # Verify that user has commited the ignore,
    # by comparing the local file and the committed file taken from the repo
    with main_branch.latest_commit.file(".gitignore") as commited_gitignore_file:
        if (
            commited_gitignore_file is None
            or commited_gitignore_file != gitignore_file_contents
        ):
            no_user_commit = True

    # Verify the state of the ignore by recreating the necessary files and checking if
    # Git ignores them directly in a separate temporary Git repository
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        (tmp_path / ".gitignore").write_text(gitignore_file_contents)

        simulated_files = [
            "why_am_i_hidden.txt",
            "ignore_me.txt",
            "this/is/very/nested/find_me.txt",
            "this/is/very/nested/runaway.txt",
        ] + [f"many/file{i}.txt" for i in range(1, 101)]
        for file in simulated_files:
            (tmp_path / file).parent.mkdir(parents=True, exist_ok=True)
            (tmp_path / file).touch()

        test_repo: Repo = Repo.init(tmp_path)
        ignored = {f for f in simulated_files if test_repo.ignored(f)}

        comments: List[str] = []
        if "many/file22.txt" in ignored:
            comments.append(STILL_IGNORING_FILE_22)

        for i in range(1, 101):
            if f"many/file{i}.txt" and i != 22 and f"many/file{i}.txt" not in ignored:
                comments.append(NOT_IGNORING_REST_OF_MANY)
                break

        if "why_am_i_hidden.txt" in ignored:
            comments.append(STILL_HIDING)

        if "ignore_me.txt" not in ignored:
            comments.append(NOT_IGNORING_IGNORE_ME)

        if "this/is/very/nested/find_me.txt" in ignored:
            comments.append(IGNORING_FIND_ME)

        if "this/is/very/nested/runaway.txt" not in ignored:
            comments.append(NOT_IGNORING_RUNAWAY)
        elif "this/**/runaway.txt" not in gitignore_file_contents.splitlines():
            comments.append(NOT_PATTERN_MATCHING_RUNAWAY)

        if no_user_commit:
            comments.append(MISSING_COMMITS)

        if comments:
            raise exercise.wrong_answer(comments)

        return exercise.to_output(
            ["Great work using .gitignore!"], status=GitAutograderStatus.SUCCESSFUL
        )
