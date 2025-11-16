from pathlib import Path
import shutil
from exercise_utils.github_cli import clone_repo, fork_repo

__requires_git__ = True
__requires_github__ = True

REPO_NAME = "samplerepo-things-force-push"
UPSTREAM_REPO = "git-mastery/samplerepo-things"
WORK_DIR = "things"


def download(verbose: bool):
    work_dir = Path(WORK_DIR)
    if work_dir.exists():
        shutil.rmtree(work_dir)

    fork_repo(UPSTREAM_REPO, REPO_NAME, verbose)
    clone_repo(REPO_NAME, verbose, WORK_DIR)
