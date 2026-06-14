<script lang="ts">
	import { deriveUserId } from "../lib/crypto.js";

	const UUID_RE = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i;

	let { onSuccess }: { onSuccess: (code: string, userId: string) => void } = $props();

	let code = $state("");
	let loading = $state(false);
	let error = $state<string | null>(null);

	let valid = $derived(UUID_RE.test(code.trim()));

	async function submit() {
		loading = true;
		error = null;
		try {
			const userId = await deriveUserId(code.trim());
			onSuccess(code.trim(), userId);
		} catch (e) {
			error = e instanceof Error ? e.message : String(e);
		} finally {
			loading = false;
		}
	}
</script>

<div class="card preset-outlined-surface-200-800 w-full max-w-md space-y-8 p-8">
	<header class="space-y-1 text-center">
		<h1 class="h1 text-2xl font-semibold tracking-tight">Autosave Cloud</h1>
		<p class="text-sm text-surface-600-400">Enter your backup code to view or restore saves.</p>
	</header>

	<div class="space-y-3">
		<label class="label" for="backup-code">
			<span class="text-xs font-medium uppercase tracking-widest text-surface-600-400">
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
			onkeydown={(e) => e.key === "Enter" && valid && !loading && submit()}
		/>
	</div>

	{#if error}
		<p class="text-error-600-400 text-sm">{error}</p>
	{/if}

	<button class="btn preset-filled w-full" disabled={!valid || loading} onclick={submit}>
		{loading ? "Loading…" : "Load saves"}
	</button>
</div>
