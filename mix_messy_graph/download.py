from exercise_utils.git import merge, merge_with_message, track_remote_branch


def setup(verbose: bool = False):
    remote_name = "origin"
    remote_branches = ["feature-search", "feature-delete", "list"]
    for remote_branch_name in remote_branches:
        track_remote_branch(remote_name, remote_branch_name, verbose)

    merge_with_message("feature-search", False, "Merge search feature", verbose)
