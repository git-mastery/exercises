from exercise_utils.cli import run_command
from exercise_utils.git import tag, push
from exercise_utils.gitmastery import create_start_tag

__resources__ = {}

REMOTE_NAME = "production"
TAG_1_NAME = "v1.0"
TAG_2_NAME = "v2.0"
TAG_DELETE_NAME = "beta"
TAG_2_MESSAGE = "First stable roster"

def setup(verbose: bool = False):
    create_start_tag(verbose)
    run_command(["git", "remote", "rename", "origin", REMOTE_NAME], verbose)
    tag(TAG_DELETE_NAME, verbose)
    push(REMOTE_NAME, "--tags", verbose) # somewhat hacky, maybe use run_command instead
    run_command(["git", "tag", "-d", TAG_DELETE_NAME], verbose)

    run_command(["git", "tag", TAG_1_NAME, "HEAD~4"], verbose)
    run_command(["git", "tag", "-a", TAG_2_NAME, "HEAD~1", "-m", f"\"{TAG_2_MESSAGE}\""], verbose)
