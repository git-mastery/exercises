import subprocess
from sys import exit
from typing import List, Optional


def run_command(command: List[str], verbose: bool) -> Optional[str]:
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=True,
        )
        if verbose:
            print(result.stdout)
        return result.stdout
    except subprocess.CalledProcessError as e:
        if verbose:
            print(e.stderr)
        exit(1)


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
    run_command(["git", "checkout", "-b", "rewrite"], verbose)
    commit(*CRIMINAL, "2024-02-10 10:00", "Rewrite the comments", verbose)
    commit(*CRIMINAL, "2024-02-11 09:00", "Covering my tracks", verbose)
    run_command(["git", "checkout", "main"], verbose)

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
    run_command(
        ["git", "merge", "--no-ff", "rewrite", "-m", "Merge branch 'rewrite'"], verbose
    )

    # Add a few final commits after merge
    aftermath = [
        "Police investigation intensifies",
        "Wanted posters distributed",
        "Citywide curfew announced",
    ]
    for k, msg in enumerate(aftermath, start=1):
        commit(*ANON, f"2024-04-{k:02d} 12:00", msg, verbose)
