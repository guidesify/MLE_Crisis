import { LambdaClient, InvokeCommand } from "@aws-sdk/client-lambda";
import { json } from "@sveltejs/kit";
import type { RequestHandler } from "./$types";
import { AWS_KEY, AWS_SECRET } from '$env/static/private';

export const GET: RequestHandler = async ({ }) => {
  const region = "us-east-1"; // Replace with your actual AWS region

  // Create an instance of the Lambda client
  const lambdaClient = new LambdaClient({
    region,
    credentials: {
        accessKeyId: AWS_KEY,
        secretAccessKey: AWS_SECRET,
      },
  });

  // No payload required for invoking the Lambda function

  // Define the input parameters for invoking the Lambda function
  const invokeParams = {
    FunctionName: "base-train", // Replace with your actual Lambda function name
    InvocationType: "RequestResponse",
  };

  try {
    // Invoke the Lambda function
    const response = await lambdaClient.send(new InvokeCommand(invokeParams));

    // Parse and process the response from the Lambda function
    const responseData = JSON.parse(
      new TextDecoder().decode(response.Payload)
    );

    // Return the processed response
    return json(responseData);
  } catch (error) {
    console.error("Error invoking Lambda function:", error);
    throw error;
  }
};
