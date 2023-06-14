<script lang="ts">
  import { page } from '$app/stores';
  import { supabase } from "$lib/supabaseClient";
  import type { AuthSession } from '@supabase/supabase-js'
  import { get } from 'svelte/store';
  import {sessionStore, baseTrainStatusStore} from '$lib/stores'
  import { onMount } from 'svelte'
  import {tooltip} from '$lib/components/tooltip';
  import Spinner from '$lib/components/Spinner.svelte';
  import Login from '$lib/components/Login.svelte';
  import Notification from "$lib/components/Notification.svelte";
  let endpoints = [];
  let body;
  let [success, failure, loading, genTimeout] = [false, false, false, null];
  let clickHandler;
  let defaultModel = '';
  export let session: AuthSession | null = null
  export let baseStatus = get(baseTrainStatusStore);

  async function getEndpoints() {
	loading = true;

	const response = await fetch('/api/getEndpoint', {
	method: 'GET',
	headers: {
		'Content-Type': 'application/json',
	}
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

async function getActiveEndpoint() {
	// Get the newest active endpoint
	const res = await supabase.from('model').select('endpoint').order('id', {ascending: false}).limit(1)
	// console.log(res)
	if (res.status < 300) {
		return res.data[0].endpoint
	} else {
		return null
	}
}

async function updateActiveEndpoint(endpoint) {
	// console.log(endpoint)
	const res = await supabase.from('model').insert([{endpoint: endpoint}])
	// console.log(res)
	if (res.status < 300) {
		defaultModel = endpoint
		return endpoint
	} else {
		return null
	}
}

async function trainBaseModel() {
	[loading, success, failure] = [true, false, false]
	clearTimeout(genTimeout)

	const response = await fetch('/api/trainBase', {
	method: 'GET',
	headers: {
		'Content-Type': 'application/json',
	},
	})
	.then(response => response.json())
	.then(data => {
		body = data['body']
		console.log('Success:', body);
		loading = false;
		// success true if body contains successfully else failure true
		if (body.includes('successfully')) {
			success = true;
			baseTrainStatusStore.set(true)
			baseStatus = get(baseTrainStatusStore);
		} else {
			failure = true;
		}
	})
	.catch((error) => {
		console.error('Error:', error);
		loading = false;
		failure = true;
	})
	.finally(() => {
        let alert_type = success ? 'alert' : 'alert2'
        if (document.getElementById(alert_type)) {
          document.getElementById(alert_type).classList.remove('transition-opacity', 'duration-300', 'ease-out', 'opacity-0', 'hidden')
        }
        genTimeout = setTimeout(() => {
          let dur = clickHandler(alert_type, alert_type)()
          setTimeout(() => {
            [loading, success, failure] = [false, false, false]
          }, dur)
        }, 5000)
	})
}

const logout = async () => {
      await supabase.auth.signOut()
      window.location.href = '/';
    }

onMount(async () => {
    await getEndpoints();
	const res = await supabase.auth.getSession()
    if (res) {
      session = res.data.session
      sessionStore.set(session)
    }

    supabase.auth.onAuthStateChange((_event, _session) => {
      session = _session
      sessionStore.set(session)
    })

	defaultModel = await getActiveEndpoint()
	console.log(defaultModel)

  });
</script>

<svelte:head>
	<title>Machine Learning Engineering - Admin Portal</title>
	<meta name="description" content="Machine Learning Engineering - Admin Portal" />
	<meta property="og:title" content="Machine Learning Engineering - Admin Portal" />
	<meta property="og:description" content="Machine Learning Engineering - Admin Portal" />
</svelte:head>

{#if $page.url.pathname === '/admin'}
<div class="flex flex-col items-center justify-center p-8 mx-auto mt-8">
	<p class="text-2xl font-bold">Crisis Detection Admin Portal</p>
</div>
{/if}

{#if success}
  <Notification bind:clickHandler={clickHandler}>Training job successfully created, check back in awhile.</Notification>
{/if}

{#if failure}
  <Notification red bind:clickHandler={clickHandler}>Something went wrong. Please contact admin.</Notification>
{/if}

{#if session}
<!-- Make a flowbite table for endpoint -->
<div class="flex flex-col items-center justify-center py-8 mx-auto mt-8 w-full sm:w-3/4 sm:max-w-2xl">
	<div class="flex justify-end ml-auto pb-4">
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
	<table class="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
		<thead>
			<tr>
				<th class="border-gray-300 border px-4 py-2">Endpoint</th>
				<th class="border-gray-300 border px-4 py-2">Status</th>
				<th class="border-gray-300 border px-4 py-2">Actions</th>
			</tr> 
		</thead>
		<tbody>
			{#if loading}
				<tr>
					<td class="border-gray-300 border px-4 py-2 text-center" colspan=3>
						<div class="flex items-center justify-center">
							<Spinner /> Refreshing Endpoint List...
						</div>
					</td>
				</tr>
			{:else}
				{#if endpoints.length > 0}
					{#each endpoints as endpoint}
					<tr>
						<td class="border-gray-300 border px-4 py-2">{endpoint["EndpointName"]}</td>
						<td class="border-gray-300 border px-4 py-2">{endpoint["EndpointStatus"]}</td>
						<td class="border-gray-300 border px-4 py-2 text-center">
							{#if defaultModel == endpoint["EndpointName"]}
							Selected
							{:else}
							<button class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded disabled:opacity-50" on:click={updateActiveEndpoint(endpoint["EndpointName"])} disabled={endpoint["EndpointStatus"] != "InService"}>
								Set Default
							</button>
							{/if}
						</td>					
					</tr>
					{/each}
				{:else}
				<tr>
					<td class="border-gray-300 border px-4 py-2 text-center" colspan=2>No endpoints deployed currently</td>
					<td class="border-gray-300 border px-4 py-2 text-center">
						<button class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded disabled:opacity-50" on:click={trainBaseModel} disabled={baseStatus}>
							Train Base Model
						</button>
					</td>
				</tr>
				{/if}
			{/if}
		</tbody>
	</table>

	<!-- Log out button -->
	<div class="flex justify-center mt-8">
		<button class="bg-red-500 hover:bg-red-600 text-white font-bold py-2 px-4 rounded" on:click={logout}>
			Log Out
		</button>
	</div>
</div>
{:else}
<Login />
{/if}