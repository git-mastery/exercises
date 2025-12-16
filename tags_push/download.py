from exercise_utils.cli import run_command
from exercise_utils.git import tag, tag_with_options


def setup(verbose: bool = False):
    run_command(["git", "remote", "rename", "origin", "production"], verbose)
    tag("beta", verbose)
    run_command(["git", "push", "production", "--tags"], verbose)
    run_command(["git", "tag", "-d", "beta"], verbose)

    tag_with_options("v1.0", ["HEAD~4"], verbose)
    tag_with_options("v2.0", ["-a", "HEAD~1", "-m", "First stable roster"], verbose)
