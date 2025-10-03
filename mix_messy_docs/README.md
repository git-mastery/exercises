# mix-messy-docs

You are writing user documentation for a product. You have already written documentation for a few new features, each in a separate branch. You wish to accumulate this work in a separate branch called `development` until the next product release.

## Task

1. Create a new branch `development`, starting from the commit tagged `v1.0`
2. Merge the `feature-search` branch onto the `development` branch, without using fast-forwarding (i.e., create a merge commit). Delete the `feature-search` branch.
3. Similarly, merge the `feature-delete` branch onto the `development` branch. Resolve any merge conflicts -- in the `features.md`, the delete feature should appear after the search feature (see below). Delete the `feature-delete` branch.
   ```
   # Features

   ## Create Book

   Allows creating one book at a time.

   ## Searching for Books

   Allows searching for books by keywords.
   Works only for book titles.

   ## Deleting Books

   Allows deleting books.
   ```
5. The `list` branch is not yet ready to be merged but rename it as `feature-list`, to be consistent with the naming convention you have been following in this repo.

