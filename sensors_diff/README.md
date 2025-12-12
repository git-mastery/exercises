# sensors-diff

A system is using Git to record data received daily from for sensors, each monitoring one of directions east, west, north, south. Each sensor provides 20 integer values, which are stored in a csv file (e.g., values from the sensor monitoring the east direction are recorded as `east.csv`). Data for each day is recorded as one commit.

## Task

Examine the revision history to answer the questions in `answers.txt`.

## Hints

<details>
<summary>How do I see what's staged vs unstaged?</summary>

Use `git status` to see which files are staged and which are modified but unstaged.

</details>
