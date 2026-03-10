import json
from pathlib import Path
from typing import Any


def update_config_fields(updates: dict[str, Any]) -> None:
    """
    Update a JSON file using dotted-path keys.

    Example updates:
    {
        "exercise_repo.pr_number": 1,
        "exercise_repo.repo_full_name": "owner/repo",
        "teammate_role": "teammate-bob",
    }
    """
    config_path = Path("../.gitmastery-exercise.json")
    if not config_path.exists():
        raise FileNotFoundError(
            f".gitmastery-exercise.json file not found at {config_path.resolve()}"
        )
    config = json.loads(config_path.read_text())

    for dotted_path, value in updates.items():
        keys = dotted_path.split(".")
        cursor = config

        for key in keys[:-1]:
            if key not in cursor or not isinstance(cursor[key], dict):
                cursor[key] = {}
            cursor = cursor[key]

        cursor[keys[-1]] = value

    config_path.write_text(json.dumps(config, indent=2))

def add_pr_config(pr_number: int, repo_full_name: str) -> None:
    update_config_fields({
        "exercise_repo.pr_number": pr_number,
        "exercise_repo.repo_full_name": repo_full_name,
    })