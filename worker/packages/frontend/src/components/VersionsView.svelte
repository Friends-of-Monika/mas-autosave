<script lang="ts">
	import { onMount } from "svelte";

	import { downloadVersion, listVersions, type Version } from "../lib/api.js";
	import { decrypt, deriveKey } from "../lib/crypto.js";
	import VersionItem from "./VersionItem.svelte";

	let { code, userId, onBack }: { code: string; userId: string; onBack: () => void } = $props();

	let versions = $state<Version[]>([]);
	let loading = $state(true);
	let error = $state<string | null>(null);
	let downloadingHash = $state<string | null>(null);

	onMount(async () => {
		try {
			versions = await listVersions(userId);
		} catch (e) {
			error = e instanceof Error ? e.message : String(e);
		} finally {
			loading = false;
		}
	});

	async function download(sha256: string) {
		downloadingHash = sha256;
		error = null;
		try {
			const key = await deriveKey(code);
			const encrypted = await downloadVersion(userId, sha256);
			const plaintext = await decrypt(encrypted, key);
			const url = URL.createObjectURL(new Blob([plaintext]));
			const a = document.createElement("a");
			a.href = url;
			a.download = "persistent";
			a.click();
			URL.revokeObjectURL(url);
		} catch (e) {
			error = e instanceof Error ? e.message : String(e);
		} finally {
			downloadingHash = null;
		}
	}
</script>

<div class="card preset-outlined-surface-200-800 w-full max-w-xl space-y-6 p-8">
	<header class="flex items-center gap-4">
		<button class="btn preset-outlined btn-sm" onclick={onBack}>← Back</button>
		<div>
			<h1 class="h1 text-2xl font-semibold tracking-tight">Saves</h1>
			<p class="font-mono text-xs text-surface-600-400">{code}</p>
		</div>
	</header>

	{#if error}
		<p class="text-error-600-400 text-sm">{error}</p>
	{/if}

	{#if loading}
		<p class="text-surface-600-400 py-8 text-center text-sm">Loading…</p>
	{:else if versions.length === 0}
		<p class="text-surface-600-400 py-8 text-center text-sm">No saves found.</p>
	{:else}
		<ul class="space-y-3">
			{#each versions as v (v.sha256)}
				<VersionItem
					version={v}
					downloading={downloadingHash === v.sha256}
					onDownload={() => download(v.sha256)}
				/>
			{/each}
		</ul>
	{/if}
</div>
