from exercise_utils.git import (
    merge_with_message,
    remove_remote,
    track_remote_branch,
)


def setup(verbose: bool = False):
    remote_name = "origin"
    remote_branches = ["feature-search", "feature-delete", "list"]
    for remote_branch_name in remote_branches:
        track_remote_branch(remote_name, remote_branch_name, verbose)
    remove_remote("origin", verbose)

    merge_with_message("feature-search", False, "Merge search feature", verbose)
