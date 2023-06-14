<script>
    import { onMount } from 'svelte';
    import { afterUpdate } from 'svelte';
    import { supabase } from "$lib/supabaseClient";
    import Spinner from '$lib/components/Spinner.svelte';
    import Chart from 'chart.js/auto';
    import 'chartjs-adapter-moment';
    import moment from 'moment';
  import { init } from 'svelte/internal';

    let combinedArray = [];
    let output = { Output: [], Probabilities: [[]] };
    let timeInterval = 'hour'; // Default time interval is set to 'hour'
    let chartInstance = null;
    let canvasElement = null;
    let loading;

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

        // Extract timestamps and convert them to Moment.js objects
        const timestamps = filteredData.map((item) => moment(item.date));

        // Prepare labels and data for the chart
        const labels = timestamps.map((timestamp) => timestamp.format('lll')); // Format the timestamp using Moment.js
        const data = calculateSumByInterval(timestamps, timeInterval); // Calculate the sum of predictions by the selected interval

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

        console.log('Combined Array with Predictions:', combinedArray);
        // Check if the code is running in the browser
        if (typeof window !== 'undefined') {
            import('chartjs-plugin-zoom').then((zoomPlugin) => {
            Chart.register(zoomPlugin.default);
            createChart();
            });
        } else {
            createChart();
        }
        loading = false;
    }

    onMount(async () => {
        initLoad();
    });

    afterUpdate(() => {
        createChart(); // Recreate the chart after updating the component
    });

    // Change canvasElementClass depending on whether combinedArray is empty or not
  </script>

{#if loading}
    <div class="flex items-center justify-center h-screen">
        <Spinner /> Fetching predictions...
    </div>
{:else}
    <canvas bind:this={canvasElement} class="items-center justify-center mx-auto w-full sm:w-3/4 sm:max-w-6xl"></canvas>
{/if}