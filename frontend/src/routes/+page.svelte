<script lang="ts">
  import Chart from '$lib/components/Chart.svelte'
  import LabelWork from '$lib/components/LabelWork.svelte'
  import logo from '$lib/images/Main Logo.svg';
  let toLabelArray = [];

</script>

<svelte:head>
	<title>Machine Learning Engineering - Crisis Dectection Demo</title>
	<meta name="description" content="Machine Learning Engineering - Crisis Dectection Demo" />
	<meta property="og:title" content="Machine Learning Engineering - Crisis Dectection Demo" />
	<meta property="og:description" content="Machine Learning Engineering - Crisis Dectection Demo" />
	<meta property="og:image" content={logo} />
</svelte:head>

<div class="flex flex-col items-center justify-center p-8 mx-auto mt-8">
	<p class="text-2xl font-bold">Machine Learning Engineering - Crisis Dectection Demo</p>
</div>

<Chart bind:toLabelArray={toLabelArray} />
<LabelWork bind:toLabelArray={toLabelArray} />
<div class=pb-16></div>
