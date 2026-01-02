import os
import textwrap
from dataclasses import dataclass


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
    hands_on_name = input("Hands-on name: hp-")
    requires_git = confirm("Requires Git?", True)
    requires_github = confirm("Requires Github?", True)

    return HandsOnConfig(
        hands_on_name=hands_on_name,
        requires_git=requires_git,
        requires_github=requires_github,
    )


def create_download_py_file(config: HandsOnConfig) -> None:
    with open(
        f"{config.hands_on_name.replace('-', '_')}.py", "w"
    ) as download_script_file:
        download_script = f"""
        from exercise_utils.cli import run_command
        from exercise_utils.gitmastery import create_start_tag

        __requires_git__ = {config.requires_git}
        __requires_github__ = {config.requires_github}


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
