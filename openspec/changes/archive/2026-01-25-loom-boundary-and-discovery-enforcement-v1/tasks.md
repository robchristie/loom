# Tasks: loom-boundary-and-discovery-enforcement-v1

## 0) Project defaults
- [x] Add a minimal project config (can be env vars at first):
  - [x] SDLC_MAX_FILES_TOUCHED (default 8)
  - [x] SDLC_MAX_SUBSYSTEMS_TOUCHED (default 2)
  - [x] SDLC_DISCOVERY_ALLOWLIST (default "docs/,notes/,tools/,experiments/,runs/")

## 1) Boundary registry loading
- Define default boundary registry location:
- [x] `sdlc/boundary_registry.json` (as hinted by the canonical dirs section)
- Implement:
  - [x] load_boundary_registry(paths, bead) -> BoundaryRegistry
    - [x] If bead.boundary_registry_ref exists: resolve it (minimal v1: only support local file ref by convention)
    - [x] Else: load sdlc/boundary_registry.json
  - [x] hash_boundary_registry(registry) -> HashRef

## 2) Change detection (minimal v1)
- Implement best-effort changed-files discovery:
  - [x] Prefer: `git diff --name-only HEAD` or `git diff --name-only <head_before>..HEAD`
  - [x] Fallback: empty list if git unavailable
- [x] NOTE: keep it simple; unit tests can monkeypatch the function that returns changed files.

## 3) Subsystem computation
- Given changed files, compute touched subsystems by prefix matching against BoundaryRegistry.subsystems[].paths.
- Produce:
  - [x] touched_subsystems: list[str]
  - [x] files_touched: int

## 4) Enforcement gates
- Enforce on transitions toward verification (at minimum: when requesting `verification_pending -> verified`):
  - [x] If files_touched > max_files_touched or len(touched_subsystems) > max_subsystems_touched:
    - [x] reject transition with message requiring abort/split
    - [x] write an ExecutionRecord describing metrics + policy thresholds
    - [x] (optional minimal helper) `sdlc abort <bead_id> --reason ...` that appends a DecisionLedgerEntry and requests the abort transition

## 5) Discovery bead Policy A gate
- For BeadType.discovery:
  - [x] Determine production paths = union of boundary registry subsystem prefixes
  - [x] If any changed file begins with any production path prefix:
    - [x] reject start/verify transitions
    - [x] record policy violation in ExecutionRecord
  - [x] If changed files are only inside allowlist prefixes:
    - [x] allow (subject to existing gates)

## 6) Linking BoundaryRegistry in ExecutionRecord.links
- When boundary evaluation occurs, add an ArtifactLink:
  - [x] artifact_type: "boundary_registry"
  - [x] artifact_id: registry.artifact_id
  - [x] schema_name: "sdlc.boundary_registry"
  - [x] schema_version: 1
- [x] Also record the boundary registry hash used (notes_md is fine if you don’t want new fields).

## 7) Tests
Add tests to cover:
- [x] subsystem computation from prefixes
- [x] enforcement triggers on too many files / too many subsystems
- [x] discovery policy rejects production path modifications
- [x] boundary registry link present in the generated ExecutionRecord

## 8) Docs (small)
Add a short section to docs/loom-specification.md describing:
- [x] default boundary registry location
- [x] how discovery allowlist works in v1 (Policy A)
