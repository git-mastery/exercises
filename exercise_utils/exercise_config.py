# exercise_utils/json_config.py
import json
from pathlib import Path
from typing import Any


def update_json_fields(config_path: Path, updates: dict[str, Any]) -> None:
    """
    Update a JSON file using dotted-path keys.

    Example updates:
    {
        "exercise_repo.pr_number": 1,
        "exercise_repo.repo_full_name": "owner/repo",
        "teammate_role": "teammate-bob",
    }
    """
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
