<script lang="ts">
    import moment from 'moment';
    import { supabase } from "$lib/supabaseClient";
    import type { AuthSession } from '@supabase/supabase-js'
    import { onMount } from 'svelte';
    import Spinner from '$lib/components/Spinner.svelte';
    import { construct_svelte_component } from 'svelte/internal';
    export let toLabelArray = [];
    let workArray = [];
    let cleanedToLabelArray = [];
    let loading
    export let session: AuthSession | null = null

    async function alreadyLabelled() {
        workArray = await supabase.from('labelled').select()
        // console.log(workArray)
        // Need id and submitted
        workArray = workArray.data.map((item) => {
          return {
            id: item.id,
            submitted: item.submitted
          }
        }
        )
        // console.log("Work array: ", workArray)
      }
    

    async function cleanToLabelArray() {
        cleanedToLabelArray = toLabelArray.filter((item) => {
            return !workArray.some((item2) => {
              return item.id === item2.id
            })
          })
        console.log("To label array: ", toLabelArray)
        console.log("Cleaned to label array: ", cleanedToLabelArray)
    }

    async function updateLabel(tweetID, label, text) {
        loading = true;
        const res = await supabase
          .from('labelled')
          .upsert([{ id: tweetID, label: label, text: text, submitted: false }])
          // console.log("Response from upsert: ", res)
        await groupFunction();
        loading = false;
    }

    async function groupFunction() {
        await alreadyLabelled();
        await cleanToLabelArray();
    }

    onMount(async () => {
        const res = await supabase.auth.getSession();
        if (res) {
            session = res.data.session;
        }

        await groupFunction();

        console.log(cleanedToLabelArray)
    })

    $: {
        console.log("Arrays have changed:", toLabelArray)
        groupFunction();
    }

</script>

<!-- Table to show toLabelArray -->
{#if cleanedToLabelArray.length > 0 && session}
<div class="custom-overflow items-center justify-center py-8 mx-auto w-11/12 sm:w-3/4 sm:max-w-4xl">
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
    {#if loading}
    <tr>
      <td class="border-gray-300 px-4 py-2 text-center" colspan=5>
        <div class="flex items-center justify-center">
          <Spinner /> Loading...
        </div>
      </td>
    </tr>
    {:else}
    {#each cleanedToLabelArray as tweet}
    <tr>
      <td class="border px-4 py-2">{tweet.id}</td>
      <td class="border px-4 py-2">{tweet.renderedContent}</td>
      <td class="border px-4 py-2">{moment(tweet.date).format('MMM DD, YYYY hh:mm:ss A')}</td>
      <td class="border px-4 py-2">{tweet.prediction}</td>
      <td class="justify-center items-center border px-4 space-x-2">
        <div class="flex space-x-2">
            <button class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded" on:click={() => updateLabel(tweet.id, 0, tweet.renderedContent)}>
                0
              </button>
              <button class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded" on:click={() => updateLabel(tweet.id, 1, tweet.renderedContent)}>
                1
              </button>
        </div>
      </td>
    </tr>
    {/each}
    {/if}
  </tbody>
</table>
</div>
{/if}
