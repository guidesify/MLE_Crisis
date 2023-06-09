<script>
	import "../app.css";
	import "flowbite/dist/flowbite.css";
	import Header from './Header.svelte';
</script>

<div class="">
	<Header />

		<slot />

	<footer class="fixed bottom-0 w-full bg-gray-100">
		<p>Sign up on <a href="https://app.guidesify.com">app.guidesify.com</a> for 50 free credits.</p>
	</footer>
</div>

<style>

	footer {
		display: flex;
		flex-direction: column;
		justify-content: center;
		align-items: center;
		padding: 12px;
	}

	footer a {
		font-weight: bold;
	}

	@media (min-width: 480px) {
		footer {
			padding: 12px 0;
		}
	}
</style>
