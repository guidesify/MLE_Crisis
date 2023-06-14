import { json } from '@sveltejs/kit';
import { AWS_KEY, AWS_SECRET } from '$env/static/private';
import aws4 from 'aws4';
import fetch from 'node-fetch';
import type { RequestHandler } from './$types';

export const POST: RequestHandler = async ({ request }) => {
  try {
    let { endpoint, tweets } = await request.json();

    const region = 'us-east-1'; // Replace with your actual AWS region

    // Construct the request parameters
    const params = {
      host: `runtime.sagemaker.${region}.amazonaws.com`,
      path: `/endpoints/${endpoint}/invocations`,
      service: 'sagemaker',
      region: region,
      body: JSON.stringify({ Input: tweets }),
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
    };

    // Sign the request using aws4
    const signedRequest = aws4.sign(params, {
      accessKeyId: AWS_KEY,
      secretAccessKey: AWS_SECRET,
    });

    // Make the inference request using node-fetch
    const response = await fetch(`https://${params.host}${params.path}`, {
      method: signedRequest.method,
      headers: signedRequest.headers,
      body: signedRequest.body,
    });

    // Parse the predictions from the response
    const predictionData = await response.json();

    // Render the page template with the predictions
    console.log("Number of Predictions:", predictionData.Output.length);
    return json(predictionData);
  } catch (error) {
    console.error("Error making inference request:", error);
    return json(error);
  }
};
