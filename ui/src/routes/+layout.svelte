<script lang="ts">
  import { onMount } from 'svelte';
  import '../app.css';
  import { apiGet } from '$lib/api';
  import type { RepoInfo } from '$lib/types';

  let repo: RepoInfo | null = null;
  let repoErr: string | null = null;

  onMount(async () => {
    try {
      repo = await apiGet<RepoInfo>('/api/repo');
    } catch (e) {
      repoErr = (e as Error).message;
    }
  });
</script>

<svelte:head>
  <title>Loom Console</title>
</svelte:head>

<header class="container" style="padding-top:1rem;">
  <nav>
    <ul>
      <li><strong><a href="/" class="mono">loom</a></strong></li>
    </ul>
    <ul>
      {#if repo}
        <li class="small mono">HEAD {repo.git_head ? repo.git_head.slice(0, 7) : '—'}</li>
        <li class="small mono">{repo.git_dirty ? 'dirty' : 'clean'}</li>
      {:else if repoErr}
        <li class="small mono">API unreachable</li>
      {:else}
        <li class="small mono">connecting…</li>
      {/if}
    </ul>
  </nav>
</header>

<main class="container" style="padding-bottom:2rem;">
  <slot />
</main>

<footer class="container small" style="padding-bottom:2rem;">
  Artifact-driven SDLC console.
</footer>
