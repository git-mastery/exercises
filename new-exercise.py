#!/usr/bin/python3

import json
import os
import pathlib
import textwrap


def main():
    exercise_name = input("Exercise name: ")
    tags = input("Tags (space separated): ").split(" ")
    cur_path = pathlib.Path(os.getcwd())
    exercise_dir = cur_path / exercise_name
    os.makedirs(exercise_dir)
    with open(exercise_dir / ".gitmastery-exercise.json", "w") as exercise_config_file:
        exercise_config = {
            "exercise_name": exercise_name,
            "tags": tags,
            "is_downloadable": True,
        }
        exercise_config_str = json.dumps(exercise_config, indent=2)
        exercise_config_file.write(exercise_config_str)

    with open(exercise_dir / "README.md", "w") as readme_file:
        readme = f"""
        # {exercise_name}

        <!--- Insert exercise description -->

        ## Learning outcomes

        <!--- Insert exercise learning outcomes -->

        ## Task

        <!--- Insert exercise task, simplify what needs to be done -->

        ## Verification

        Run `gitmastery verify` in this exercise folder.

        ## Hints

        <!--- Insert hints here -->
        <!--- 
            Use Github Markdown's collapsible content:
            <details>
            <summary>...</summary>
            ...
            </details>
        -->
        """
        readme_file.write(textwrap.dedent(readme).lstrip())

    with open(exercise_dir / "download.sh", "w") as download_script_file:
        download_script = """
        #!/bin/bash

        # Specify the downloaded behavior
        """
        download_script_file.write(textwrap.dedent(download_script).lstrip())

    os.makedirs(exercise_dir / "res")


if __name__ == "__main__":
    main()
