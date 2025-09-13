"""Git-Mastery specific exercise utility."""

from exercise_utils.cli import run_command


def create_start_tag(verbose: bool):
    """Creates a Git-Mastery start tag."""
    commits_str = run_command(
        ["git", "log", "--reverse", "--pretty=format:%h"], verbose
    )
    assert commits_str is not None
    first_commit = commits_str.split("\n")[0]
    tag_name = f"git-mastery-start-{first_commit}"
    run_command(["git", "tag", tag_name], verbose)
