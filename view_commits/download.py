from exercise_utils.cli import run_command
from exercise_utils.file import append_to_file, create_or_update_file
from exercise_utils.gitmastery import create_start_tag

def setup(verbose: bool = False):
    create_start_tag(verbose)
    
    
