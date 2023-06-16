<script>
    import Endpoint from './Endpoint.svelte';
    import LabelDone from './LabelDone.svelte';
    let activeTab = 'endpoint';
    let activeClass = ' inline-block p-4 rounded-t-lg hover:text-gray-600 hover:bg-gray-50 dark:hover:bg-gray-800 dark:hover:text-gray-300 active text-gray-900 dark:text-gray-100 bg-gray-200 dark:bg-gray-900'
    let inactiveClass = ' inline-block p-4 hover:text-gray-600 hover:bg-gray-50 dark:hover:bg-gray-800 dark:hover:text-gray-300 text-blue-500 dark:text-blue-400'
  
    function setActiveTab(tab) {
      activeTab = tab;
      console.log(activeTab);
    }
  </script>
  
  <ul class="flex flex-wrap justify-center items-center text-sm font-medium text-center text-gray-500 border-b border-gray-200 dark:border-gray-700 dark:text-gray-400">
    <li class="mr-2">
      <!-- svelte-ignore a11y-invalid-attribute -->
      <a href="#" class={activeTab === 'endpoint' ? activeClass : inactiveClass} aria-current={activeTab === 'endpoint' ? 'page' : null} on:click={() => setActiveTab('endpoint')}>
        Endpoint List
      </a>
    </li>
    <li class="mr-2">
      <!-- svelte-ignore a11y-invalid-attribute -->
      <a href="#" class={activeTab === 'label' ? activeClass : inactiveClass} aria-current={activeTab === 'label' ? 'page' : null} on:click={() => setActiveTab('label')}>
        Labelled Work
      </a>
    </li>
  </ul>
  
  {#if activeTab === 'endpoint'}
    <Endpoint />
  {:else}
    <LabelDone />
  {/if}