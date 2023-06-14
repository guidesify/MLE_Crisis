import { AWS_KEY, AWS_SECRET } from '$env/static/private';
import AWS from 'aws-sdk';
import { json } from '@sveltejs/kit';
import type { RequestHandler } from './$types';

export const POST: RequestHandler = async ({ request }) => {
  try {
    let { endpoint, tweets } = await request.json();

    const region = 'us-east-1'; // Replace with your actual AWS region

    // Set up the AWS credentials
    AWS.config.update({
      accessKeyId: AWS_KEY,
      secretAccessKey: AWS_SECRET,
      region: region
    });

    // Create a SageMaker runtime instance
    const sagemaker = new AWS.SageMakerRuntime();

    // Construct the request parameters
    const params = {
      EndpointName: endpoint,
      Body: JSON.stringify({ Input: tweets }),
      ContentType: "application/json",
    };

    // Make the inference request
    const response = await sagemaker.invokeEndpoint(params).promise();

    // Parse the predictions from the response
    const { Body } = response;
    const predictionData = JSON.parse(Buffer.from(Body as ArrayBuffer).toString());

    // Render the page template with the predictions
    console.log("Number of Predictions:", predictionData.Output.length);
    return json(predictionData);
  } catch (error) {
    console.error("Error making inference request:", error);
    return json(error);
  }
};
