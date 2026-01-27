import type { DecisionLedgerEntry, ExecutionRecord, TimelineItem } from './types';

export function fmtWhen(iso?: string | null): string {
  if (!iso) return '—';
  const d = new Date(iso);
  if (Number.isNaN(d.getTime())) return iso;
  return d.toLocaleString();
}

export function statusTone(status: string): 'good' | 'warn' | 'bad' | 'neutral' {
  if (status === 'done') return 'good';
  if (status.startsWith('aborted') || status === 'failed') return 'bad';
  if (status === 'blocked') return 'warn';
  return 'neutral';
}

export function mergeTimeline(
  journal: ExecutionRecord[],
  decisions: DecisionLedgerEntry[]
): TimelineItem[] {
  const items: TimelineItem[] = [];

  for (const r of journal) {
    items.push({
      kind: 'execution_record',
      at: r.created_at ?? '',
      record: r
    });
  }

  for (const e of decisions) {
    items.push({
      kind: 'decision_entry',
      at: e.created_at ?? '',
      entry: e
    });
  }

  items.sort((a, b) => (a.at || '').localeCompare(b.at || ''));
  return items;
}

export function nextCanonicalTransition(status: string): string | null {
  const map: Record<string, string> = {
    draft: 'draft -> sized',
    sized: 'sized -> ready',
    ready: 'ready -> in_progress',
    in_progress: 'in_progress -> verification_pending',
    verification_pending: 'verification_pending -> verified',
    verified: 'verified -> approval_pending',
    approval_pending: 'approval_pending -> done'
  };
  return map[status] ?? null;
}

export function toStatusFromTransition(transition?: string | null): string | null {
  if (!transition) return null;
  const parts = transition.split('->');
  if (parts.length !== 2) return null;
  return parts[1].trim();
}
