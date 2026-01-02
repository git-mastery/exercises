# Script to verify that all exercise configurations are compliant with the expected format
import json
import os
import pathlib
import subprocess
import sys
from dataclasses import dataclass
from typing import List, Set

# List of exercises to exempt, maybe because these have not been updated or are deprecated exercises
EXEMPTION_LIST: Set[str] = set()


@dataclass
class ValidationIssue:
    dir_name: str
    issue: str


def main() -> None:
    issues: List[ValidationIssue] = []
    for dir in os.listdir("."):
        if dir in EXEMPTION_LIST or not os.path.isfile(
            pathlib.Path(dir) / ".gitmastery-exercise.json"
        ):
            continue
        config = {}
        with open(pathlib.Path(dir) / ".gitmastery-exercise.json", "r") as config_file:
            config = json.loads(config_file.read())

            if config["exercise_name"].strip() == "":
                issues.append(
                    ValidationIssue(dir, "Empty exercise_name is not permitted")
                )

            if config.get("exercise_repo", {}).get(
                "repo_type", "local"
            ) == "remote" and not config.get("requires_github", False):
                issues.append(
                    ValidationIssue(
                        dir,
                        "Cannot use 'remote' repo_type if require_github is disabled",
                    )
                )

            if (
                config.get("exercise_repo", {}).get("repo_type", "local") == "local"
                and not config.get("requires_git", False)
                and config.get("exercise_repo", {}).get("init", False)
            ):
                issues.append(
                    ValidationIssue(
                        dir,
                        "Cannot use 'local' repo_type with init: true if require_git is disabled",
                    )
                )

            if (
                config.get("exercise_repo", {}).get("repo_type", "local") == "remote"
                and subprocess.call(
                    [
                        "git",
                        "ls-remote",
                        f"https://github.com/git-mastery/{config['exercise_repo']['repo_title']}",
                        "--quiet",
                    ]
                )
                != 0
            ):
                issues.append(
                    ValidationIssue(
                        dir, "Missing Github repository to fetch for remote exercise"
                    )
                )

            for file in config["base_files"].keys():
                if not os.path.isfile(pathlib.Path(dir) / "res" / file):
                    issues.append(
                        ValidationIssue(dir, f"Missing file {file} from res/")
                    )

    if len(issues) > 0:
        for issue in issues:
            print(f"- {issue.dir_name}: {issue.issue}")
        sys.exit(1)


if __name__ == "__main__":
    main()
