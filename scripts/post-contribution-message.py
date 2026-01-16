import os

from github import Github, Auth

GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
PR_NUMBER = os.environ.get("PR_NUMBER")
COMMIT_AUTHOR = os.environ.get("COMMIT_AUTHOR")
FORK_AUTHOR = os.environ.get("FORK_AUTHOR")
FORK_REPO = os.environ.get("FORK_REPO")
FORK_BRANCH = os.environ.get("FORK_BRANCH")

if not all(
    [GITHUB_TOKEN, PR_NUMBER, COMMIT_AUTHOR, FORK_AUTHOR, FORK_REPO, FORK_BRANCH]
):
    raise ValueError("Missing required environment variables")

assert PR_NUMBER is not None
PR_NUMBER_INT = int(PR_NUMBER)

assert GITHUB_TOKEN is not None

auth = Auth.Token(GITHUB_TOKEN)
gh = Github(auth=auth)
repo = gh.get_repo("git-mastery/exercises")
pr = repo.get_pull(PR_NUMBER_INT)

comment = f"""
Hi @{COMMIT_AUTHOR}, thank you for your contribution! 🎉

This PR comes from your fork `{FORK_AUTHOR}/{FORK_REPO}` on branch `{FORK_BRANCH}`.

Before you request for a review, please ensure that you have tested your changes locally!

> [!IMPORTANT]
> The previously recommended way of using `./test-download.py` is no longer the best way to test your changes locally. 
>
> Please read the following instructions for the latest instructions.

### Prerequisites

Ensure that you have the `gitmastery` app installed locally ([instructions](https://git-mastery.github.io/companion-app/index.html))

### Testing steps

If you already have a local Git-Mastery root to test, you can skip the following step.

Create a Git-Mastery root locally:

```bash
gitmastery setup
```

Navigate into the Git-Mastery root (defaults to `gitmastery-exercises/`):

```bash
cd gitmastery-exercises/
```

Edit the `.gitmastery.json` configuration file. You need to set the following values under the `exercises_source` key.

```json
{{
    # other fields...
    "exercises_source": {{
        "username": "{FORK_AUTHOR}",
        "repository": "{FORK_REPO}",
        "branch": "{FORK_BRANCH}"
    }}
}}
```

Then, you can use the `gitmastery` app to download and verify your changes locally.

```bash
gitmastery download <your new change>
gitmastery verify
```

### Checklist

- [ ] (For exercises and hands-ons) I have verified that the downloading behavior works
- [ ] (For exercises only) I have verified that the verification behavior is accurate

> [!IMPORTANT]
> To any reviewers of this pull request, please use the same instructions above to test the changes.
""".lstrip()

pr.create_issue_comment(comment)
