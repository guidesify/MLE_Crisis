<script lang="ts">
    import { supabase } from '$lib/supabaseClient'
    import Button from '$lib/components/Button.svelte'
    import Notification from '$lib/components/Notification.svelte'
  
    let [success, failure, loading] = [false, false, false]
    let [email, genTimeout] = ['', null]
    let clickHandler;
  
    const handleLogin = async () => {
      try {
        [loading, success, failure] = [true, false, false]
        const { error } = await supabase.auth.signInWithOtp({ email })
        clearTimeout(genTimeout)
        if (error) throw error
          success = true
      } catch (error) {
        if (error instanceof Error) {
          failure = true
        }
      } finally {
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
      }
    }
  </script>
  
{#if success}
  <Notification bind:clickHandler={clickHandler}>Check your email for the login link!</Notification>
{/if}

{#if failure}
  <Notification red bind:clickHandler={clickHandler}>Something went wrong. Please try again later.</Notification>
{/if}


  <div class="flex flex-col items-center justify-center py-2">
    <form class="w-full max-w-sm md:max-w-md mb-16" on:submit|preventDefault="{handleLogin}">
      <!-- <p class="text-xl font-bold">Crisis Detection Portal Login</p> -->
      <p class="dark:text-gray-300 mb-4 text-md">Sign in via magic link with your email below</p>
        <div class="flex items-center border-b border-teal-500 py-2">
          <input class="appearance-none bg-transparent border-none w-full text-gray-700 mr-3 py-1 px-2 leading-tight focus:outline-none dark:text-gray-300" type="text" placeholder="your@email.com" aria-label="Email" bind:value="{email}" />
          <Button primary label={loading ? 'Loading' : 'Get OTP'} on:click={() => {handleLogin}} disabled={loading} />
        </div>
    </form>
</div>

