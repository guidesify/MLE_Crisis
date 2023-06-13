<script>
	export let title_custom;
	export let x;
	export let y;
</script>
<div style="top: {y + 5}px; left: {x + 5}px;" class="dark:bg-gray-700 dark:text-gray-200 dark:border-gray-600 text-sm border-gray-200 z-50">
        {title_custom}
</div>

<style>
	div {
		border: 1px solid #ddd;
		background: white;
		border-radius: 8px;
		padding: 0.4rem 0.6rem;
		position: absolute;
	}
</style>
