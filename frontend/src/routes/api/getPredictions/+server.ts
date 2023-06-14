import axios from 'axios';
import CryptoJS from 'crypto-js';

import { AWS_KEY, AWS_SECRET } from '$env/static/private';
import { json } from '@sveltejs/kit';
import type { RequestHandler } from './$types';

export const POST: RequestHandler = async ({ request }) => {
  try {
    let { endpoint, tweets } = await request.json();
    const region = 'us-east-1'; // Replace with your actual AWS region
  
    // Construct the request parameters
    const params = {
      EndpointName: endpoint,
      Body: JSON.stringify({ Input: tweets }),
      ContentType: 'application/json',
    };

    // Generate the AWS signature
    const date = new Date().toISOString().replace(/[:\-]|\.\d{3}/g, '');
    const canonicalRequest = `${request.method}\n${request.path}\n\nhost:${request.host}\nx-amz-date:${date}\n\nhost;x-amz-date\n${CryptoJS.SHA256(JSON.stringify(params)).toString(CryptoJS.enc.Hex)}`;
    const stringToSign = `AWS4-HMAC-SHA256\n${date}\n${date.substr(0, 8)}/${region}/sagemaker/aws4_request\n${CryptoJS.SHA256(canonicalRequest).toString(CryptoJS.enc.Hex)}`;
    const signingKey = CryptoJS.HmacSHA256(date.substr(0, 8), CryptoJS.HmacSHA256(region, CryptoJS.HmacSHA256('sagemaker', CryptoJS.HmacSHA256('aws4_request', `AWS4${AWS_SECRET}`))));
    const signature = CryptoJS.HmacSHA256(stringToSign, signingKey).toString(CryptoJS.enc.Hex);
    const authorizationHeader = `AWS4-HMAC-SHA256 Credential=${AWS_KEY}/${date.substr(0, 8)}/${region}/sagemaker/aws4_request, SignedHeaders=host;x-amz-date, Signature=${signature}`;

    // Make the inference request
    const url = `https://runtime.sagemaker.${region}.amazonaws.com/endpoints/${endpoint}/invocations`;
    const headers = {
      'Content-Type': 'application/json',
      'X-Amz-Date': date,
      'Authorization': authorizationHeader,
    };
    const response = await axios.post(url, params.Body, { headers });

    // Parse the predictions from the response
    const predictionData = JSON.parse(response.data);

    // Render the page template with the predictions
    console.log('Number of Predictions:', predictionData.Output.length);
    return json(predictionData);
  } catch (error) {
    console.error('Error making inference request:', error);
    return json(error);
  }
};
