#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"
CMD="${1:-sync}"

require_clean() {
  if ! git diff --quiet || ! git diff --cached --quiet; then
    echo "ERROR: working tree has uncommitted changes; refusing to pull." >&2
    git status --short >&2
    exit 2
  fi
}

pull_ff() {
  require_clean
  git fetch origin main
  git pull --ff-only origin main
}

case "$CMD" in
  sync)
    pull_ff
    python3 .bridge/bridge_cli.py status
    echo "--- NEXT REQUEST ---"
    python3 .bridge/bridge_cli.py next
    ;;
  pull)
    pull_ff
    ;;
  status)
    python3 .bridge/bridge_cli.py status
    ;;
  next)
    python3 .bridge/bridge_cli.py next
    ;;
  *)
    echo "usage: ./exchange.sh [sync|pull|status|next]" >&2
    exit 64
    ;;
esac
