import type { PageLoad } from './$types';
import { apiGetOrNull } from '$lib/api';
import type {
  Bead,
  BeadArtifactsIndex,
  BeadReview,
  DecisionLedgerEntry,
  EvidenceBundle,
  ExecutionRecord,
  GroundingBundle
} from '$lib/types';

export const load: PageLoad = async ({ params }) => {
  const bead_id = params.bead_id;

  const bead = await apiGetOrNull<Bead>(`/api/beads/${bead_id}`);
  if (!bead) {
    return {
      bead_id,
      bead: null,
      artifacts: null,
      review: null,
      grounding: null,
      evidence: null,
      journal: [],
      decisions: [],
      error: 'Bead not found (or API unreachable).'
    };
  }

  const [artifacts, review, grounding, evidence, journal, decisions] = await Promise.all([
    apiGetOrNull<BeadArtifactsIndex>(`/api/beads/${bead_id}/artifacts`),
    apiGetOrNull<BeadReview>(`/api/beads/${bead_id}/review`),
    apiGetOrNull<GroundingBundle>(`/api/beads/${bead_id}/grounding`),
    apiGetOrNull<EvidenceBundle>(`/api/beads/${bead_id}/evidence`),
    apiGetOrNull<ExecutionRecord[]>(`/api/beads/${bead_id}/journal`),
    apiGetOrNull<DecisionLedgerEntry[]>(`/api/beads/${bead_id}/decisions`)
  ]);

  return {
    bead_id,
    bead,
    artifacts,
    review,
    grounding,
    evidence,
    journal: journal ?? [],
    decisions: decisions ?? [],
    error: null
  };
};
