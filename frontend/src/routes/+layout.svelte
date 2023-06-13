<script context="module">
	export async function load({ page }) {
	  const { host } = page.request.headers;
	  return {
		props: {
		  currentUrl: `https://${host}${page.path}`,
		},
	  };
	}
  </script>

<script>
	import "../app.css";
    import "flowbite/dist/flowbite.css";
	import Header from '$lib/components/Header.svelte';
	import './styles.css';

	export let currentUrl;
</script>

<svelte:head>
	<meta prefix="og: http://ogp.me/ns#" />
	<meta property="og:url" content="{currentUrl}" />
	<meta name="viewport" content="width=device-width, initial-scale=1.0" />
</svelte:head>

<div class="app">
	<Header />

		<slot />

	<footer class="fixed bottom-0 w-full bg-gray-100">
		<p>Sign up on <a href="https://app.guidesify.com">app.guidesify.com</a> for 50 free credits.</p>
	</footer>
</div>

<style>
	.app {
		display: flex;
		flex-direction: column;
		min-height: 100vh;
	}


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
