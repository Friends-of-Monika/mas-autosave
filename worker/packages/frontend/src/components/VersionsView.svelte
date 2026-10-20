<script lang="ts">
	import { Dialog, Portal } from "@skeletonlabs/skeleton-svelte";
	import { onMount } from "svelte";

	import { deleteAllData, downloadVersion, listVersions, type Version } from "../lib/api.js";
	import { decrypt, deriveKey } from "../lib/crypto.js";
	import VersionItem from "./VersionItem.svelte";

	let { code, userId, onBack }: { code: string; userId: string; onBack: () => void } = $props();

	let versions = $state<Version[]>([]);
	let loading = $state(true);
	let error = $state<string | null>(null);
	let downloadingHash = $state<string | null>(null);
	let deleteOpen = $state(false);
	let deleting = $state(false);
	let deleted = $state(false);
	let copied = $state(false);

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

	async function copyUserId() {
		try {
			await navigator.clipboard.writeText(userId);
			copied = true;
			setTimeout(() => (copied = false), 1500);
		} catch (e) {
			error = e instanceof Error ? e.message : String(e);
		}
	}

	async function deleteAll() {
		deleting = true;
		error = null;
		try {
			await deleteAllData(userId);
			versions = [];
			deleted = true;
		} catch (e) {
			error = e instanceof Error ? e.message : String(e);
		} finally {
			deleting = false;
			deleteOpen = false;
		}
	}
</script>

<div class="card preset-outlined-surface-200-800 w-full max-w-xl space-y-6 p-8">
	<header class="flex items-center gap-4">
		<button class="btn preset-outlined btn-sm" onclick={onBack}>← Back</button>
		<div>
			<h1 class="h1 text-2xl font-semibold tracking-tight">Saves</h1>
			<p class="text-surface-600-400 flex items-baseline gap-3 font-mono text-xs">
				<span>{code}</span>
				<button class="hover:text-surface-950-50 cursor-pointer" onclick={copyUserId}>
					{copied ? "Copied!" : "Copy user ID"}
				</button>
			</p>
		</div>
	</header>

	{#if error}
		<p class="text-error-600-400 text-sm">{error}</p>
	{/if}

	{#if loading}
		<p class="text-surface-600-400 py-8 text-center text-sm">Loading…</p>
	{:else if deleted}
		<p class="text-surface-600-400 py-8 text-center text-sm">All your data has been deleted.</p>
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

<Dialog open={deleteOpen} onOpenChange={(e) => (deleteOpen = deleting || e.open)}>
	<Dialog.Trigger
		class="text-surface-600-400 hover:text-error-600-400 fixed bottom-6 left-1/2 -translate-x-1/2 font-mono text-sm"
	>
		Delete all my data
	</Dialog.Trigger>
	<Portal>
		<Dialog.Backdrop class="bg-surface-50-950/50 fixed inset-0 z-50" />
		<Dialog.Positioner class="fixed inset-0 z-50 flex items-center justify-center p-4">
			<Dialog.Content
				class="card bg-surface-100-900 w-full max-w-md space-y-4 p-6 shadow-xl"
			>
				<Dialog.Title class="text-lg font-semibold">Delete all my data?</Dialog.Title>
				<Dialog.Description class="text-surface-600-400 text-sm">
					This permanently deletes all cloud backups stored under this code. This cannot be
					undone.
				</Dialog.Description>
				<footer class="flex justify-end gap-2">
					<Dialog.CloseTrigger class="btn preset-tonal" disabled={deleting}>
						Cancel
					</Dialog.CloseTrigger>
					<button class="btn preset-filled-error-500" disabled={deleting} onclick={deleteAll}>
						{deleting ? "Deleting…" : "Delete"}
					</button>
				</footer>
			</Dialog.Content>
		</Dialog.Positioner>
	</Portal>
</Dialog>
