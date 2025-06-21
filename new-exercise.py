import json
import os
import pathlib
import sys
import textwrap
from dataclasses import dataclass
from typing import Dict, List, Literal, Optional


@dataclass
class ExerciseConfig:
    @dataclass
    class ExerciseRepoConfig:
        repo_type: Literal["local", "remote"]
        repo_name: str
        repo_title: Optional[str]
        create_fork: Optional[bool]
        init: Optional[bool]

    exercise_name: str
    tags: List[str]
    requires_git: bool
    requires_github: bool
    base_files: Dict[str, str]
    exercise_repo: ExerciseRepoConfig

    def to_json(self) -> str:
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=False, indent=2)

    @property
    def exercise_dir(self) -> pathlib.Path:
        cur_path = pathlib.Path(os.getcwd())
        exercise_dir_name = self.exercise_name.replace("-", "_")
        exercise_dir = cur_path / exercise_dir_name
        return exercise_dir


def confirm(prompt: str, default: bool) -> bool:
    str_result = input(f"{prompt} (defaults to {'y' if default else 'N'})  [y/N]: ")
    bool_value = default if str_result.strip() == "" else str_result.lower() == "y"
    return bool_value


def prompt(prompt: str, default: str) -> str:
    str_result = input(f"{prompt} (defaults to '{default}'): ")
    if str_result.strip() == "":
        return default
    return str_result.strip()


def get_exercise_config() -> ExerciseConfig:
    exercise_name = input("Exercise name: ")
    tags_str = input("Tags (space separated): ")
    tags = [] if tags_str.strip() == "" else tags_str.split(" ")
    requires_git = confirm("Requires Git?", True)
    requires_github = confirm("Requires Github?", True)
    exercise_repo_type = prompt("Exercise repo type (local or remote)", "local").lower()

    if exercise_repo_type != "local" and exercise_repo_type != "remote":
        print("Invalid exercise_repo_type, only local and remote allowed")
        sys.exit(1)

    exercise_repo_name = prompt("Exercise repo name", exercise_name.replace("-", "_"))

    init: Optional[bool] = None
    create_fork: Optional[bool] = None
    repo_title: Optional[str] = None
    if exercise_repo_type == "local":
        init = confirm("Initialize exercise repo as Git repository?", True)
    elif exercise_repo_type == "remote":
        repo_title = prompt("Git-Mastery Github repository title", "")
        create_fork = confirm("Create fork of repository?", True)
    return ExerciseConfig(
        exercise_name=exercise_name,
        tags=tags,
        requires_git=requires_git,
        requires_github=requires_github,
        base_files={},
        exercise_repo=ExerciseConfig.ExerciseRepoConfig(
            repo_type=exercise_repo_type,  # type: ignore
            repo_name=exercise_repo_name,
            repo_title=repo_title,
            create_fork=create_fork,
            init=init,
        ),
    )


def create_exercise_config_file(config: ExerciseConfig) -> None:
    with open(".gitmastery-exercise.json", "w") as exercise_config_file:
        exercise_config_file.write(config.to_json())


def create_readme_file(config: ExerciseConfig) -> None:
    with open("README.md", "w") as readme_file:
        readme = f"""
        # {config.exercise_name}

        <!--- Insert exercise description -->

        ## Task

        <!--- Insert exercise task, simplify what needs to be done -->

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


def create_download_py_file() -> None:
    # TODO: conditionally add the git tagging only when requires_repo is True
    with open("download.py", "w") as download_script_file:
        download_script = """
        import subprocess
        from sys import exit
        from typing import List, Optional

        __resources__ = {}


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
            first_commit = commits_str.split("\\n")[0]
            tag_name = f"git-mastery-start-{first_commit}"
            run_command(["git", "tag", tag_name], verbose)
        """
        download_script_file.write(textwrap.dedent(download_script).lstrip())


def create_verify_py_file() -> None:
    with open("verify.py", "w") as verify_script_file:
        verify_script = """
        from git_autograder import GitAutograderOutput, GitAutograderExercise


        def verify(exercise: GitAutograderExercise) -> GitAutograderOutput:
            # INSERT YOUR GRADING CODE HERE

            return exercise.to_output([])
        """
        verify_script_file.write(textwrap.dedent(verify_script).lstrip())


def create_init_py_file() -> None:
    open("__init__.py", "a").close()


def create_test_dir(config: ExerciseConfig) -> None:
    tests_dir = "tests"
    os.makedirs(tests_dir, exist_ok=True)
    os.chdir(tests_dir)

    create_init_py_file()

    with open("test_verify.py", "w") as test_grade_file:
        test_grade = f"""
        from git_autograder import GitAutograderTestLoader

        from ..verify import verify

        REPOSITORY_NAME = "{config.exercise_name}"

        loader = GitAutograderTestLoader(__file__, REPOSITORY_NAME, verify)


        def test():
            with loader.load("specs/base.yml", "start"):
                pass
        """
        test_grade_file.write(textwrap.dedent(test_grade).lstrip())

    os.makedirs("specs", exist_ok=True)
    with open("specs/base.yml", "w") as base_spec_file:
        base_spec = """
        initialization:
          steps:
            - type: commit
              empty: true
              message: Empty commit
              id: start
        """
        base_spec_file.write(textwrap.dedent(base_spec).lstrip())


def main():
    config = get_exercise_config()
    os.makedirs(config.exercise_dir)
    os.chdir(config.exercise_dir)

    os.makedirs("res", exist_ok=True)
    create_exercise_config_file(config)
    create_readme_file(config)
    create_download_py_file()
    create_verify_py_file()
    create_test_dir(config)


if __name__ == "__main__":
    main()
