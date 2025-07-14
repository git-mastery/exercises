# ignoring-somethings

You have stumbled upon a repository with an existing `.gitignore`. However, you
have discovered that the `.gitignore` is not as accurate as you would like it to
be.

Some files are showing up when they should be hidden, and some files are hidden
when they should be present.

## Task

1. While you wish to continue ignoring every file in the `many/` folder, you 
    want to un-ignore just `many/file22.txt`
2. `why_am_i_hidden.txt` should not be hidden
3. `ignore_me.txt` should be hidden
4. Hide the `runaway.txt` file in `this/`, however, you don't know how many 
    layers of nesting it is under, so use the pattern matching syntax
