<script>
    import { onMount } from 'svelte';
    import { afterUpdate } from 'svelte';
    import { supabase } from "$lib/supabaseClient";
    import Spinner from '$lib/components/Spinner.svelte';
    import Chart from 'chart.js/auto';
    import 'chartjs-adapter-moment';
    import moment from 'moment';

    let combinedArray = [];
    let output = { Output: [], Probabilities: [[]] };
    let timeInterval = 'hour'; // Default time interval is set to 'hour'
    let chartInstance = null;
    let canvasElement = null;
    let loading = true;
    let threshold = 70;
    export let toLabelArray = [];

    async function fetchJSONData() {
      try {
        const response = await fetch('/data/tweets.json');
        const data = await response.text();
        return data;
      } catch (error) {
        console.error('Error fetching JSON data:', error);
        return '';
      }
    }
  
    async function getPredictions() {
      const endpoint = await supabase.from('model').select('endpoint').order('id', { ascending: false }).limit(1);
  
      const response = await fetch('/api/getPredictions', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          endpoint: endpoint.data[0].endpoint,
          tweets: combinedArray.map((tweet) => tweet.renderedContent),
        }),
      })
        .then((response) => response.json())
        .then((data) => {
          console.log('Success:', data);
          return data;
        })
        .catch((error) => {
          console.error('Error:', error);
          return null;
        });
      return response;
    }


    function createChart() {
        const ctx = canvasElement.getContext('2d');
        const filteredData = combinedArray.filter((item) => item.prediction === 1);
        const filteredDataPriority = combinedArray.filter((item) => item.prediction === 1 && item.probabilities[1] > threshold/100);

        // Extract timestamps and convert them to Moment.js objects
        const timestamps = filteredData.map((item) => moment(item.date));
        const timestampsPriority = filteredDataPriority.map((item) => moment(item.date));

        // Prepare labels and data for the chart
        const labels = timestamps.map((timestamp) => timestamp.format('lll')); // Format the timestamp using Moment.js
        const data = calculateSumByInterval(timestamps, timeInterval); // Calculate the sum of predictions by the selected interval
        const dataPriority = calculateSumByInterval(timestampsPriority, timeInterval); // Calculate the sum of predictions by the selected interval

        // Create the chart
        if (chartInstance) {
            chartInstance.destroy();
        }
        chartInstance = new Chart(ctx, {
            type: 'line',
            data: {
            labels: labels,
            datasets: [
                {
                label: 'Sum of Predictions',
                data: data,
                borderColor: 'rgb(75, 192, 192)',
                tension: 0.1,
                },
                {
                    label: 'Priority Tweets',
                    data: dataPriority,
                    borderColor: 'rgb(255, 99, 132)',
                    tension: 0.1,
                }
            ],
            },
            options: {
            scales: {
                x: {
                ticks: {
                    autoSkip: true, // Enable automatic skipping of ticks
                    autoSkipPadding: 5, // Set the padding between ticks
                    maxRotation: 0, // Set the maximum rotation angle for tick labels
                },
                type: 'time',
                time: {
                    unit: timeInterval, // Use the selected time interval
                    displayFormats: {
                    hour: 'lll', // Format for displaying hour labels
                    minute: 'lll', // Format for displaying minute labels
                    second: 'lll', // Format for displaying second labels
                    },
                },
                title: {
                    display: true,
                    text: 'Time',
                },
                },
                y: {
                beginAtZero: true,
                title: {
                    display: true,
                    text: 'Sum of Predictions',
                },
                },
            },
            plugins: {
                tooltip: {
                mode: 'x', // Show tooltip on the x-axis
                },
                zoom: {
                    zoom: {
                    wheel: {
                        enabled: true,
                    },
                    pinch: {
                        enabled: true
                    },
                    mode: 'xy',
                    }
                },
            },
            },
        });
    }

    function calculateSumByInterval(timestamps, interval) {
        const sums = {};

        timestamps.forEach((timestamp) => {
            const roundedTimestamp = timestamp.startOf(interval).toISOString(); // Round the timestamp to the start of the selected interval
            if (sums[roundedTimestamp]) {
            sums[roundedTimestamp]++;
            } else {
            sums[roundedTimestamp] = 1;
            }
        });

        // Convert the sums object into an array of data points
        const data = Object.keys(sums).map((roundedTimestamp) => {
            return {
            x: moment(roundedTimestamp).toISOString(),
            y: sums[roundedTimestamp],
            };
        });

        return data;
    }

    function getUncertainTweets() {
        // Filter combinedArray to only include tweets with probability 1st or 2nd item between 0.4 and 0.6
        const filteredData = combinedArray.filter((item) => item.probabilities[1] > 0.50 && item.probabilities[1] < 0.51);
        return filteredData;
    }

    async function ChartInit() {
        let success = false;
        let attempts = 0

        while (!success && attempts < 5) {
            attempts++;
            try {
                if (typeof window !== 'undefined') {
                    import('chartjs-plugin-zoom').then((zoomPlugin) => {
                    Chart.register(zoomPlugin.default);
                    createChart();
                    });
                } else {
                    createChart();
                }
                success = true;
            } catch (error) {
                console.error('Error:', error);
                await new Promise((resolve) => setTimeout(resolve, 2000));
            }
        }

    }

    async function initLoad() {
        loading = true;
        const data = await fetchJSONData();
        const lines = data.split('\n'); // Split the text into separate lines

        for (let i = 0; i < lines.length; i++) {
        const tweet = JSON.parse(lines[i]);
        combinedArray.push(tweet);
        }

        console.log('Number of tweets:', combinedArray.length);

        // Call getPredictions function and update combinedArray with predictions
        output = await getPredictions();
        if (output && output.Output.length === combinedArray.length) {
        for (let i = 0; i < combinedArray.length; i++) {
            combinedArray[i].prediction = output.Output[i]; // Assuming the output is in the same order as the tweets
            combinedArray[i].probabilities = output.Probabilities[i];
        }
        }

        // console.log('Combined Array with Predictions:', combinedArray);
        toLabelArray = getUncertainTweets();
        // console.log('Uncertain Tweets:', toLabelArray);

        // Check if the code is running in the browser
        await ChartInit();
        loading = false;
    }

    onMount(async () => {
        initLoad();
    });

    afterUpdate(async () => {
        await ChartInit(); // Recreate the chart after updating the component
    });

    // Change canvasElementClass depending on whether combinedArray is empty or not
  </script>

{#if loading}
    <div class="flex items-center justify-center h-screen">
        <Spinner /> Fetching predictions...
    </div>
{:else}
<!-- Make a slider for threshold between 0.7-0.9 -->
<div class="flex flex-col items-end mx-auto w-full sm:w-3/4 sm:max-w-6xl">
    <input type="range" min="70" max="90" step="1" bind:value={threshold} />
    <span class="text-sm text-gray-500">Threshold: {threshold}%</span>
</div>
<canvas bind:this={canvasElement} class="items-center justify-center mx-auto w-full sm:w-3/4 sm:max-w-6xl"></canvas>
{/if}