from exercise_utils.cli import run_command
from exercise_utils.git import tag

def setup(verbose: bool = False):
    run_command(["git", "remote", "rename", "origin", "production"], verbose)
    tag("beta", verbose)
    run_command(["git", "push", "production", "--tags"], verbose)
    run_command(["git", "tag", "-d", "beta"], verbose)

    run_command(["git", "tag", "v1.0", "HEAD~4"], verbose)
    run_command(["git", "tag", "-a", "v2.0", "HEAD~1", "-m", "First stable roster"], verbose)
