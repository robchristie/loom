export type ActorKind = 'human' | 'agent' | 'system';

export interface Actor {
  kind: ActorKind;
  name: string;
  email?: string | null;
}

export interface RepoInfo {
  repo_root: string;
  git_head?: string | null;
  git_dirty?: boolean | null;
}

export interface BeadSummary {
  bead_id: string;
  title: string;
  bead_type: string;
  status: string;
  priority?: number;
  owner?: string | null;
  created_at?: string | null;
}

export interface ArtifactStatus {
  name: string;
  path: string;
  exists: boolean;
}

export interface BeadArtifactsIndex {
  bead_id: string;
  artifacts: ArtifactStatus[];
}

// We keep these “loose” because they’re Pydantic-shaped JSON objects.
// Add fields as you need them.
export interface Bead {
  bead_id: string;
  title: string;
  bead_type: string;
  status: string;
  priority?: number;
  owner?: string | null;
  created_at?: string;
  created_by?: Actor;
  acceptance_checks?: unknown[];
  depends_on?: string[];
  [k: string]: unknown;
}

export interface BeadReview {
  bead_id: string;
  effort_bucket: string;
  risk_flags?: string[];
  [k: string]: unknown;
}

export interface GroundingBundle {
  bead_id: string;
  summary_md?: string | null;
  items?: unknown[];
  [k: string]: unknown;
}

export interface EvidenceBundle {
  bead_id: string;
  status: string;
  invalidated_reason?: string | null;
  items?: unknown[];
  [k: string]: unknown;
}

export interface ExecutionRecord {
  schema_name?: string;
  bead_id: string;
  phase: string;
  exit_code?: number | null;
  requested_transition?: string | null;
  applied_transition?: string | null;
  notes_md?: string | null;
  created_at?: string;
  created_by?: Actor;
  produced_artifacts?: Array<{ path: string }>;
  [k: string]: unknown;
}

export interface DecisionLedgerEntry {
  schema_name?: string;
  bead_id?: string | null;
  decision_type: string;
  summary: string;
  rationale_md?: string | null;
  created_at?: string;
  created_by?: Actor;
  [k: string]: unknown;
}

export interface TransitionResponse {
  ok: boolean;
  notes?: string;
  requested_transition: string;
  applied_transition?: string | null;
  auto_abort?: boolean;
  execution_record?: ExecutionRecord | null;
}

export interface ActionResponse {
  ok: boolean;
  notes?: string | null;
  produced_artifacts?: string[];
}

export type TimelineItem =
  | { kind: 'execution_record'; at: string; record: ExecutionRecord }
  | { kind: 'decision_entry'; at: string; entry: DecisionLedgerEntry };
