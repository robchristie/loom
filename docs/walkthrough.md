# Loom Walkthrough

Loom’s SDLC artifacts are file-backed: a bead lives at `runs/<bead_id>/bead.json`, with companion artifacts like `grounding.json` and `evidence.json` in the same directory, and append-only timelines in `runs/journal.jsonl` plus `decision_ledger.jsonl` at repo root.

Below is a **start-from-empty-repo → finish-with-working-app** walkthrough that exercises the system end-to-end, including the **agent workflow** (OpenRouter for planner/verifier + `codex` for implementation).

---

## What we’ll build

A tiny “Hello” FastAPI app in a single file:

* `hello_app.py` exposes `GET /?name=...` returning JSON
* `uv run pytest -q` is the acceptance check

We’ll let Loom drive:

* lifecycle gates (`draft → … → done`)
* OpenSpec wiring (approved OpenSpecRef)
* grounding bundle
* agent plan → codex implement → verify (runs checks + produces evidence + optional verifier)

---

## 0) Prereqs and environment

### Tools you need locally

* **Python 3.13+** (Loom itself declares `requires-python = ">=3.13"`).
* `uv`
* `git`
* `codex` CLI available in PATH (or configure `LOOM_CODEX_BIN`).

### OpenRouter key + optional model config

Planner/verifier use OpenRouter via env `OPENROUTER_API_KEY` (required if you run `sdlc agent plan`, and also needed for verifier if enabled).

```bash
export OPENROUTER_API_KEY="...your key..."
# optional overrides:
export LOOM_PLANNER_MODEL="openai/gpt-4o-mini"
export LOOM_VERIFIER_MODEL="openai/gpt-4o-mini"
```

### Make agents auto-advance lifecycle (recommended)

Loom supports an **auto transition** mode for agent runs via `LOOM_AGENT_AUTO_TRANSITION` (or CLI flags like `--auto-transition`).

```bash
export LOOM_AGENT_AUTO_TRANSITION=1
```

---

## 1) Create an empty repo + Python deps

```bash
mkdir hello-loom-app
cd hello-loom-app
git init
```

Create a minimal `pyproject.toml` (feel free to tweak versions):

```toml
# pyproject.toml
[project]
name = "hello-loom-app"
version = "0.1.0"
requires-python = ">=3.13"
dependencies = [
  "fastapi>=0.110.0",
  "uvicorn>=0.27.0",
  "pytest>=8.0.0",
  "httpx>=0.27.0",
]
```

Then sync deps:

```bash
uv sync
```

### Install Loom into this repo’s environment

Because Loom exposes the `sdlc` CLI via a project script entry point, installing it makes `uv run sdlc ...` work.

Use whichever is true for you:

```bash
# Option A: editable install from a local Loom checkout
uv pip install -e /path/to/loom

# Option B: if Loom is already published somewhere you can install from
# uv pip install loom
```

Sanity check:

```bash
uv run sdlc --help
```

---

## 2) Add a minimal Boundary Registry

By default, Loom looks for `sdlc/boundary_registry.json` as the boundary registry file.

Create it:

```bash
mkdir -p sdlc
cat > sdlc/boundary_registry.json << 'EOF'
{
  "schema_name": "sdlc.boundary_registry",
  "schema_version": 1,
  "artifact_id": "boundary-registry-default",
  "created_at": "2026-01-27T00:00:00Z",
  "created_by": { "kind": "system", "name": "hello-loom-bootstrap" },
  "registry_name": "hello-loom-boundaries",
  "subsystems": [
    { "name": "app", "paths": ["hello_app.py"], "invariants": ["Single-file app for demo"] },
    { "name": "tests", "paths": ["tests/"], "invariants": ["Tests only"] }
  ],
  "notes": "Demo registry for subsystem counting + boundary enforcement."
}
EOF
```

(You can make this stricter later; this is just enough to exercise boundary evaluation.)

---

## 3) Create an OpenSpec proposal + an approved OpenSpecRef

### 3.1 The proposal markdown

Create the OpenSpec change doc:

```bash
mkdir -p openspec/changes/bootstrap-agentic-sdlc-v1
cat > openspec/changes/bootstrap-agentic-sdlc-v1/proposal.md << 'EOF'
# Change: Build a Hello FastAPI app

## Why
We need a minimal repo that exercises Loom’s lifecycle + agent flow end-to-end.

## What Changes
- Add `hello_app.py` implementing a FastAPI app with `GET /?name=...`
- Add tests in `tests/` proving the behavior
- Provide a simple run instruction using uvicorn

## Impact
- Affected code: `hello_app.py`, `tests/`
- Acceptance: `uv run pytest -q` passes
EOF
```

### 3.2 The approved OpenSpecRef JSON

Loom expects an OpenSpecRef artifact and (for implementation beads) it must be **approved** per the spec gate behavior.

Create:

```bash
mkdir -p openspec/refs
cat > openspec/refs/openspec-helloapp.json << 'EOF'
{
  "schema_name": "sdlc.openspec_ref",
  "schema_version": 1,
  "artifact_id": "openspec-helloapp",
  "created_at": "2026-01-27T00:00:00Z",
  "created_by": { "kind": "human", "name": "you" },
  "change_id": "bootstrap-agentic-sdlc-v1",
  "state": "approved",
  "path": "openspec/changes/bootstrap-agentic-sdlc-v1/proposal.md",
  "approved_at": "2026-01-27T00:00:00Z",
  "approved_by": { "kind": "human", "name": "you" }
}
EOF
```

---

## 4) Create the bead (work item)

Bead IDs must match the `work-...` format (regex-enforced), and **`artifact_id` must equal `bead_id`**.

We’ll use:

* `bead_id = work-helloapp`
* `bead_type = implementation` (so spec gate applies)

Create the bead:

```bash
mkdir -p runs/work-helloapp
cat > runs/work-helloapp/bead.json << 'EOF'
{
  "schema_name": "sdlc.bead",
  "schema_version": 1,
  "artifact_id": "work-helloapp",
  "created_at": "2026-01-27T00:00:00Z",
  "created_by": { "kind": "human", "name": "you" },

  "bead_id": "work-helloapp",
  "title": "Hello FastAPI app (agentic demo)",
  "bead_type": "implementation",
  "status": "draft",

  "priority": 3,
  "owner": "you",

  "openspec_ref": {
    "artifact_type": "openspec_ref",
    "artifact_id": "openspec-helloapp",
    "schema_name": "sdlc.openspec_ref",
    "schema_version": 1
  },

  "requirements_md": "Create hello_app.py and tests per OpenSpec.",
  "acceptance_criteria_md": "- uv run pytest -q passes\n- App can be run with uvicorn",
  "context_md": "Start from empty repo. Use agent workflow to implement.",

  "acceptance_checks": [],
  "execution_profile": "sandbox",
  "depends_on": []
}
EOF
```

Validate it:

```bash
uv run sdlc validate runs/work-helloapp/bead.json
```

(Validation is part of the documented “Example flow”.)

---

## 5) Drive the lifecycle to READY

### 5.1 draft → sized

```bash
uv run sdlc request work-helloapp "draft -> sized"
```



### 5.2 Add bead review (sets acceptance checks)

Create `runs/work-helloapp/bead_review.json` with a single acceptance check:

```bash
cat > runs/work-helloapp/bead_review.json << 'EOF'
{
  "schema_name": "sdlc.bead_review",
  "schema_version": 1,
  "artifact_id": "review-work-helloapp",
  "created_at": "2026-01-27T00:00:00Z",
  "created_by": { "kind": "human", "name": "reviewer" },

  "bead_id": "work-helloapp",
  "effort_bucket": "S",
  "risk_flags": [],
  "split_required": false,

  "tightened_acceptance_checks": [
    {
      "name": "tests",
      "command": "uv run pytest -q",
      "expect_exit_code": 0
    }
  ],

  "notes": "Single check is enough for the demo; tests cover behavior."
}
EOF
```

### 5.3 sized → ready

```bash
uv run sdlc request work-helloapp "sized -> ready"
```



At this point, Loom will freeze the acceptance checks for the bead (you’ll see a ready snapshot artifact in the bead dir in Loom’s UI/endpoint list).

---

## 6) Generate grounding + sync OpenSpecRef into the bead run

### 6.1 Grounding bundle

```bash
uv run sdlc grounding generate work-helloapp
```



### 6.2 Sync OpenSpecRef into `runs/work-helloapp/openspec_ref.json`

This is important because both gates and agents expect the per-run copy; the agent code even suggests running the sync if the file is missing.

```bash
uv run sdlc openspec sync work-helloapp
```



---

## 7) Run the agent workflow (Plan → Implement via codex → Verify)

The README describes the agent workflow and the artifacts it produces (`agent_plan.json`, `codex_prompt.md`, `codex.log`, evidence, etc.).

### 7.1 Plan

```bash
uv run sdlc agent plan work-helloapp
```

This writes:

* `runs/work-helloapp/agent_plan.json`
* `runs/work-helloapp/codex_prompt.md`

(If `OPENROUTER_API_KEY` is missing, OpenRouter model construction fails.)

### 7.2 Implement (codex)

```bash
uv run sdlc agent implement work-helloapp --auto-transition
```

CLI supports `--auto-transition` for implement/verify.

What happens:

* If the bead is `ready`, the agent can **auto transition `ready -> in_progress`** (as system).
* It runs codex and writes `runs/work-helloapp/codex.log`.
* If codex succeeds (exit code 0) and bead is `in_progress`, it can auto transition to `verification_pending`.

### 7.3 Verify (runs acceptance checks + produces evidence)

```bash
uv run sdlc agent verify work-helloapp --auto-transition
```

Verify does a lot:

* Runs the acceptance checks and writes:

  * `runs/work-helloapp/evidence.json`
  * per-check logs under `runs/work-helloapp/evidence/<check>.log` (and attaches them)
* Validates the evidence bundle against the bead (so it becomes “validated” if checks pass)
* Optionally runs an LLM verifier (if a model is available / API key set) and writes `agent_verify.json`
* If everything is OK and bead is `verification_pending`, it can auto transition to `verified` (system-only transition).

---

## 8) Approve and finish (approval_pending → done)

From the “Example flow”, approvals are recorded and then the bead transitions to done.

```bash
# Move verified → approval_pending
uv run sdlc request work-helloapp "verified -> approval_pending"

# Create an approval decision entry
uv run sdlc approve work-helloapp --summary "APPROVAL: hello app works; tests + run instructions present"

# Finish
uv run sdlc request work-helloapp "approval_pending -> done"
```



---

## 9) Run the resulting application

Assuming codex followed the spec and created `hello_app.py` as described, you should be able to run:

```bash
# start server
uv run uvicorn hello_app:app --reload --port 8000
```

Then:

```bash
curl "http://localhost:8000/?name=Loom"
```

Expected JSON shape is up to your OpenSpec, but typically something like `{"message":"Hello, Loom!"}`.

---

## 10) Optional: visualize via Loom’s FastAPI + UI

Loom includes a FastAPI server run script like:

* `uv run uvicorn sdlc.server:app --reload --port 54321 --host 0.0.0.0`

And a Svelte UI that proxies `/api` to a configured backend; in the repo snapshot it’s set to a specific host, so you’d update it to `http://localhost:54321` for local use.

---

## What “success” looks like on disk

You’ll end up with (at minimum):

* `runs/work-helloapp/bead.json`
* `runs/work-helloapp/bead_review.json`
* `runs/work-helloapp/grounding.json`
* `runs/work-helloapp/openspec_ref.json`
* `runs/work-helloapp/agent_plan.json`
* `runs/work-helloapp/codex_prompt.md`
* `runs/work-helloapp/codex.log`
* `runs/work-helloapp/evidence.json`
* `runs/work-helloapp/evidence/tests.log`
* `runs/journal.jsonl` (append-only execution timeline)
* `decision_ledger.jsonl` (append-only decisions)

---

## Quick troubleshooting

* **`sdlc agent plan` fails**: ensure `OPENROUTER_API_KEY` is set; it’s required for OpenRouter model creation.
* **Implement won’t start because of spec gate**: ensure you ran `uv run sdlc openspec sync work-helloapp` so `runs/.../openspec_ref.json` exists.
* **`codex` not found**: install it or set `LOOM_CODEX_BIN` to the correct executable name/path.
* **Verify fails**: open `runs/work-helloapp/evidence/tests.log` to see stdout/stderr captured for the check.

---
