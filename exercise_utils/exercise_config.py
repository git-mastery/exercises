import json
from pathlib import Path
from typing import Any


def _merge_config_fields(config: dict[str, Any], updates: dict[str, Any]) -> None:
    for key, value in updates.items():
        if isinstance(value, dict):
            current_value = config.get(key)
            if not isinstance(current_value, dict):
                config[key] = {}
            _merge_config_fields(config[key], value)
            continue

        config[key] = value


def update_config_fields(updates: dict[str, Any]) -> None:
    """
    Update fields in .gitmastery-exercise.json.

    Example updates:
    {
        "exercise_repo": {
            "pr_number": 1,
            "pr_repo_full_name": "owner/repo",
        },
        "teammate": "teammate-bob",
    }
    """
    config_path = Path("../.gitmastery-exercise.json")
    if not config_path.exists():
        raise FileNotFoundError(
            f".gitmastery-exercise.json file not found at {config_path.resolve()}"
        )
    config = json.loads(config_path.read_text())
    _merge_config_fields(config, updates)

    config_path.write_text(json.dumps(config, indent=2))


def add_pr_config(pr_number: int, pr_repo_full_name: str) -> None:
    update_config_fields(
        {
            "exercise_repo": {
                "pr_number": pr_number,
                "pr_repo_full_name": pr_repo_full_name,
            }
        }
    )
