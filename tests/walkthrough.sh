#!/usr/bin/env bash
set -euo pipefail

export LOOM_AGENT_AUTO_TRANSITION=1

SCRIPT_PATH=$(realpath "$0")
SCRIPT_PATH=$(dirname "$SCRIPT_PATH")
LOOM_PATH=$(realpath "$SCRIPT_PATH/..")

# OpenRouter API Key
source "${LOOM_PATH}/.env"
#echo $OPENROUTER_API_KEY

PROJ_DIR="hello-loom-app"

#rm -rf $PROJ_DIR
mkdir -p ${PROJ_DIR}
pushd $PROJ_DIR

step_1 () {
echo  "1) Create an empty repo + Python deps"
git init

# Create a minimal `pyproject.toml` and sync deps
cat <<EOF > pyproject.toml
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
EOF

uv sync > /dev/null

## Install Loom into this repo’s environment
uv pip install -e $LOOM_PATH > /dev/null

# Sanity check
uv run sdlc --help
}

step_2 () {
echo  "2) Add a minimal Boundary Registry"
# By default, Loom looks for `sdlc/boundary_registry.json` as the boundary registry file.
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
}

step_3 () {
echo "3) Create an OpenSpec proposal + an approved OpenSpecRef"
### 3.1 The proposal markdown

#Create the OpenSpec change doc:

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
### 3.2 The approved OpenSpecRef JSON

# Loom expects an OpenSpecRef artifact and (for implementation beads) it must be **approved** per the spec gate behavior.

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

}

step_4 () {
echo "4) Create the bead (work item)"

# Bead IDs must match the `work-...` format (regex-enforced), and **`artifact_id` must equal `bead_id`**.

# We’ll use:
# * `bead_id = work-helloapp`
# * `bead_type = implementation` (so spec gate applies)

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

# Validate it
uv run sdlc validate runs/work-helloapp/bead.json

}

step_5 () {
echo "5) Drive the lifecycle to READY"
# 5.1 draft → sized
uv run sdlc request work-helloapp "draft -> sized"

# 5.2 Add bead review (sets acceptance checks)
#Create `runs/work-helloapp/bead_review.json` with a single acceptance check:

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

# 5.3 sized → ready
uv run sdlc request work-helloapp "sized -> ready"
}

step_6 () {
echo "6) Generate grounding + sync OpenSpecRef into the bead run"

# 6.1 Grounding bundle
uv run sdlc grounding generate work-helloapp

# 6.2 Sync OpenSpecRef into `runs/work-helloapp/openspec_ref.json`
#This is important because both gates and agents expect the per-run copy; the agent code even suggests running the sync if the file is missing.

uv run sdlc openspec sync work-helloapp

}

step_7 () {
echo "7) Run the agent workflow (Plan → Implement via codex → Verify)"

# The README describes the agent workflow and the artifacts it produces (`agent_plan.json`, `codex_prompt.md`, `codex.log`, evidence, etc.).

# 7.1 Plan
uv run sdlc agent plan work-helloapp

# This writes:
# * `runs/work-helloapp/agent_plan.json`
# * `runs/work-helloapp/codex_prompt.md`

# If `OPENROUTER_API_KEY` is missing, OpenRouter model construction fails.

# 7.2 Implement (codex)
uv run sdlc agent implement work-helloapp --auto-transition

# 7.3 Verify (runs acceptance checks + produces evidence)
uv run sdlc agent verify work-helloapp --auto-transition

}

step_8 () {
echo "8) Approve and finish (approval_pending → done)"

# From the “Example flow”, approvals are recorded and then the bead transitions to done.

# Move verified → approval_pending
uv run sdlc request work-helloapp "verified -> approval_pending"

# Create an approval decision entry
uv run sdlc approve work-helloapp --summary "APPROVAL: hello app works; tests + run instructions present"

# Finish
uv run sdlc request work-helloapp "approval_pending -> done"
}

step_9 () {
echo "9) Run the resulting application"

#Assuming codex followed the spec and created `hello_app.py` as described, you should be able to run:

# start server
echo "Starting server on http://127.0.0.1:8765..."
uv run uvicorn hello_app:app --reload --port 8765 &
BACKEND_PID=$!

# Wait for server to start
sleep 5

# Then:
curl "http://localhost:8765/?name=Loom"

#Expected JSON shape is up to your OpenSpec, but typically something like `{"message":"Hello, Loom!"}`.

kill $BACKEND_PID
wait
}


#step_1
#step_2
#step_3
#step_4
#step_5
#step_6
#step_7
#step_8
step_9
