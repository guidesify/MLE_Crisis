<script lang="ts">
  import { page } from '$app/stores';
  import { supabase } from "$lib/supabaseClient";
  import type { AuthSession } from '@supabase/supabase-js'
  import {sessionStore} from '$lib/stores'
  import { onMount } from 'svelte'
  import Login from '$lib/components/Login.svelte';
  import Tab from './Tab.svelte';
//   import {tooltip} from '$lib/components/tooltip';
  export let session: AuthSession | null = null

  onMount(async () => {
	const res = await supabase.auth.getSession()
	if (res) {
	session = res.data.session
	sessionStore.set(session)
	}

	supabase.auth.onAuthStateChange((_event, _session) => {
	session = _session
	sessionStore.set(session)
	})
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

{#if session}
<Tab />
{:else}
<Login />
{/if}
<div class=pb-16></div>
