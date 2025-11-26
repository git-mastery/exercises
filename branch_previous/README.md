# branch-previous

You are writing the outline for a story, in `story.txt`. You have written the first few steps of the storyline. You are not very happy with the way the story is progressing, and wish to explore a few alternative storylines starting from a previous step.

## Task

1. Start a new branch named `visitor-line`, starting from the second commit (i.e., commit with message "Describe location").
2. Add the line `I heard someone knocking at the door.` to the `story.txt`.
3. Commit the change. You may use any suitable commit message.
4. Start a new branch named `sleep-line`, starting from the same starting point as before.
5. Add the line `I fell asleep on the couch.` to the `story.txt`.
6. Commit the change. You may use any suitable commit message.

## Hints

<details>
<summary>How do I create a branch from a specific commit?</summary>

You can create a branch from a specific commit using:
```bash
git branch <branch-name> <commit-hash>
```

Or you can checkout directly to a new branch from a specific commit:
```bash
git checkout -b <branch-name> <commit-hash>
```
</details>

<details>
<summary>How do I find the commit hash?</summary>

Use `git log` to view the commit history and find the hash of the commit with message "Describe location".
</details>
