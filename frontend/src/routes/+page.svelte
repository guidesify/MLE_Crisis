<script>
  import { onMount } from 'svelte'

  let endpoints = [];

  async function getEndpoints() {

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
		console.log('Success:', data);
	})
	.catch((error) => {
		console.error('Error:', error);
	});
}

onMount(() => {
	endpoints = getEndpoints()
	console.log(endpoints)

})

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
			{#if endpoints.length > 0}
			{#each endpoints as endpoint}
			<tr>
				<td class="border px-4 py-2">{endpoint}</td>
				<td class="border px-4 py-2">Active</td>
			</tr>
			{/each}
			{:else}
			<!-- Just say no endpoints deployed currently combined as colspan 2 -->
			<tr>
				<td class="border px-4 py-2 text-center" colspan="2">No endpoints deployed currently</td>
			</tr>
			{/if}
		</tbody>
	</table>
</div>