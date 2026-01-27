<script lang="ts">
  import type { ArtifactStatus } from '$lib/types';
  export let artifacts: ArtifactStatus[] = [];
</script>

<div class="small" style="margin-bottom:0.25rem;">Artifacts</div>

<div class="grid" style="grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap:0.5rem;">
  {#each artifacts as a}
    <article style="margin:0; padding:0.75rem;">
      <div class="spread">
        <strong class="mono">{a.name}</strong>
        <span class="mono">{a.exists ? '✅' : '—'}</span>
      </div>
      <div class="small mono" style="margin-top:0.25rem;">{a.path}</div>
    </article>
  {/each}
</div>
