# merge-undo

Scenario: You are keeping notes on the characters of a play that you are writing. In the main story line (which is in the `main` branch), you introduced two characters, Rick and Morty. You had two other characters in two separate branches `daughter` and `son-in-law`. Just now, you introduced these two characters to the main story line by merging the two branches to the `main` branch.

```mermaid
gitGraph
    commit id: "Add Rick"
    commit id: "Add morty"
    branch daughter
    branch son-in-law
    checkout daughter
    commit id: "Add Beth"
    checkout son-in-law
    commit id: "Add Jerry"
    checkout main
    commit id: "Mention Morty is grandson"
    merge daughter id: "Introduce Beth"
    merge son-in-law id: "Introduce Jerry"
```

However, now you realise this is premature, and wish to undo that change.

## Task

Undo the merging of branches `son-in-law` and `daughter`.

The result should be as follows:

```mermaid
gitGraph
    commit id: "Add Rick"
    commit id: "Add morty"
    branch daughter
    branch son-in-law
    checkout daughter
    commit id: "Add Beth"
    checkout son-in-law
    commit id: "Add Jerry"
    checkout main
    commit id: "Mention Morty is grandson"
```
