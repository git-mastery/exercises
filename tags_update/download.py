from exercise_utils.cli import run_command

__resources__ = {}


def setup(verbose: bool = False):    
    run_command(["git", "tag", "first-update", "HEAD~4"], verbose)
    run_command(["git", "tag", "april-update"], verbose)
    run_command(["git", "tag", "may-update"], verbose)
