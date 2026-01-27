<script lang="ts">
  export let text: string;
  export let tone: 'neutral' | 'good' | 'warn' | 'bad' = 'neutral';
</script>

<span class={"badge " + (tone === 'neutral' ? '' : tone)}>{text}</span>
