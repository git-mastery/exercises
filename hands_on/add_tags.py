from exercise_utils.cli import run_command

__requires_git__ = True
__requires_github__ = True

WORKING_REPO = "samplerepo-preferences"


def download(verbose: bool):
    run_command(["gh", "repo", "fork", f"git-mastery/{WORKING_REPO}",
                 "--clone"], verbose)
