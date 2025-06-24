# Open Targets Croissant Tools

Utilities to discover every dataset in the Open Targets Platform **purely from
their `.croissant.json` metadata** — no hand‑maintained schemas required.

## Quick‑start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python croissant_introspect.py evidence target disease
```

## Tests

```bash
pytest
```
