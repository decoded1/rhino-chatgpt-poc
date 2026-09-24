# Rhino ChatGPT Bridge Protocol v0.2

This repository is the laboratory for the controller/operator bridge.

## Roles

- **Controller:** ChatGPT Web
- **Transport:** GitHub / Git
- **Operator:** Codex on the local Mac

## Directories

- `.bridge/requests/` — controller-created tasks
- `.bridge/reports/` — operator-created task results
- `.bridge/state/` — durable controller/operator state
- `.bridge/templates/` — report examples

A request is considered pending when a request JSON exists and no report JSON with the same task ID exists.

## Safe exchange

```bash
./exchange.sh
```

The default exchange:

1. refuses to pull over a dirty working tree,
2. fetches `origin`,
3. fast-forwards `main` only,
4. validates the bridge files,
5. prints the next pending controller request.

It **does not automatically execute arbitrary instructions**. Codex remains the execution layer.

Other commands:

```bash
./exchange.sh status
./exchange.sh next
./exchange.sh pull
```
