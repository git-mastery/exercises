from sys import exit

from exercise_utils.cli import run_command
from exercise_utils.git import checkout, merge_with_message


def commit(
    author: str,
    email: str,
    date: str,
    message: str,
    verbose: bool,
) -> None:
    run_command(
        [
            "git",
            "commit",
            "--allow-empty",
            "--date",
            date,
            "--author",
            f"{author} <{email}>",
            "-m",
            message,
        ],
        verbose,
    )


def replace_sha_in_file(verbose: bool = False):
    # Get a list of commit SHAs (most recent first)
    log_output = run_command(
        ["git", "log", "--pretty=format:%H"],
        verbose,
    )
    assert log_output is not None

    commits = log_output.strip().splitlines()
    if not commits or len(commits) < 2:
        print("Not enough commits to choose from.")
        exit(1)

    # Exclude the very first commit (the root commit)
    commits_without_root = commits[1:10] + commits[11:]

    # Pick one at random
    import random

    chosen_sha = random.choice(commits_without_root)

    if verbose:
        print(f"Chosen commit: {chosen_sha}")

    # Replace {SHA} in answers.txt
    from pathlib import Path

    # We need to go up one level since we're currently in the crime-spree/ folder
    answers_file = Path("../answers.txt")
    if not answers_file.exists():
        print("answers.txt not found.")
        exit(1)

    text = answers_file.read_text()
    text = text.replace("{SHA}", chosen_sha)
    answers_file.write_text(text)

    if verbose:
        print("answers.txt updated.")


ANON = ("Anonymous", "anon@example.com")
CRIMINAL = ("Josh Badur", "josh.badur@example.com")


def setup(verbose: bool = False):
    # Early small crimes
    crimes = [
        "Stole bicycle from Main Street",
        "Pickpocketed wallet at train station",
        "Shoplifted candy from corner store",
        "Broke into car on Elm Street",
        "Graffiti on library wall",
        "Vandalized statue in city park",
        "Spray painted bus stop shelter",
        "Trespassed in restricted area",
        "Robbed Alice Bakersfield",
        "Stole guitar from pawn shop",
    ]

    for i, msg in enumerate(crimes, start=1):
        commit(*ANON, f"2024-01-{i:02d} 08:00", msg, verbose)

    # Branch: the criminal tries to hide crimes
    checkout("rewrite", True, verbose)
    commit(*CRIMINAL, "2024-02-10 10:00", "Rewrite the comments", verbose)
    commit(*CRIMINAL, "2024-02-11 09:00", "Covering my tracks", verbose)
    checkout("main", False, verbose)

    # Escalation of crimes
    more_crimes = [
        "Broke into bakery overnight",
        "Graffiti on police station wall",
        "Stole motorcycle from parking lot",
        "Oh no what have I done",
        "Currently hiding at the abandoned warehouse at docks",
    ]

    for j, msg in enumerate(more_crimes, start=1):
        commit(*ANON, f"2024-03-{j:02d} 07:00", msg, verbose)

    # Merge rewrite branch back, creates a real graph
    merge_with_message("rewrite", False, "Merge branch 'rewrite'", verbose)

    # Add a few final commits after merge
    aftermath = [
        "Police investigation intensifies",
        "Wanted posters distributed",
        "Citywide curfew announced",
    ]
    for k, msg in enumerate(aftermath, start=1):
        commit(*ANON, f"2024-04-{k:02d} 12:00", msg, verbose)

    replace_sha_in_file(verbose)
