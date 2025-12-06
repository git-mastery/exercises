from git import TagObject
from git_autograder import GitAutograderExercise, GitAutograderStatus

FIRST_TAG = "first-pilot"
SECOND_TAG = "v1.0"
SECOND_TAG_MSG = "first full duty roster"
MARCH_MSG_FRAGMENT = "Update roster for March"

MISSING_FIRST_TAG = f'Missing lightweight tag "{FIRST_TAG}".'
MISSING_SECOND_TAG = f'Missing annotated tag "{SECOND_TAG}".'
WRONG_SECOND_TAG_MESSAGE = f'"{SECOND_TAG}" message must be exactly "{SECOND_TAG_MSG}".'
SUCCESS_MESSAGE = "Great work using git tag to annotate various commits in the repository!"


def verify(exercise: GitAutograderExercise):
    repo = exercise.repo.repo

    root_sha = next(repo.iter_commits(rev="HEAD", reverse=True)).hexsha

    march_commit = None
    for c in repo.iter_commits("HEAD"):
        if MARCH_MSG_FRAGMENT in c.message:
            march_commit = c
            break

    comments = []

    t_first = next((t for t in repo.tags if t.name == FIRST_TAG), None)
    if not t_first:
        comments.append(MISSING_FIRST_TAG)
    else:
        if t_first.commit.hexsha != root_sha:
            comments.append(
                f'"{FIRST_TAG}" should point to first commit {root_sha[:7]}, '
                f"but points to {t_first.commit.hexsha[:7]} instead."
            )
        if isinstance(getattr(t_first, "tag", None), TagObject):
            comments.append(f"`{FIRST_TAG}` must be a lightweight tag (not annotated).")

    t_v1 = next((t for t in repo.tags if t.name == SECOND_TAG), None)
    if not t_v1:
        comments.append(MISSING_SECOND_TAG)
    else:
        if not isinstance(getattr(t_v1, "tag", None), TagObject):
            comments.append(f"`{SECOND_TAG}` must be an annotated tag.")
        else:
            msg = (t_v1.tag.message or "").strip()
            if msg != SECOND_TAG_MSG:
                comments.append(WRONG_SECOND_TAG_MESSAGE)
        if not march_commit:
            comments.append(f"Could not find the commit containing '{MARCH_MSG_FRAGMENT}'.")
        else:
            if t_v1.commit.hexsha != march_commit.hexsha:
                comments.append(
                    f"`{SECOND_TAG}` should point to March commit {march_commit.hexsha[:7]}, "
                    f"but points to {t_v1.commit.hexsha[:7]} instead."
                )

    status = GitAutograderStatus.SUCCESSFUL if not comments else GitAutograderStatus.UNSUCCESSFUL

    if status == GitAutograderStatus.SUCCESSFUL:
        return exercise.to_output([SUCCESS_MESSAGE], status)

    return exercise.to_output(comments, status)
