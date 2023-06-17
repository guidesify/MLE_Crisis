import { LambdaClient, InvokeCommand } from "@aws-sdk/client-lambda";
import { json } from "@sveltejs/kit";
import type { RequestHandler } from "./$types";
import { AWS_KEY, AWS_SECRET } from '$env/static/private';

export const POST: RequestHandler = async ({ request }) => {
  const dataArray = await request.json();
//   Clean the array into [{"target": label, "text": text}, ..."}]
  const cleanArray = dataArray["workArray"].map((item) => {
        return {"target": item.label, "text": item.text}
    });
  const region = "us-east-1"; // Replace with your actual AWS region

  // Create an instance of the Lambda client
//   const lambdaClient = new LambdaClient({
//     region,
//     credentials: {
//         accessKeyId: AWS_KEY,
//         secretAccessKey: AWS_SECRET,
//       },
//   });

//   // No payload required for invoking the Lambda function

//   // Define the input parameters for invoking the Lambda function
//   const invokeParams = {
//     FunctionName: "incremental-train", // Replace with your actual Lambda function name
//     InvocationType: "RequestResponse",
//   };

  try {
//     // Invoke the Lambda function
//     const response = await lambdaClient.send(new InvokeCommand(invokeParams));

//     // Parse and process the response from the Lambda function
//     const responseData = JSON.parse(
//       new TextDecoder().decode(response.Payload)
//     );

//     // Return the processed response
//     return json(responseData);
        console.log(cleanArray);
        return json(cleanArray);
    } catch (error) {
    console.error("Error invoking Lambda function:", error);
    return json(error)
  }
};
