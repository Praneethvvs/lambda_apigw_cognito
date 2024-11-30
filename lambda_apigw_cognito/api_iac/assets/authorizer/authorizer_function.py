import json
import os

def handler(event, context):
    # Extract the token (usually from Authorization header)
    token = event['authorizationToken']
    
    # Get the API Gateway URL from environment variable
    api_gateway_url = os.getenv('API_GATEWAY_URL')


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
                    'Resource': f'{api_gateway_url}/*'  # Use the API Gateway URL in the policy
                }
            ]
        }
    }

   

    return policy
