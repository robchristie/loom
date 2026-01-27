<script lang="ts">
  export let value: unknown;

  function asJson(v: unknown): string {
    if (v === null || v === undefined) return '—';
    try {
      return JSON.stringify(v, null, 2);
    } catch {
      return String(v);
    }
  }

  async function copy() {
    await navigator.clipboard.writeText(asJson(value));
  }
</script>

<div class="row" style="margin-bottom:0.5rem;">
  <button class="secondary" type="button" on:click={copy} disabled={value == null}>
    Copy JSON
  </button>
</div>

<pre class="json"><code>{asJson(value)}</code></pre>
