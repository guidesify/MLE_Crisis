<script>
    import moment from 'moment';
    import { supabase } from "$lib/supabaseClient";
    import { get } from 'svelte/store';
    import { sessionStore } from '$lib/stores';
    import {onMount} from 'svelte';
    export let toLabelArray = [];
    export let session = get(sessionStore);
    let workArray = [];

    async function alreadyLabelled() {
        workArray = await supabase.from('labelled').select()
        console.log(workArray)
        workArray = workArray.data.map((item) => item.id)
        console.log("Already labelled: ", workArray)
    }

    async function updateLabel(tweetID, label) {

    }

    onMount(async () => {
        await alreadyLabelled();
    })
</script>

<!-- Table to show toLabelArray -->
<div class="flex flex-col items-center justify-center py-8 mx-auto mt-8 w-full sm:w-3/4 sm:max-w-4xl">

<table class="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
  <thead>
    <tr>
      <th class="px-4 py-2">ID</th>
      <th class="px-4 py-2">Tweet</th>
      <th class="px-4 py-2">Date</th>
      <th class="px-4 py-2">Prediction</th>
      <th class="px-4 py-2">Action</th>
    </tr>
  </thead>
  <tbody>
    {#each toLabelArray as tweet}
    <tr>
      <td class="border px-4 py-2">{tweet.id}</td>
      <td class="border px-4 py-2">{tweet.renderedContent}</td>
      <td class="border px-4 py-2">{moment(tweet.date).format('MMM DD, YYYY hh:mm:ss A')}</td>
      <td class="border px-4 py-2">{tweet.prediction}</td>
      <td class="justify-center items-center border px-4 space-x-2">
        <div class="flex space-x-2">
            <button class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded" on:click={() => updateLabel(tweet.id, 0)}>
                0
              </button>
              <button class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded" on:click={() => updateLabel(tweet.id, 1)}>
                1
              </button>
        </div>
      </td>
    </tr>
    {/each}
  </tbody>
</table>
</div>
