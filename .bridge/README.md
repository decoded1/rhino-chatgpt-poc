# Rhino ChatGPT Bridge Protocol v0.3

This repository is the laboratory for the controller/operator bridge.

## Roles

- **Controller:** ChatGPT Web
- **Transport:** GitHub / Git
- **Operator:** Codex on the local Mac

## Safety model

`main` is controller-visible stable state. Operator execution occurs on a dedicated task branch:

```text
main
  └── operator/<task-id>
        ├── work commit
        └── report/receipt commit
```

The report records both the `base_commit` and the `result_commit`. The report itself is committed *after* the result commit, which avoids the impossible self-reference of trying to place a commit's own SHA inside itself.

## Directories

- `.bridge/requests/` — controller-created tasks
- `.bridge/reports/` — operator-created task reports
- `.bridge/state/` — measured controller/operator state
- `.bridge/templates/` — protocol examples

A request is pending when a request JSON exists on the current branch and no report JSON with the same task ID exists.

## Exchange commands

```bash
./exchange.sh
./exchange.sh status
./exchange.sh next
./exchange.sh prepare TASK_ID
```

Default `./exchange.sh`:

1. requires the local branch to be `main`,
2. refuses to pull over a dirty working tree,
3. fetches and fast-forwards from `origin/main`,
4. validates the bridge,
5. prints the next pending request.

`./exchange.sh prepare TASK_ID`:

1. requires a clean `main`,
2. fast-forwards from `origin/main`,
3. validates the request,
4. refuses to overwrite an existing local or remote task branch,
5. creates `operator/<task-id>` from `origin/main`.

It does **not** execute the task. Codex remains the execution layer.
