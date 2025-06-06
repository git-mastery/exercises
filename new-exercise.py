#!/usr/bin/python3

import json
import os
import pathlib
import textwrap


def main():
    exercise_name = input("Exercise name: ")
    tags_str = input("Tags (space separated): ")
    tags = [] if tags_str.strip() == "" else tags_str.split(" ")

    cur_path = pathlib.Path(os.getcwd())
    exercise_dir_name = exercise_name.replace("-", "_")
    exercise_dir = cur_path / exercise_dir_name
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

        first_commit_hash=$(git log --reverse --pretty=format:'%h' | head -n 1)
        if [ $(git tag -l "git-mastery-start-$first_commit_hash") ]; then
          git tag -d "git-mastery-start-$first_commit_hash"
        fi

        git tag "git-mastery-start-$first_commit_hash"
        """
        download_script_file.write(textwrap.dedent(download_script).lstrip())

    with open(exercise_dir / "verify.py", "w") as verify_script_file:
        verify_script = """
        from typing import List

        from git_autograder import GitAutograderOutput, GitAutograderRepo


        def verify(repo: GitAutograderRepo) -> GitAutograderOutput:
            comments: List[str] = []

            # INSERT YOUR GRADING CODE HERE

            return repo.to_output(comments)
        """
        verify_script_file.write(textwrap.dedent(verify_script).lstrip())

    open(exercise_dir / "__init__.py", "a").close()

    os.makedirs(exercise_dir / "res", exist_ok=True)

    tests_dir = exercise_dir / "tests"
    os.makedirs(tests_dir, exist_ok=True)
    open(tests_dir / "__init__.py", "a").close()

    with open(tests_dir / "test_verify.py", "w") as test_grade_file:
        test_grade = f"""
        from git_autograder import GitAutograderTestLoader

        from ..verify import verify

        REPOSITORY_NAME = "{exercise_name}"

        loader = GitAutograderTestLoader(__file__, REPOSITORY_NAME, verify)


        def test():
            with loader.load("specs/base.yml", "start"):
                pass
        """
        test_grade_file.write(textwrap.dedent(test_grade).lstrip())

    os.makedirs(tests_dir / "specs", exist_ok=True)
    with open(tests_dir / "specs" / "base.yml", "w") as base_spec_file:
        base_spec = """
        initialization:
          steps:
            - type: commit
              empty: true
              message: Empty commit
              id: start
        """
        base_spec_file.write(textwrap.dedent(base_spec).lstrip())


if __name__ == "__main__":
    main()
