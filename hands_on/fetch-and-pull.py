import os
from exercise_utils.cli import run_command

__requires_git__ = True
__requires_github__ = False

def download(verbose: bool):
    """
    Sets up the fetch-and-pull hands-on exercise sandbox.
    Prepares the gm-shapes repo and README for the student.
    """

    # Create the main exercise folder
    os.makedirs("fetch-and-pull", exist_ok=True)

    # Create README.md with exercise instructions
    readme_content = """# fetch-and-pull

## Task

You have been given a clone of the `git-mastery/gm-shapes` repo.

Another developer Alice's has created a remote copy of this repo at <https://github.com/git-mastery/gm-shapes-alice> which seems to have an additional commit in the `main` branch.

Add that repo as a remote titled `alice-upstream`, and bring over Alice's additional commit to your repo.

Alice's friend Bob has copied Alice's repo to <https://github.com/git-mastery/gm-shapes-bob>, and added one more commit.

Add that repo as another remote titled `bob-remote`, and fetch (not pull or merge) his new commit to your repo.
"""

    os.chdir("fetch-and-pull")

    # Clone the base repo gm-shapes into the exercise folder
    run_command([
        "git",
        "clone",
        "https://github.com/git-mastery/gm-shapes.git"
    ], verbose)
