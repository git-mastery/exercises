# sensors-checkout

A system is using Git to record data received daily from for sensors, each monitoring one of directions east, west, north, south. Each sensor provides 20 integer values, which are stored in a csv file (e.g., values from the sensor monitoring the east direction are recorded as east.csv). Data for each day is recorded as one commit.

## Task

Traverse the revision history to answer the following questions in `answers.txt`.

## Hints

Tip: You can use the bash command `awk '{s+=$1} END {print s}' south.csv` to find the sum of values in `south.csv` (and so on). Alternatively, you can open the csv file in a spreadsheet program and use a feature of that program to find the sum.
