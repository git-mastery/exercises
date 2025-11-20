# ff-undo

This exercise focuses on **undoing a merge in Git**. You will practice how to revert unwanted merge commits while keeping branches and commits intact.

## Task

You have a repository with two branches:

- `main` branch, which initially contains commits:
  - `Add Rick`
  - `Add Morty`
- `others` branch, which contains commits:
  - `Add Birdperson`
  - `Add Cyborg to birdperson.txt`
  - `Add Tammy`

A merge with fast forward from `others` into `main` has been done incorrectly. Your task is:

1. **Undo the merge on `main`**, so that only `Add Rick` and `Add Morty` remain on `main`.
2. Ensure the `others` branch still exists with all its commits intact.
3. Do not delete any commits; only undo the merge on `main`.

## Hints

<details>
<summary>Hint 1: Check your branches</summary>

Use `git branch` to see the current branches and verify `main` and `others` exist.
</details>

<details>
<summary>Hint 2: View commit history</summary>

Use `git log --oneline` on `main` to identify the merge commit that needs to be undone.
</details>

<details>
<summary>Hint 3: Undo the merge</summary>

You can undo a merge using: `git reset --hard <commit-before-merge>`
</details>