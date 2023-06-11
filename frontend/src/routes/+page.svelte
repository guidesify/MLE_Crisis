<script>
  import { supabase } from "$lib/supabaseClient";
  import { onMount } from 'svelte'
  import Spinner from '$lib/components/Spinner.svelte';
  let endpoints = [];
  let loading = false;

  async function getEndpoints() {
	loading = true;

	const response = await fetch('/api/getEndpoint', {
	method: 'POST',
	headers: {
		'Content-Type': 'application/json',
	},
	body: JSON.stringify(
		{
			"endpoint": "test is successful"
		}
	)
	})
	.then(response => response.json())
	.then(data => {
		endpoints = data
		console.log('Success:', endpoints);
		loading = false;
	})
	.catch((error) => {
		console.error('Error:', error);
		loading = false;
	});
}

onMount(async () => {
    await getEndpoints();
  });

console.log(supabase)

</script>

<svelte:head>
	<title>Machine Learning Engineering - Crisis Dectection Demo</title>
	<meta name="description" content="Machine Learning Engineering - Crisis Dectection Demo" />
</svelte:head>

<div class="flex flex-col items-center justify-center p-8 mt-8">
	<p class="text-2xl font-bold">Machine Learning Engineering - Crisis Dectection Demo</p>
</div>

<!-- Make a flowbite table for endpoint -->
<div class="flex flex-col items-center justify-center py-8 px-32 mt-8">
	<!-- make a mini reload svg align on the right that calls getEndpoints-->
	<div class="flex justify-end ml-auto">
		{#if loading}
			<Spinner />
		{:else}
			<button type="button" on:click={getEndpoints}>
			<svg class="w-5 h-5 mr-1 text-gray-500 cursor-pointer hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-300" fill="currentColor" stroke="currentColor" viewBox="0 0 94.073 94.072" xml:space="preserve" xmlns="http://www.w3.org/2000/svg">
				<path d="M91.465 5.491a1.996 1.996 0 0 0-2.18.434l-8.316 8.316C72.046 5.057 60.125 0 47.399 0c-2.692 0-5.407.235-8.068.697C21.218 3.845 6.542 17.405 1.944 35.244a2 2 0 0 0 1.936 2.499h12.738a2 2 0 0 0 1.878-1.313c3.729-10.193 12.992-17.971 23.598-19.814a31.022 31.022 0 0 1 5.288-.456c8.428 0 16.299 3.374 22.168 9.5l-8.445 8.444a2.001 2.001 0 0 0 1.414 3.414H90.7a2 2 0 0 0 2-2V7.338c0-.808-.489-1.537-1.235-1.847zM90.192 56.328H77.455c-.839 0-1.59.523-1.878 1.312-3.729 10.193-12.992 17.972-23.598 19.814a31.03 31.03 0 0 1-5.288.456c-8.428 0-16.3-3.374-22.168-9.5l8.444-8.444a2 2 0 0 0-1.414-3.414H3.374a2 2 0 0 0-2 2v28.181a2 2 0 0 0 3.414 1.413l8.316-8.315c8.922 9.183 20.843 14.241 33.569 14.241 2.693 0 5.408-.235 8.069-.697 18.112-3.146 32.789-16.708 37.387-34.547.155-.6.023-1.234-.354-1.725a2.008 2.008 0 0 0-1.583-.775z"/>
			</svg>
			</button>
		{/if}
	</div>
	<!-- based on const endpoints -->
	<!-- table should be centered -->
	<table class="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
		<thead>
			<tr>
				<th class="px-4 py-2">Endpoint</th>
				<th class="px-4 py-2">Status</th>
			</tr>
		</thead>
		<tbody>
			{#if loading}
				<tr>
					<td class="px-4 py-2 flex items-center justify-end" colspan="2">
					<Spinner />
					</td>
				</tr> 
			{:else}
				{#if endpoints.length > 0}
					{#each endpoints as endpoint}
					<tr>
						<td class="border px-4 py-2">{endpoint}</td>
						<td class="border px-4 py-2">Active</td>
					</tr>
					{/each}
				{:else}
				<tr>
					<td class="px-4 py-2 text-center">No endpoints deployed currently</td>
					<td class="px-4 py-2 text-center">
						<button class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
							Train Base Model
						</button>
					</td>
				</tr>
				{/if}
			{/if}
		</tbody>
	</table>
</div>