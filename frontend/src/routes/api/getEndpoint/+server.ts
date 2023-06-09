import AWS from 'aws-sdk';
import { AWS_KEY, AWS_SECRET } from '$env/static/private';
import type { RequestHandler } from './$types';
import { json } from '@sveltejs/kit'


export const POST: RequestHandler = async ({ request }) => {
  let {endpoint} = await request.json();
  console.log(endpoint)
  const credentials = new AWS.Credentials({
    accessKeyId: AWS_KEY,
    secretAccessKey: AWS_SECRET,
  });

  const region = 'us-east-1'; // Replace with your actual AWS region

  const sagemaker = new AWS.SageMaker({ credentials, region });

  const listEndpointsParams: AWS.SageMaker.ListEndpointsInput = {
    SortBy: 'CreationTime', // Optional: Specify a sorting order
    SortOrder: 'Descending', // Optional: Specify the sorting order (e.g., 'Ascending', 'Descending')
    MaxResults: 10, // Optional: Specify the maximum number of endpoints to retrieve
  };

  try {
    const response = await sagemaker.listEndpoints(listEndpointsParams).promise();
    console.log(response.Endpoints)
    return json(response.Endpoints);
  } catch (error) {
    console.error('Error retrieving SageMaker endpoints:', error);
    throw error;
  }
}
