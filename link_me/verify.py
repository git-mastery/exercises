from git_autograder import GitAutograderOutput, GitAutograderRepo, GitAutograderStatus

MISSING_UPSTREAM_REMOTE = "Missing remote called 'upstream'."
WRONG_UPSTREAM_URL = "Wrong 'upstream' remote URL"


def verify(repo: GitAutograderRepo) -> GitAutograderOutput:
    if not repo.remotes.has_remote("upstream"):
        raise repo.wrong_answer([MISSING_UPSTREAM_REMOTE])

    upstream = repo.remotes.remote("upstream")
    if not upstream.remote.url.startswith("https://github.com/git-mastery/link-me"):
        raise repo.wrong_answer([WRONG_UPSTREAM_URL])

    return repo.to_output(
        ["Great work with using git remote to add an upstream remote!"],
        GitAutograderStatus.SUCCESSFUL,
    )
