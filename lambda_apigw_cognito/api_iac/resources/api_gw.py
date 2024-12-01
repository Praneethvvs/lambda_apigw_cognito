from aws_cdk import (
    aws_apigateway as apigateway,
    aws_lambda as _lambda,
    aws_iam as iam,
    aws_ssm as ssm,
    Stack,
    CfnOutput
)
from constructs import Construct
from validators.env_config_validator import EnvConfig



def create_apigw(
     stack: Stack, lambda_function_api: _lambda.IFunction, env_config: EnvConfig, lambda_authorizer: _lambda.IFunction, **kwargs
):

    apigw_authorizer = apigateway.TokenAuthorizer(
        stack, f"{env_config.PROJECT_NAME}-{env_config.ENV}-apigw_authorizer",
        handler=lambda_authorizer #Default identity source - "Authorization"
    )

    # Define the API Gateway REST API
    api_gw = apigateway.LambdaRestApi(
        stack,
        f"{env_config.PROJECT_NAME}-{env_config.ENV}-api_gateway",
        handler=lambda_function_api,
        proxy=True,
        default_method_options=apigateway.MethodOptions(
            authorizer=apigw_authorizer

        )
    )

    api_gw_url = api_gw.url
    apig_gw_arn = api_gw.arn_for_execute_api("*", "/", "*")

    parameter = ssm.StringParameter(stack, 
            f"{env_config.PROJECT_NAME}-{env_config.ENV}-apigw_resource_arn",
            parameter_name=f"/{env_config.PROJECT_NAME}/apigw_resource_arn",
            string_value=f"{apig_gw_arn}",
            tier=ssm.ParameterTier.STANDARD,  # Use STANDARD or ADVANCED
            description="api gateway url to use inside lambda authorizer code"
        )

    # parameter.grant_read(lambda_authorizer)

    CfnOutput(
            stack, "ApiGatewayUrl",
            value=api_gw_url,  # URL of the API Gateway
            description="The URL of the API Gateway",
            export_name="ApiGatewayEndpoint"
        )



        # Return the API Gateway instance for potential further use
    return api_gw, api_gw_url
