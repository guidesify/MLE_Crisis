import { LambdaClient, InvokeCommand } from "@aws-sdk/client-lambda";
import { AWS_KEY, AWS_SECRET } from "$env/static/private";
import { json } from "@sveltejs/kit";
import type { RequestHandler } from "./$types";

export const POST: RequestHandler = async ({request }) => {
  const { endpoint, tweets } = await request.json();
  console.log(endpoint)
  const region = "us-east-1"; // Replace with your actual AWS region

  const lambdaClient = new LambdaClient({
    region,
    credentials: {
        accessKeyId: AWS_KEY,
        secretAccessKey: AWS_SECRET,
      },
  });
  const invokeParams = {
    FunctionName: "get-predictions",
    Payload: JSON.stringify({ body: { endpoint, tweets } }),
  };

  try {
    const response = await lambdaClient.send(new InvokeCommand(invokeParams));
    const responseData = JSON.parse(
      new TextDecoder().decode(response.Payload)
    );

    // Get the body only and parse it as JSON
    const predictionData = JSON.parse(responseData.body);
    console.log("Number of Predictions:", predictionData.Output.length);
    return json(predictionData);
  } catch (error) {
    console.log(error);
    return json(error);
  }
}
