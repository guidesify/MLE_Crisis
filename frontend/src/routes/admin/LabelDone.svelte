<script>
    import { supabase } from "$lib/supabaseClient";
    import { onMount } from 'svelte';
    import Spinner from '$lib/components/Spinner.svelte';
    import Notification from "$lib/components/Notification.svelte";

    let body;
    let [success, failure, loading, genTimeout] = [false, false, false, null];
    let clickHandler;
    let workArray = [];
    
    async function alreadyLabelled() {
        // must be submitted false
        workArray = await supabase.from('labelled').select().eq('submitted', false)
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

    async function submit() {
        loading = true;
        
        const response = await fetch('/api/trainIncremental', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({workArray})
        })
        .then(response => response.json())
        .then(data => {
            body = data['body']
            console.log('Success:', body);
            loading = false;
            if (body.includes('successfully')) {
                success = true;
                // Change Supabase submitted to true one shot by adding submitted: true to all items in workArray
                const updateArray = workArray.map((item) => {
                    return {
                        id: item.id,
                        submitted: true
                    }
                })
                supabase.from('labelled').upsert(updateArray)
                .then(res => {
                    console.log("Response from upsert: ", res)
                })

                // Remove all items from workArray
                workArray = []
            } else {
                failure = true;
            }
            loading = false;
        })
        .catch((error) => {
            console.error('Error:', error);
            failure = true;
            loading = false;
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

    onMount(async () => {
        await alreadyLabelled();
        console.log("Work array: ", workArray)
    })
</script>

{#if success}
  <Notification bind:clickHandler={clickHandler}>Training job successfully created, check back in awhile.</Notification>
{/if}

{#if failure}
  <Notification red bind:clickHandler={clickHandler}>Something went wrong. Please contact admin.</Notification>
{/if}

{#if workArray.length > 0}
{#if loading}
<div class="flex items-center justify-center mt-16">
    <Spinner /> Submitting and cleaning up data...
</div>
{:else}
<!-- button for submitting work done to lambda function -->
<div class="flex flex-col items-center justify-center mt-8 mx-auto w-full sm:w-3/4 sm:max-w-4xl">
    <button class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded" on:click={() => submit()}>
        Submit for Incremental Training
    </button>
</div>
<div class="flex flex-col items-center justify-center py-8 mx-auto w-full sm:w-3/4 sm:max-w-4xl">
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
{/if}
{:else}
<div class="flex flex-col items-center justify-center py-8 mx-auto mt-8 w-full sm:w-3/4 sm:max-w-4xl">
    <p class="text-gray-500 dark:text-gray-400">No tweets have been labelled yet.</p>
</div>
{/if}
