from pathlib import Path

from git_autograder import (
    GitAutograderOutput,
    GitAutograderExercise,
    GitAutograderStatus,
)

from exercise_utils.exercise_config import add_pr_config
from exercise_utils.github_cli import get_github_username, get_pr_numbers_by_author


JAVA_FILE_MISSING = "Java.txt file is missing in the latest commit on main branch."
JAVA_INVALID_CONTENT = "The content in Java.txt in main branch is not correct."
MUTIPLE_PRS = "Multiple PRs found. The lastest pr will be used in grading."
PR_MISSING = "No PR is found."
WRONG_HEAD_BRANCH = "The PR's head branch is not 'main'."


EXPECTED_CONTENT_STEP_3 = ["1955, by James Gosling"]


def verify(exercise: GitAutograderExercise) -> GitAutograderOutput:
    username = get_github_username(False)
    target_repo = f"git-mastery/{exercise.config.exercise_repo.repo_title}"
    comments = []
    
    pr_numbers = get_pr_numbers_by_author(username, target_repo, False)
    if not pr_numbers:
        raise exercise.wrong_answer([PR_MISSING])
    if len(pr_numbers) > 1:
        comments.append(MUTIPLE_PRS)
    pr_number = pr_numbers[-1]

    add_pr_config(pr_number=pr_number, config_path=Path("./"))
    exercise.fetch_pr()

    if exercise.repo.prs.pr.head_branch != "main":
        comments.append(WRONG_HEAD_BRANCH)
        raise exercise.wrong_answer(comments)

    latest_user_commit = exercise.repo.prs.pr.last_user_commit
    with latest_user_commit.file("Java.txt") as content:
        if content is None:
            comments.append(JAVA_FILE_MISSING)
            raise exercise.wrong_answer(comments)
        extracted_content = [line.strip() for line in content.splitlines() if line.strip() != ""]
    if extracted_content != EXPECTED_CONTENT_STEP_3:
        comments.append(JAVA_INVALID_CONTENT)
        raise exercise.wrong_answer(comments)

    comments.append("Good job creating the PR and pushing commits!")
    return exercise.to_output(comments, GitAutograderStatus.SUCCESSFUL)
