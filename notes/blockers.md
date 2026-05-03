# Blockers

## Phase 0 dependency install blocked by shell network

Command attempted:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Observed result:

- `.venv/` was created successfully.
- The venv already had `pip 26.0`.
- `pip install` could not resolve PyPI hosts from the shell sandbox.
- Error repeated for `/simple/pip/` and `/simple/mlx-lm/`:

```text
Failed to establish a new connection: [Errno 8] nodename nor servname provided, or not known
ERROR: Could not find a version that satisfies the requirement mlx-lm==0.31.2 (from versions: none)
ERROR: No matching distribution found for mlx-lm==0.31.2
```

Interpretation:

This looks like blocked DNS/network access from shell commands, not a package-version problem. Web-based source checks still work, but the shell cannot download packages.

Current status:

- Phase 0 code files are written.
- Dependency installation is incomplete.
- Model downloads and sanity-check execution were not attempted.

Next action:

Run the same pip commands in an environment where this repo's shell has PyPI network access, or have the human run them locally in the repo. Do not proceed to model download or sanity checks until dependencies install cleanly.

## Resume instructions for the user

When shell network access is available, resume from the repo root:

```bash
cd /Users/gordonxiong/Desktop/Repos/memory_state
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python scripts/download_models.py
python scripts/phase0_sanity_check.py
```

Notes:

- `scripts/download_models.py` downloads about 9 GB into `./models/`.
- Do not move the models into the default HuggingFace cache; the project expects local paths under `./models/`.
- After the sanity check finishes, share `results/phase0_sanity_check.json` for review.
