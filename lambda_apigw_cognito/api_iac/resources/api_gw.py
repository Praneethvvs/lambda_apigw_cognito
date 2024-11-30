from aws_cdk import (
    aws_apigateway as apigateway,
    aws_lambda as _lambda,
    aws_iam as iam,
    Stack,
    CfnOutput
)
from constructs import Construct
from validators.env_config_validator import EnvConfig




def create_apigw(
     stack: Stack, lambda_function_api: _lambda.IFunction, env_config: EnvConfig, lambda_authorizer: _lambda.IFunction, **kwargs
):

    # Define the API Gateway REST API
    api_gw = apigateway.LambdaRestApi(
        stack,
        f"{env_config.PROJECT_NAME}-{env_config.ENV}-api_gateway",
        handler=lambda_function_api,
        proxy=False
    )

    authorizer = apigateway.TokenAuthorizer(
        stack, f"{env_config.PROJECT_NAME}-{env_config.ENV}-apigw_authorizer",
        handler=lambda_authorizer,
    )

    api_gw.root.add_method( "ANY",
            apigateway.LambdaIntegration(lambda_function_api), # method to apply to all HTTP methods (GET, POST, PUT, DELETE, etc.)
            authorizer=authorizer,  # Attach the Lambda Authorizer here
        )
    # Optional: Add additional permissions or policies if needed

    api_gw_url = api_gw.url

        # Return the API Gateway instance for potential further use
    return api_gw, api_gw_url
