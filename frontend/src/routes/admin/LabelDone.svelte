<script>
    import { supabase } from "$lib/supabaseClient";
    import { onMount } from 'svelte';
    import Spinner from '$lib/components/Spinner.svelte';
    let workArray = [];
    let loading;
    
    async function alreadyLabelled() {
        workArray = await supabase.from('labelled').select()
        // console.log(workArray)
        // Need id and submitted
        workArray = workArray.data.map((item) => {
          return {
            id: item.id,
            label: item.label,
            text: item.text
          }
        }
        )
        // console.log("Work array: ", workArray)
      }

    onMount(async () => {
        await alreadyLabelled();
        console.log("Work array: ", workArray)
    })
</script>

{#if workArray.length > 0}
<div class="flex flex-col items-center justify-center py-8 mx-auto mt-8 w-full sm:w-3/4 sm:max-w-4xl">
    <table class="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
      <thead>
        <tr>
            <th class="px-4 py-2">ID</th>
            <th class="px-4 py-2">Label</th>
            <th class="px-4 py-2">Text</th>
        </tr>
      </thead>
      <tbody>
        {#each workArray as item}
        <tr>
            <td class="px-4 py-2">{item.id}</td>
            <td class="px-4 py-2">{item.label ? "1" : "0"}</td>
            <td class="px-4 py-2">{item.text}</td>
        </tr>
        {/each}
      </tbody>
    </table>
</div>
{:else}
<div class="flex flex-col items-center justify-center py-8 mx-auto mt-8 w-full sm:w-3/4 sm:max-w-4xl">
    <p class="text-gray-500 dark:text-gray-400">No tweets have been labelled yet.</p>
</div>
{/if}
