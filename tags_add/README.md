# tags-add

1. Add a **lightweight** tag `first-pilot` to the **first commit**.
2. Add an **annotated** tag `v1.0` to the commit that updates March duty roster, with message `first full duty roster`.

## Task

This exercise clones `git-mastery/gm-duty-roster` into the `duty-roster/` folder.

## Hints

```bash
# first commit
git rev-list --max-parents=0 HEAD

# add lightweight tag
git tag first-pilot <FIRST_COMMIT_SHA>

# find the commit for "Update roster for March"
git log --oneline | grep -i "Update roster for March"

# add annotated tag with message
git tag -a v1.0 -m "first full duty roster" <MARCH_COMMIT_SHA>