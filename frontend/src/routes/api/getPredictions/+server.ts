import { SageMakerRuntime, InvokeEndpointCommand } from "@aws-sdk/client-sagemaker-runtime";
import { AWS_KEY, AWS_SECRET } from '$env/static/private';
import { json } from '@sveltejs/kit';
import type { RequestHandler } from './$types';

export const POST: RequestHandler = async ({ request }) => {
    let { endpoint, tweets } = await request.json();
    const region = 'us-east-1'; // Replace with your actual AWS region
  
    // Make a request to SageMaker for predictions
    const sagemaker = new SageMakerRuntime({
        region,
        credentials: {
          accessKeyId: AWS_KEY,
          secretAccessKey: AWS_SECRET,
        },
      });

    // Construct the request parameters
    const params = {
        EndpointName: endpoint,
        Body: JSON.stringify({ Input: tweets }),
        ContentType: "application/json",
    };

    try {
        // Make the inference request
        const command = new InvokeEndpointCommand(params);
        const response = await sagemaker.send(command);

        // Parse the predictions from the response
        const { Body } = response;
        const predictionData = JSON.parse(Buffer.from(Body).toString());

        // Render the page template with the predictions
        console.log("Number of Predictions:", predictionData.Output.length);
        return json(predictionData);
    } catch (error) {
        console.error("Error making inference request:", error);
        throw error;
    }
    };
  




