# nothing-to-hide

You are the IT specialist in your department and you've been noticing some strange files show up on your machine but nothing shows up on Git.

You suspect that someone has been tampering with your files and want to investigate what's going on and identify what's causing the files from disappearing.

## Task

You should have a set of files available in your local repository. Use your file explorer or terminal to explore the files and all sub-folders.

> [!NOTE]  
> Leave `.git/`, `.github/`, `README.md`, `post-download.sh`, and `submit.sh` alone! They are not a part of this problem set.

### Task 1

Use tools like `git status -u` to find the files that are missing from Git but are still found on your local repository.

In `answers.txt`, list them out as follows:

```text
Q: What files are missing from Git, but found on your local repository?
A:
- filea.txt
- fileb.txt
...
```

### Task 2

Continue poking around the repository, what is responsible for causing the files to disappear?

Answer in `answers.txt`:

```text
Q: What is responsible for the hidden files?
A: ...
```

### Task 3

What is the general pattern used to hide the `senstive/` folder?

Answer in `answers.txt`:

```text
Q: What is the general pattern used to hide the sensitive/ folder?
A: ...
```

### Task 4

What is the pattern used to only show `sensitive/names.txt`?

Answer in `answers.txt`:

```text
Q: What is the pattern used to only show sensitive/names.txt?
A: ...
```
