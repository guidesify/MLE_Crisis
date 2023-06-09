import { SageMaker } from "@aws-sdk/client-sagemaker";
import { AWS_KEY, AWS_SECRET } from '$env/static/private';
import { json } from '@sveltejs/kit';
import type { RequestHandler } from './$types';

export const GET: RequestHandler = async ({  }) => {
  const region = 'us-east-1'; // Replace with your actual AWS region

  const sagemaker = new SageMaker({
    region,
    credentials: {
      accessKeyId: AWS_KEY,
      secretAccessKey: AWS_SECRET,
    },
  });

  const listEndpointsParams = {
    SortBy: 'CreationTime', // Optional: Specify a sorting order
    SortOrder: 'Descending', // Optional: Specify the sorting order (e.g., 'Ascending', 'Descending')
    MaxResults: 10, // Optional: Specify the maximum number of endpoints to retrieve
  };

  try {
    const response = await sagemaker.listEndpoints(listEndpointsParams);
    console.log(response.Endpoints.length);
    return json(response.Endpoints);
  } catch (error) {
    console.error('Error retrieving SageMaker endpoints:', error);
    throw error;
  }
};
