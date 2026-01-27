<script lang="ts">
  import { onDestroy, onMount } from 'svelte';
  import { invalidateAll } from '$app/navigation';

  import { apiPost, apiUrl } from '$lib/api';
  import type {
    Actor,
    ActorKind,
    ActionResponse,
    Bead,
    BeadArtifactsIndex,
    BeadReview,
    DecisionLedgerEntry,
    EvidenceBundle,
    ExecutionRecord,
    GroundingBundle,
    TimelineItem,
    TransitionResponse
  } from '$lib/types';

  import Badge from '$lib/components/Badge.svelte';
  import StatusRail from '$lib/components/StatusRail.svelte';
  import ArtifactsBar from '$lib/components/ArtifactsBar.svelte';
  import Timeline from '$lib/components/Timeline.svelte';
  import JsonPanel from '$lib/components/JsonPanel.svelte';

  import { fmtWhen, mergeTimeline, nextCanonicalTransition, statusTone, toStatusFromTransition } from '$lib/util';

  export let data: {
    bead_id: string;
    bead: Bead | null;
    artifacts: BeadArtifactsIndex | null;
    review: BeadReview | null;
    grounding: GroundingBundle | null;
    evidence: EvidenceBundle | null;
    journal: ExecutionRecord[];
    decisions: DecisionLedgerEntry[];
    error: string | null;
  };

  let tab: 'timeline' | 'bead' | 'review' | 'grounding' | 'evidence' = 'timeline';

  // Actor defaults (stored locally)
  let actorKind: ActorKind = 'human';
  let actorName = 'you';

  function readActor() {
    try {
      const k = localStorage.getItem('loom.actorKind') as ActorKind | null;
      const n = localStorage.getItem('loom.actorName');
      if (k === 'human' || k === 'agent' || k === 'system') actorKind = k;
      if (n && n.trim()) actorName = n;
    } catch {}
  }

  function persistActor() {
    try {
      localStorage.setItem('loom.actorKind', actorKind);
      localStorage.setItem('loom.actorName', actorName);
    } catch {}
  }

  $: actor = ({ kind: actorKind, name: actorName } satisfies Actor);

  // Suggested next transition
  $: suggested = data.bead ? nextCanonicalTransition(data.bead.status) : null;

  let customTransition = '';
  let approveSummary = 'APPROVAL: ';
  let abortReason = 'needs discovery';

  let busy = false;
  let toast: { type: 'ok' | 'error'; message: string } | null = null;

  // Live timeline via SSE
  let liveJournal: ExecutionRecord[] = [];
  let liveDecisions: DecisionLedgerEntry[] = [];
  $: timelineItems = mergeTimeline([...data.journal, ...liveJournal], [...data.decisions, ...liveDecisions]);

  let sseState: 'disconnected' | 'connecting' | 'connected' = 'disconnected';
  let es: EventSource | null = null;

  function systemActor(): Actor {
    return { kind: 'system', name: 'sdlc-web' };
  }

  function actorForTransition(transition: string): Actor {
    const to = toStatusFromTransition(transition);
    // Your engine enforces verification_pending->verified authority = system.
    if (to === 'verified') return systemActor();
    return actor;
  }

  async function doTransition(transition: string) {
    if (!data.bead) return;
    busy = true;
    toast = null;
    try {
      const body = { transition, actor: actorForTransition(transition) };
      const res = await apiPost<TransitionResponse>(`/api/beads/${data.bead_id}/transition`, body);

      // Optimistically update status if applied
      if (res.applied_transition) {
        const to = toStatusFromTransition(res.applied_transition);
        if (to && data.bead) data.bead.status = to;
      }

      toast = { type: res.ok ? 'ok' : 'error', message: res.notes || (res.ok ? 'ok' : 'failed') };
      await invalidateAll();
    } catch (e) {
      toast = { type: 'error', message: (e as Error).message };
    } finally {
      busy = false;
    }
  }

  async function doAction(path: string, body?: unknown) {
    if (!data.bead) return;
    busy = true;
    toast = null;
    try {
      const res = await apiPost<ActionResponse>(path, body);
      toast = { type: res.ok ? 'ok' : 'error', message: res.notes || (res.ok ? 'ok' : 'failed') };
      await invalidateAll();
    } catch (e) {
      toast = { type: 'error', message: (e as Error).message };
    } finally {
      busy = false;
    }
  }

  async function doApprove() {
    if (!data.bead) return;
    busy = true;
    toast = null;
    try {
      const body = { summary: approveSummary, actor };
      const res = await apiPost<ActionResponse>(`/api/beads/${data.bead_id}/approve`, body);
      toast = { type: res.ok ? 'ok' : 'error', message: res.notes || (res.ok ? 'ok' : 'failed') };
      await invalidateAll();
    } catch (e) {
      toast = { type: 'error', message: (e as Error).message };
    } finally {
      busy = false;
    }
  }

  async function doAbort() {
    if (!data.bead) return;
    busy = true;
    toast = null;
    try {
      const body = { reason: abortReason, actor };
      const res = await apiPost<TransitionResponse>(`/api/beads/${data.bead_id}/abort`, body);
      if (res.applied_transition) {
        const to = toStatusFromTransition(res.applied_transition);
        if (to && data.bead) data.bead.status = to;
      }
      toast = { type: res.ok ? 'ok' : 'error', message: res.notes || (res.ok ? 'ok' : 'failed') };
      await invalidateAll();
    } catch (e) {
      toast = { type: 'error', message: (e as Error).message };
    } finally {
      busy = false;
    }
  }

  function startSse() {
    if (!data.bead) return;
    if (es) es.close();

    sseState = 'connecting';
    const url = apiUrl(`/api/events?bead_id=${encodeURIComponent(data.bead_id)}&start_at_end=true`);
    es = new EventSource(url);

    es.addEventListener('open', () => (sseState = 'connected'));
    es.addEventListener('error', () => (sseState = 'disconnected'));

    es.addEventListener('execution_record', (evt) => {
      try {
        const rec = JSON.parse((evt as MessageEvent).data) as ExecutionRecord;
        liveJournal = [...liveJournal, rec].slice(-500);

        // If a transition happened, update local status
        if (rec.applied_transition && data.bead) {
          const to = toStatusFromTransition(rec.applied_transition);
          if (to) data.bead.status = to;
        }
      } catch {}
    });

    es.addEventListener('decision_entry', (evt) => {
      try {
        const entry = JSON.parse((evt as MessageEvent).data) as DecisionLedgerEntry;
        liveDecisions = [...liveDecisions, entry].slice(-500);
      } catch {}
    });
  }

  onMount(() => {
    readActor();
    startSse();
  });

  onDestroy(() => {
    if (es) es.close();
  });
</script>

{#if data.error}
  <article>
    <h2 class="mono">{data.bead_id}</h2>
    <div class="small">{data.error}</div>
    <hr />
    <a href="/">← back</a>
  </article>
{:else if data.bead}
  <div class="spread">
    <div>
      <h1 class="mono" style="margin-bottom:0.25rem;">{data.bead.bead_id}</h1>
      <div style="margin-bottom:0.5rem;">{data.bead.title}</div>
      <div class="row">
        <Badge text={data.bead.status} tone={statusTone(data.bead.status)} />
        <span class="small mono">type {data.bead.bead_type}</span>
        <span class="small mono">prio {data.bead.priority ?? '—'}</span>
        <span class="small mono">owner {data.bead.owner ?? '—'}</span>
        <span class="small mono">created {fmtWhen(data.bead.created_at)}</span>
      </div>
    </div>

    <div class="row">
      <span class="small mono">SSE: {sseState}</span>
      <button type="button" class="secondary" on:click={() => invalidateAll()} disabled={busy}>
        Refresh
      </button>
    </div>
  </div>

  <hr />

  <StatusRail status={data.bead.status} />

  <hr />

  {#if data.artifacts}
    <ArtifactsBar artifacts={data.artifacts.artifacts} />
    <hr />
  {/if}

  {#if toast}
    <article>
      <strong>{toast.type === 'ok' ? 'OK' : 'Error'}</strong>
      <div class="small mono">{toast.message}</div>
    </article>
  {/if}

  <article>
    <h3 style="margin-top:0;">Interact</h3>

    <div class="grid">
      <label>
        Actor kind
        <select bind:value={actorKind} on:change={persistActor} disabled={busy}>
          <option value="human">human</option>
          <option value="system">system</option>
          <option value="agent">agent</option>
        </select>
      </label>

      <label>
        Actor name
        <input bind:value={actorName} on:blur={persistActor} disabled={busy} />
      </label>
    </div>

    <hr />

    <div class="row">
      <button
        type="button"
        on:click={() => suggested && doTransition(suggested)}
        disabled={!suggested || busy}
      >
        Next: {suggested ?? '—'}
      </button>

      <label style="flex:1; min-width: 280px;">
        Custom transition
        <input class="mono" placeholder="e.g. ready -> in_progress" bind:value={customTransition} disabled={busy} />
      </label>

      <button type="button" class="secondary" on:click={() => doTransition(customTransition)} disabled={!customTransition.trim() || busy}>
        Request
      </button>
    </div>

    <hr />

    <div class="row">
      <button type="button" class="secondary" on:click={() => doAction(`/api/beads/${data.bead_id}/grounding/generate`, systemActor())} disabled={busy}>
        Generate grounding
      </button>

      <button type="button" class="secondary" on:click={() => doAction(`/api/beads/${data.bead_id}/openspec/sync`, systemActor())} disabled={busy}>
        Sync OpenSpecRef
      </button>

      <button type="button" class="secondary" on:click={() => doAction(`/api/beads/${data.bead_id}/evidence/collect`, systemActor())} disabled={busy}>
        Collect evidence skeleton
      </button>

      <button
        type="button"
        class="secondary"
        on:click={() => doAction(`/api/beads/${data.bead_id}/evidence/validate?mark_validated=true`, systemActor())}
        disabled={busy}
      >
        Validate evidence
      </button>

      <button type="button" class="secondary" on:click={() => doAction(`/api/beads/${data.bead_id}/evidence/invalidate-if-stale`, systemActor())} disabled={busy}>
        Invalidate evidence (if stale)
      </button>
    </div>

    <hr />

    <div class="grid">
      <label>
        Approval summary
        <input bind:value={approveSummary} disabled={busy} />
      </label>
      <div class="row" style="align-items:end;">
        <button type="button" on:click={doApprove} disabled={busy || !approveSummary.trim()}>
          Approve
        </button>
      </div>
    </div>

    <div class="grid">
      <label>
        Abort reason
        <input bind:value={abortReason} disabled={busy} />
      </label>
      <div class="row" style="align-items:end;">
        <button type="button" class="contrast" on:click={doAbort} disabled={busy || !abortReason.trim()}>
          Abort
        </button>
      </div>
    </div>
  </article>

  <hr />

  <div class="tabs" role="tablist" aria-label="Bead panels">
    <button type="button" on:click={() => (tab = 'timeline')} aria-current={tab === 'timeline'}>Timeline</button>
    <button type="button" on:click={() => (tab = 'bead')} aria-current={tab === 'bead'}>Bead</button>
    <button type="button" on:click={() => (tab = 'review')} aria-current={tab === 'review'}>Review</button>
    <button type="button" on:click={() => (tab = 'grounding')} aria-current={tab === 'grounding'}>Grounding</button>
    <button type="button" on:click={() => (tab = 'evidence')} aria-current={tab === 'evidence'}>Evidence</button>
  </div>

  {#if tab === 'timeline'}
    <Timeline items={timelineItems} />
  {:else if tab === 'bead'}
    <JsonPanel value={data.bead} />
  {:else if tab === 'review'}
    <JsonPanel value={data.review} />
  {:else if tab === 'grounding'}
    <JsonPanel value={data.grounding} />
  {:else if tab === 'evidence'}
    <JsonPanel value={data.evidence} />
  {/if}
{/if}
