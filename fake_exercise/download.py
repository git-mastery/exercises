from exercise_utils.cli import run_command
from exercise_utils.gitmastery import create_start_tag

__resources__ = {}


def setup(verbose: bool = False):
    create_start_tag(verbose)
