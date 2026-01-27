<script lang="ts">
  import type { TimelineItem } from '$lib/types';
  import { fmtWhen } from '$lib/util';
  export let items: TimelineItem[] = [];
</script>

<div class="timeline">
  {#if items.length === 0}
    <article><em>No events yet.</em></article>
  {:else}
    {#each items as item}
      <article>
        <div class="spread">
          <strong class="mono">
            {#if item.kind === 'execution_record'}
              exec:{item.record.phase}{item.record.exit_code === 0 ? '' : ` (exit ${item.record.exit_code})`}
            {:else}
              decision:{item.entry.decision_type}
            {/if}
          </strong>
          <span class="small mono">{fmtWhen(item.at)}</span>
        </div>

        {#if item.kind === 'execution_record'}
          {#if item.record.requested_transition}
            <div class="small mono" style="margin-top:0.25rem;">
              requested: {item.record.requested_transition}
            </div>
          {/if}
          {#if item.record.applied_transition}
            <div class="small mono">
              applied: {item.record.applied_transition}
            </div>
          {/if}
          {#if item.record.notes_md}
            <div class="small" style="margin-top:0.5rem;">{item.record.notes_md}</div>
          {/if}
          <details style="margin-top:0.5rem;">
            <summary class="small">Raw</summary>
            <pre class="json"><code>{JSON.stringify(item.record, null, 2)}</code></pre>
          </details>
        {:else}
          <div class="small" style="margin-top:0.5rem;">
            <strong>{item.entry.summary}</strong>
          </div>
          {#if item.entry.rationale_md}
            <div class="small">{item.entry.rationale_md}</div>
          {/if}
          <details style="margin-top:0.5rem;">
            <summary class="small">Raw</summary>
            <pre class="json"><code>{JSON.stringify(item.entry, null, 2)}</code></pre>
          </details>
        {/if}
      </article>
    {/each}
  {/if}
</div>
