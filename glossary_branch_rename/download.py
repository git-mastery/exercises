import os
import shutil
from pathlib import Path

from exercise_utils.cli import run_command
from exercise_utils.github_cli import clone_repo_with_gh, fork_repo, get_github_username
from exercise_utils.git import add_remote
from exercise_utils.gitmastery import create_start_tag

__resources__ = {}


def setup(verbose: bool = False):
    upstream_repo = "git-mastery/samplerepo-funny-glossary"

    repo_dir = Path.cwd()
    parent_dir = repo_dir.parent
    repo_name = repo_dir.name

    os.chdir(parent_dir)
    if repo_dir.exists():
        shutil.rmtree(repo_dir)

    username = get_github_username(verbose)
    assert username is not None
    fork_name = f"{username}-gitmastery-samplerepo-funny-glossary"

    fork_repo(upstream_repo, fork_name, verbose, default_branch_only=False)
    clone_repo_with_gh(f"{username}/{fork_name}", verbose, name=repo_name)

    os.chdir(parent_dir / repo_name)
    add_remote("upstream", f"https://github.com/{upstream_repo}.git", verbose)
    run_command(["git", "fetch", "upstream", "--prune"], verbose)
    run_command(["git", "push", "origin", "--all"], verbose)

    create_start_tag(verbose)
