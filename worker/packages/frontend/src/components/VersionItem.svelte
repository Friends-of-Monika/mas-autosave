<script lang="ts">
	import type { Version } from "../lib/api.js";

	let {
		version,
		downloading,
		onDownload
	}: { version: Version; downloading: boolean; onDownload: () => void } = $props();

	function formatDate(iso: string): string {
		return new Date(iso).toLocaleString();
	}

	function formatSize(bytes: number): string {
		return bytes < 1024 ? `${bytes} B` : `${(bytes / 1024).toFixed(1)} KB`;
	}
</script>

<li class="card preset-outlined-surface-100-900 flex items-center justify-between gap-4 p-4">
	<div class="min-w-0 space-y-0.5">
		<p class="truncate font-medium">{version.reason}</p>
		<p class="text-surface-600-400 text-xs">
			{formatDate(version.timestamp)} · {formatSize(version.size)}
		</p>
		<p class="text-surface-700-400 font-mono text-xs">{version.sha256.slice(0, 16)}…</p>
	</div>
	<button class="btn preset-filled btn-sm shrink-0" disabled={downloading} onclick={onDownload}>
		{downloading ? "…" : "Download"}
	</button>
</li>
