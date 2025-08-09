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
    description: Optional[str],
    verbose: bool,
) -> None:
    if description is None:
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
    else:
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
                "-m",
                description,
            ],
            verbose,
        )


ANONYMOUS_AUTHOR = "Anonymous"
ANONYMOUS_EMAIL = "anon@example.com"
CRIMINAL_AUTHOR = "Josh Badur"
CRIMINAL_EMAIL = "josh.badur@example.com"


def setup(verbose: bool = False):
    commit(
        ANONYMOUS_AUTHOR,
        ANONYMOUS_EMAIL,
        "2024-01-05 08:00",
        "Stole bicycle from Main Street",
        None,
        verbose,
    )

    commit(
        ANONYMOUS_AUTHOR,
        ANONYMOUS_EMAIL,
        "2024-03-12 14:45",
        "Vandalized statue in city park",
        None,
        verbose,
    )

    commit(
        ANONYMOUS_AUTHOR,
        ANONYMOUS_EMAIL,
        "2024-06-21 22:30",
        "Robbed Alice Bakersfield",
        None,
        verbose,
    )

    commit(
        ANONYMOUS_AUTHOR,
        ANONYMOUS_EMAIL,
        "2024-09-13 03:15",
        "Graffiti on police station wall",
        "Spray painted a giant smiley face over the precinct's main entrance.",
        verbose,
    )

    commit(
        CRIMINAL_AUTHOR,
        CRIMINAL_EMAIL,
        "2024-10-28 09:00",
        "Oh no what have I done",
        None,
        verbose,
    )

    commit(
        ANONYMOUS_AUTHOR,
        ANONYMOUS_EMAIL,
        "2024-11-14 07:00",
        "Currently hiding at the abandoned warehouse at docks",
        None,
        verbose,
    )
