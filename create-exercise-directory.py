import json
import os
from collections import defaultdict

OUTPUT_FILE = "exercise-directory.md"


def find_config_files(base_dir="."):
    config_files = []
    for entry in os.listdir(base_dir):
        full_path = os.path.join(base_dir, entry)
        if os.path.isdir(full_path):
            config_path = os.path.join(full_path, ".gitmastery-exercise.json")
            if os.path.isfile(config_path):
                config_files.append(config_path)
    return config_files


def parse_configs(config_files):
    configs = []
    for path in config_files:
        try:
            with open(path, "r") as f:
                data = json.load(f)
            configs.append(data)
        except Exception as e:
            print(f"Error reading {path}: {e}")
    return configs


def generate_tag_map(configs):
    tag_map = defaultdict(list)

    for config in configs:
        exercise_name = config.get("exercise_name")
        tags = config.get("tags", [])
        for tag in set(tags):
            tag_map[tag].append((exercise_name, f"gitmastery download {exercise_name}"))
    return tag_map


def generate_markdown(tag_map):
    lines = []
    for tag in sorted(tag_map):
        lines.append(f"# {tag}\n")
        lines.append("| Exercise | Download Command |")
        lines.append("|----------|------------------|")
        for name, command in tag_map[tag]:
            lines.append(
                f"| [{name}](https://git-mastery.github.io/exercises/{name.replace('-', '_')}) | `{command}` |"
            )
        lines.append("")  # blank line between sections
    return "\n".join(lines)


def main():
    config_files = find_config_files()
    configs = parse_configs(config_files)
    tag_map = generate_tag_map(configs)
    markdown = generate_markdown(tag_map)

    with open(OUTPUT_FILE, "w") as f:
        f.write(markdown)
    with open("exercises.json", "w") as of:
        of.write(json.dumps(configs, indent=2))
    print(f"Generated {OUTPUT_FILE} with {len(tag_map)} tags.")


if __name__ == "__main__":
    main()
