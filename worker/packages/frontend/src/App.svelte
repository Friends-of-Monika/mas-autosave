<script lang="ts">
  const UUID_RE = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i;
  let code = $state("");
  let valid = $derived(UUID_RE.test(code.trim()));
</script>

<div class="flex min-h-screen items-center justify-center bg-surface-950 p-6">
  <div class="card preset-outlined-surface-200-800 w-full max-w-md space-y-8 p-8">
    <header class="space-y-1 text-center">
      <h1 class="h1 text-2xl font-semibold tracking-tight">Autosave Cloud</h1>
      <p class="text-sm text-surface-400">
        Enter your backup code to view or restore saves.
      </p>
    </header>

    <div class="space-y-3">
      <label class="label" for="backup-code">
        <span class="text-xs font-medium uppercase tracking-widest text-surface-400">
          Backup code
        </span>
      </label>
      <input
        id="backup-code"
        class="input font-mono"
        type="text"
        placeholder="xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
        maxlength={36}
        spellcheck={false}
        autocomplete="off"
        bind:value={code}
      />
    </div>

    <button class="btn preset-filled w-full" disabled={!valid}>
      Load saves
    </button>
  </div>
</div>
