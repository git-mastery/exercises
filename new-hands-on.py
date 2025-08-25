import json
import os
import pathlib
import sys
import textwrap
from dataclasses import dataclass
from typing import Dict, List, Literal, Optional


@dataclass
class HandsOnConfig:
    hands_on_name: str
    requires_git: bool
    requires_github: bool


def confirm(prompt: str, default: bool) -> bool:
    str_result = input(f"{prompt} (defaults to {'y' if default else 'N'})  [y/N]: ")
    bool_value = default if str_result.strip() == "" else str_result.lower() == "y"
    return bool_value


def prompt(prompt: str, default: str) -> str:
    str_result = input(f"{prompt} (defaults to '{default}'): ")
    if str_result.strip() == "":
        return default
    return str_result.strip()


def get_exercise_config() -> HandsOnConfig:
    hands_on_name = input("Hands-on name: ")
    requires_git = confirm("Requires Git?", True)
    requires_github = confirm("Requires Github?", True)

    return HandsOnConfig(
        hands_on_name=hands_on_name,
        requires_git=requires_git,
        requires_github=requires_github,
    )


def create_download_py_file(config: HandsOnConfig) -> None:
    with open(f"{config.hands_on_name}.py", "w") as download_script_file:
        download_script = f"""
        import subprocess
        from sys import exit
        from typing import List, Optional

        __requires_git__ = {config.requires_git}
        __requires_github__ = {config.requires_github}


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


        def download(verbose: bool):
            pass
        """
        download_script_file.write(textwrap.dedent(download_script).lstrip())


def main():
    config = get_exercise_config()
    os.chdir("hands_on")
    create_download_py_file(config)


if __name__ == "__main__":
    main()
