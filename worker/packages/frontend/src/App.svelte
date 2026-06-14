<script lang="ts">
	import EnterView from "./components/EnterView.svelte";
	import VersionsView from "./components/VersionsView.svelte";

	let view = $state<"enter" | "versions">("enter");
	let code = $state("");
	let userId = $state("");

	function onEntered(c: string, uid: string) {
		code = c;
		userId = uid;
		view = "versions";
	}
</script>

<div class="flex min-h-screen items-center justify-center bg-surface-50-950 p-6">
	{#if view === "enter"}
		<EnterView onSuccess={onEntered} />
	{:else}
		<VersionsView {code} {userId} onBack={() => (view = "enter")} />
	{/if}
</div>
