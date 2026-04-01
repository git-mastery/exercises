from pathlib import Path

from exercise_utils.exercise_config import add_pr_config
from exercise_utils.gitmastery import create_start_tag

def setup(verbose: bool = False):
    create_start_tag(verbose)
    add_pr_config(pr_repo_full_name="git-mastery/gm-languages", config_path=Path("../"))