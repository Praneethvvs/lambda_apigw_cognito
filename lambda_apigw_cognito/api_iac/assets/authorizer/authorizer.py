import json
import os
import boto3 

ssm_client = boto3.client('ssm')

def handler(event, context):
    # Extract the token (usually from Authorization header)
    print(event)
    token = event['authorizationToken']
    
    # Get the API Gateway URL from environment variable

    parameter_name = "/DocQuerySystemRAGApp/apigw_resource_arn"
    response = ssm_client.get_parameter(
                Name=parameter_name,
                WithDecryption=True  # Set to True if the parameter is encrypted (SecureString)
            )
    resource_arn = response['Parameter']['Value']
    print(f"Retrieved parameter value: {resource_arn}")


    # If the token is valid, create an allow policy, otherwise deny
    if token == 'validToken':
        effect = "Allow"
    else:
        effect = "Deny"

    policy = {
        'principalId': 'user',
        'policyDocument': {
            'Version': '2012-10-17',
            'Statement': [
                {
                    'Effect': f'{effect}',
                    'Action': 'execute-api:Invoke',
                    'Resource': [f'{resource_arn.rstrip("/")}'] # Use the API Gateway URL in the policy
                }
            ]
        }
    }

   
    print(policy)
    return policy
