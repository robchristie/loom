<script lang="ts">
  export let status: string;

  const canonical = [
    'draft',
    'sized',
    'ready',
    'in_progress',
    'verification_pending',
    'verified',
    'approval_pending',
    'done'
  ];

  $: idx = canonical.indexOf(status);
  $: isCanonical = idx !== -1;
</script>

<div class="small" style="margin-bottom:0.25rem;">Lifecycle</div>

<div class="rail">
  {#each canonical as s, i}
    <div class={"node " + (s === status ? 'active' : '') + (idx !== -1 && i < idx ? ' past' : '')}>
      <span class="mono">{s}</span>
    </div>
  {/each}
</div>

{#if !isCanonical}
  <div class="small" style="margin-top:0.5rem;">
    Non-canonical state: <span class="mono">{status}</span>
  </div>
{/if}

<style>
  .rail {
    display: grid;
    grid-template-columns: repeat(8, minmax(0, 1fr));
    gap: 0.35rem;
  }
  .node {
    padding: 0.35rem 0.35rem;
    border: 1px solid var(--pico-muted-border-color);
    border-radius: 0.5rem;
    text-align: center;
    background: transparent;
    opacity: 0.85;
  }
  .node.past {
    opacity: 0.6;
  }
  .node.active {
    opacity: 1;
    border-color: var(--pico-primary-border);
    box-shadow: 0 0 0 1px var(--pico-primary-border);
  }
  .mono {
    font-size: 0.75rem;
  }
</style>
