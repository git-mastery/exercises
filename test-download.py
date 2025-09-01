import json
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict


def get_username() -> str:
    result = subprocess.run(
        ["gh", "api", "user", "-q", ".login"], capture_output=True, text=True
    )

    if result.returncode == 0:
        username = result.stdout.splitlines()[0]
        return username
    return ""


def has_fork(fork_name: str) -> bool:
    result = subprocess.run(
        ["gh", "repo", "view", fork_name, "--json", "isFork", "--jq", ".isFork"],
        capture_output=True,
        text=True,
        env=dict(os.environ, **{"GH_PAGER": "cat"}),
    )
    return result.returncode == 0 and result.stdout.strip() == "true"


def fork(repository_name: str, fork_name: str) -> None:
    subprocess.run(
        [
            "gh",
            "repo",
            "fork",
            repository_name,
            "--default-branch-only",
            "--fork-name",
            fork_name,
        ],
        capture_output=True,
        text=True,
    )


def clone_with_custom_name(repository_name: str, name: str) -> None:
    subprocess.run(
        ["gh", "repo", "clone", repository_name, name], capture_output=True, text=True
    )


def init() -> None:
    subprocess.run(
        ["git", "init", "--initial-branch=main"], capture_output=True, text=True
    )


def add_all() -> None:
    subprocess.run(["git", "add", "."], capture_output=True, text=True)


def commit(message: str) -> None:
    subprocess.run(["git", "commit", "-m", message], capture_output=True, text=True)


def empty_commit(message: str) -> None:
    subprocess.run(
        ["git", "commit", "-m", message, "--allow-empty"],
        capture_output=True,
        text=True,
    )


def delete_repo(repository_name: str) -> None:
    subprocess.run(
        ["gh", "repo", "delete", repository_name, "--yes"],
        capture_output=True,
        text=True,
    )


def download_exercise(exercise_folder_name: str) -> None:
    os.makedirs("test-downloads", exist_ok=True)
    test_folder_name = os.path.join("test-downloads", exercise_folder_name)
    shutil.rmtree(test_folder_name, ignore_errors=True)
    os.makedirs(test_folder_name, exist_ok=True)

    starting_files = [".gitmastery-exercise.json", "README.md"]
    for file in starting_files:
        shutil.copyfile(
            os.path.join(exercise_folder_name, file),
            os.path.join(test_folder_name, file),
        )

    config = {}
    with open(
        os.path.join(exercise_folder_name, ".gitmastery-exercise.json"), "r"
    ) as exercise_config_file:
        config = json.load(exercise_config_file)

    base_files = config["base_files"]
    for resource, path in base_files.items():
        os.makedirs(Path(path).parent, exist_ok=True)
        shutil.copyfile(
            os.path.join(exercise_folder_name, "res", resource),
            os.path.join(test_folder_name, path),
        )

    repo_name = config["exercise_repo"]["repo_name"]
    repo_title = config["exercise_repo"]["repo_title"]
    repo_type = config["exercise_repo"]["repo_type"]
    if repo_type == "local":
        os.makedirs(os.path.join(test_folder_name, repo_name), exist_ok=True)
    elif repo_type == "remote":
        username = get_username()
        exercise_repo = f"git-mastery/{repo_title}"
        if config["exercise_repo"]["create_fork"]:
            fork_name = f"{username}-gitmastery-{repo_title}"
            if has_fork(fork_name):
                delete_repo(fork_name)
            fork(exercise_repo, fork_name)
            cur_dir = os.getcwd()
            os.chdir(os.path.join(test_folder_name))
            clone_with_custom_name(f"{username}/{fork_name}", repo_name)
            os.chdir(cur_dir)
        else:
            cur_dir = os.getcwd()
            os.chdir(os.path.join(test_folder_name))
            clone_with_custom_name(exercise_repo, repo_name)
            os.chdir(cur_dir)

    if repo_type != "ignore":
        namespace: Dict[str, Any] = {}
        with open(
            os.path.join(exercise_folder_name, "download.py"), "r"
        ) as download_script_file:
            contents = download_script_file.read()
            exec(contents, namespace)

        download_resources = namespace.get("__resources__", {})
        if download_resources:
            for resource, path in download_resources.items():
                os.makedirs(Path(path).parent, exist_ok=True)
                shutil.copyfile(
                    os.path.join(exercise_folder_name, "res", resource),
                    os.path.join(test_folder_name, repo_name, path),
                )

        os.chdir(os.path.join(test_folder_name, repo_name))
        if config["exercise_repo"]["init"]:
            init()
            initial_commit_message = "Set initial state"
            if download_resources:
                add_all()
                commit(initial_commit_message)
            else:
                empty_commit(initial_commit_message)

        if "setup" in namespace:
            namespace["setup"]()


def download_hands_on(hands_on_folder_name: str) -> None:
    os.makedirs("test-downloads", exist_ok=True)
    hands_on_folder = f"hp-{hands_on_folder_name.replace('_', '-')}"
    test_folder_name = os.path.join("test-downloads", hands_on_folder)
    shutil.rmtree(test_folder_name, ignore_errors=True)
    os.makedirs(test_folder_name, exist_ok=True)

    namespace: Dict[str, Any] = {}
    with open(
        os.path.join("hands_on", f"{hands_on_folder_name}.py"), "r"
    ) as download_script_file:
        contents = download_script_file.read()
        exec(contents, namespace)

    if "download" in namespace:
        os.chdir(test_folder_name)
        namespace["download"](False)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(
            "Missing exercise/hands-on folder name: ./test-download.py <exercise/hands-on folder name>"
        )
        sys.exit(1)

    arg = sys.argv[1]
    arg = arg.replace("-", "_")

    if arg.startswith("hp_"):
        if not os.path.isfile(os.path.join("hands_on", f"{arg[3:]}.py")):
            print("Invalid hands-on folder name")
            sys.exit(1)
        download_hands_on(arg[3:])
    else:
        if not os.path.isdir(arg):
            print("Invalid exercise folder name")
            sys.exit(1)
        download_exercise(arg)
