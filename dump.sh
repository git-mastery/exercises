#!/usr/bin/env bash

BASE_COMMIT="086fffb"

git diff --numstat "$BASE_COMMIT"..HEAD |
  awk '
{
    added = $1
    removed = $2
    path = $3

    split(path, parts, "/")
    folder = parts[1]

    if (folder != "exercises_utils") {
        delta = (removed - added)
        diff[folder] += delta
        total += delta
    }
}
END {
    for (f in diff) {
        printf "%s: %d\n", f, diff[f]
    }
    printf "TOTAL: %d\n", total
}
' |
  sort -t: -k2,2nr
