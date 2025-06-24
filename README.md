# Open Targets Croissant Tools

Utilities to introspect Open Targets datasets purely from their
`.croissant.json` metadata.

## Quick‑start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
ot-croissant evidence target
```

List available dataset names:

```bash
ot-croissant --list
```

All commands accept `--offline` to avoid network access and work with
a minimal embedded manifest sample.

## Tests

```bash
python -m pytest
```
