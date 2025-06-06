#!/bin/bash

first_commit_hash=$(git log --reverse --pretty=format:'%h' | head -n 1)
if [ $(git tag -l "git-mastery-start-$first_commit_hash") ]; then
  git tag -d "git-mastery-start-$first_commit_hash"
fi

git tag "git-mastery-start-$first_commit_hash"
