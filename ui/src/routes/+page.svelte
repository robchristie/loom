<script lang="ts">
  import { onMount } from 'svelte';
  import { apiGet } from '$lib/api';
  import type { BeadSummary } from '$lib/types';
  import Badge from '$lib/components/Badge.svelte';
  import { fmtWhen, statusTone } from '$lib/util';

  let beads: BeadSummary[] = [];
  let loading = false;
  let error: string | null = null;

  let q = '';
  let status = '';
  let limit = 200;

  async function load() {
    loading = true;
    error = null;
    try {
      const params = new URLSearchParams();
      if (q.trim()) params.set('q', q.trim());
      if (status.trim()) params.set('status', status.trim());
      params.set('limit', String(limit));
      beads = await apiGet<BeadSummary[]>(`/api/beads?${params.toString()}`);
    } catch (e) {
      error = (e as Error).message;
      beads = [];
    } finally {
      loading = false;
    }
  }

  onMount(load);
</script>

<div class="spread">
  <div>
    <h1 style="margin-bottom:0.25rem;">Beads</h1>
    <div class="small">Interact with lifecycle stages + observe state.</div>
  </div>

  <button type="button" class="secondary" on:click={load} disabled={loading}>
    {loading ? 'Loading…' : 'Refresh'}
  </button>
</div>

<form on:submit|preventDefault={load} style="margin-top:1rem;">
  <div class="grid">
    <input placeholder="Search id/title…" bind:value={q} />
    <select bind:value={status} aria-label="Filter by status">
      <option value="">All statuses</option>
      <option value="draft">draft</option>
      <option value="sized">sized</option>
      <option value="ready">ready</option>
      <option value="in_progress">in_progress</option>
      <option value="verification_pending">verification_pending</option>
      <option value="verified">verified</option>
      <option value="approval_pending">approval_pending</option>
      <option value="done">done</option>
      <option value="blocked">blocked</option>
      <option value="aborted:needs-discovery">aborted:needs-discovery</option>
      <option value="failed">failed</option>
      <option value="superseded">superseded</option>
    </select>
    <button type="submit" disabled={loading}>Apply</button>
  </div>
</form>

{#if error}
  <article style="margin-top:1rem;">
    <strong>Error</strong>
    <div class="small mono">{error}</div>
  </article>
{/if}

{#if beads.length === 0 && !loading && !error}
  <article style="margin-top:1rem;"><em>No beads found.</em></article>
{:else if beads.length > 0}
  <table style="margin-top:1rem;">
    <thead>
      <tr>
        <th>Bead</th>
        <th>Status</th>
        <th>Type</th>
        <th>Priority</th>
        <th>Owner</th>
        <th>Created</th>
      </tr>
    </thead>
    <tbody>
      {#each beads as b}
        <tr>
          <td>
            <a class="mono" href={`/beads/${b.bead_id}`}>{b.bead_id}</a>
            <div class="small">{b.title}</div>
          </td>
          <td>
            <Badge text={b.status} tone={statusTone(b.status)} />
          </td>
          <td class="mono">{b.bead_type}</td>
          <td class="mono">{b.priority ?? '—'}</td>
          <td class="mono">{b.owner ?? '—'}</td>
          <td class="mono small">{fmtWhen(b.created_at)}</td>
        </tr>
      {/each}
    </tbody>
  </table>
{/if}
