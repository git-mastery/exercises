import os
from exercise_utils.cli import run_command
from exercise_utils.git import tag_with_options, annotated_tag_with_options

__requires_git__ = True
__requires_github__ = True

REPO_NAME = "samplerepo-preferences"


def download(verbose: bool):

    run_command(["gh", "repo", "fork", f"git-mastery/{REPO_NAME}", REPO_NAME, "--clone"],
                verbose)

    os.chdir(REPO_NAME)

    tag_with_options("v1.0", ["HEAD~1"], verbose)
    annotated_tag_with_options("v0.9", ["HEAD~2", "-m", "First beta release"], verbose)

    pass
