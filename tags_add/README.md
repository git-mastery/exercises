# tags-add

The `duty-roster` repo contains text files that track which people are assigned for duties on which days of the week.

## Task

1. Add a lightweight tag `first-pilot` to the first commit of the repo.

2. Add the annotated tag `v1.0` to the commit that updates March duty roster. The tag should have the message `first full duty roster`.

## Hints

<details>
<summary>💡 Hint 1</summary>

```bash
# add lightweight tag
git tag first-pilot <FIRST_COMMIT_SHA>
```

</details>

<summary>💡 Hint 2</summary>

```bash
# add annotated tag with message
git tag -a v1.0 -m "first full duty roster" <MARCH_COMMIT_SHA>
```

</details>
