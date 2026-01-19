from exercise_utils.cli import run_command, run_command_no_exit
from exercise_utils.github_cli import fork_repo, get_github_username
from exercise_utils.git import add_remote
from exercise_utils.gitmastery import create_start_tag

__resources__ = {}


def setup(verbose: bool = False):
    upstream_repo = "git-mastery/samplerepo-funny-glossary"

    username = get_github_username(verbose)
    assert username is not None
    fork_name = f"{username}-gitmastery-samplerepo-funny-glossary"

    fork_repo(upstream_repo, fork_name, verbose, default_branch_only=False)

    fork_url = f"https://github.com/{username}/{fork_name}.git"
    origin_url = run_command_no_exit(["git", "remote", "get-url", "origin"], verbose)
    if origin_url is None:
        add_remote("origin", fork_url, verbose)
    else:
        run_command(["git", "remote", "set-url", "origin", fork_url], verbose)

    upstream_url = f"https://github.com/{upstream_repo}.git"
    existing_upstream = run_command_no_exit(
        ["git", "remote", "get-url", "upstream"], verbose
    )
    if existing_upstream is None:
        add_remote("upstream", upstream_url, verbose)
    else:
        run_command(["git", "remote", "set-url", "upstream", upstream_url], verbose)
    run_command(["git", "fetch", "upstream", "--prune"], verbose)

    branch_list = run_command(
        [
            "git",
            "for-each-ref",
            "refs/remotes/upstream",
            "--format=%(refname:strip=3)",
        ],
        verbose,
    )
    if branch_list:
        for branch in branch_list.splitlines():
            if branch == "HEAD":
                continue
            run_command(["git", "branch", "-f", branch, f"upstream/{branch}"], verbose)

    if run_command_no_exit(
        ["git", "show-ref", "--verify", "refs/remotes/upstream/main"],
        verbose,
    ):
        run_command(["git", "checkout", "-B", "main", "upstream/main"], verbose)

    run_command(["git", "push", "origin", "--all"], verbose)
