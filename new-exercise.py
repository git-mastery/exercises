#!/usr/bin/python3

import json
import os
import pathlib
import textwrap


def main():
    exercise_name = input("Exercise name: ")
    tags_str = input("Tags (space separated): ")
    tags = [] if tags_str.strip() == "" else tags_str.split(" ")
    requires_repo_str = input("Requires repo? (defaults to y) y/N: ")
    requires_repo = (
        requires_repo_str.strip() == ""
        or requires_repo_str == "y"
        or requires_repo_str == "Y"
    )

    cur_path = pathlib.Path(os.getcwd())
    exercise_dir_name = exercise_name.replace("-", "_")
    exercise_dir = cur_path / exercise_dir_name
    os.makedirs(exercise_dir)
    with open(exercise_dir / ".gitmastery-exercise.json", "w") as exercise_config_file:
        exercise_config = {
            "exercise_name": exercise_name,
            "tags": tags,
            "is_downloadable": True,
            "requires_repo": requires_repo,
            "resources": {},
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

    # TODO: conditionally add the git tagging only when requires_repo is True
    with open(exercise_dir / "download.py", "w") as download_script_file:
        download_script = """
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


        def setup(verbose: bool = False):
            commits_str = run_command(
                ["git", "log", "--reverse", "--pretty=format:%h"], verbose
            )
            assert commits_str is not None
            first_commit = commits_str.split('\n')[0]
            tag_name = f"git-mastery-start-{first_commit}"
            run_command(["git", "tag", tag_name], verbose)
        """
        download_script_file.write(textwrap.dedent(download_script).lstrip())

    os.makedirs(exercise_dir / "res", exist_ok=True)

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
