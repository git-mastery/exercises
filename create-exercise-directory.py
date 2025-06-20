import os
import json
from collections import defaultdict

OUTPUT_FILE = "exercise-directory.md"


def find_config_files(base_dir="."):
    """
    Finds .gitmastery-exercise.json files in 1-level subdirectories.
    """
    config_files = []
    for entry in os.listdir(base_dir):
        full_path = os.path.join(base_dir, entry)
        if os.path.isdir(full_path):
            config_path = os.path.join(full_path, ".gitmastery-exercise.json")
            if os.path.isfile(config_path):
                config_files.append(config_path)
    return config_files


def parse_configs(config_files):
    """
    Parses the config files and returns a dict: tag -> list of (exercise_name, command)
    """
    tag_map = defaultdict(list)

    for path in config_files:
        try:
            with open(path, "r") as f:
                data = json.load(f)
            exercise_name = data.get("exercise_name")
            tags = data.get("tags", [])
            for tag in set(tags):
                tag_map[tag].append(
                    (exercise_name, f"gitmastery download {exercise_name}")
                )
        except Exception as e:
            print(f"Error reading {path}: {e}")
    return tag_map


def generate_markdown(tag_map):
    """
    Generates markdown content grouped by tag.
    """
    lines = []
    for tag in sorted(tag_map):
        lines.append(f"# {tag}\n")
        lines.append("| Exercise | Download Command |")
        lines.append("|----------|------------------|")
        for name, command in tag_map[tag]:
            lines.append(f"| {name} | `{command}` |")
        lines.append("")  # blank line between sections
    return "\n".join(lines)


def main():
    config_files = find_config_files()
    tag_map = parse_configs(config_files)
    markdown = generate_markdown(tag_map)

    with open(OUTPUT_FILE, "w") as f:
        f.write(markdown)
    print(f"Generated {OUTPUT_FILE} with {len(tag_map)} tags.")


if __name__ == "__main__":
    main()
