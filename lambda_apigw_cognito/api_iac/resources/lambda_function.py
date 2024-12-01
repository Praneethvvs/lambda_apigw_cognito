from aws_cdk import Duration, Fn, Stack
from aws_cdk import aws_ec2 as ec2
from aws_cdk import aws_ecr as ecr
from aws_cdk import aws_iam as iam
from aws_cdk import aws_lambda as lambda_function
from aws_cdk import aws_lambda_event_sources as eventsources

from validators.env_config_validator import EnvConfig
from validators.api_config_validator import LambdaFunctionConfig


def create_function(
    stack: Stack,
    env_config: EnvConfig,
    resource_config: LambdaFunctionConfig,
    vpc,
    docker_tag,
):

    repo = ecr.Repository.from_repository_name(
        stack,
        f"{env_config.PROJECT_NAME}-{env_config.ENV}-LambdaFunctionEcr",
        repository_name=resource_config.ecr_repo_name,
    )

    lambda_function_api = lambda_function.DockerImageFunction(
        stack,
        f"{env_config.PROJECT_NAME}-{env_config.ENV}-lambda_function_api",
        code=lambda_function.DockerImageCode.from_ecr(repo, tag_or_digest=docker_tag),
        function_name=f"{env_config.PROJECT_NAME}-{env_config.ENV}-worker",
        timeout=Duration.minutes(resource_config.timeout),
        memory_size=resource_config.memory_size
    )

    lambda_function_api.add_permission(
        f"{env_config.PROJECT_NAME}-{env_config.ENV}-ApiGatewayInvoke",
        principal=iam.ServicePrincipal("apigateway.amazonaws.com"),
    )


    managed_policies = [
        "AmazonS3FullAccess",
        "CloudWatchFullAccess",
        "SecretsManagerReadWrite",
        "AmazonSSMFullAccess",
    ]

    for policy in managed_policies:
        lambda_function_api.role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name(policy)
        )

    return lambda_function_api


def create_authorizer(
    stack: Stack,
    env_config: EnvConfig,
):
    lambda_authorizer = lambda_function.Function(stack, f"{env_config.PROJECT_NAME}-{env_config.ENV}-LambdaAuthorizer",
        runtime=lambda_function.Runtime.PYTHON_3_10,
        handler='authorizer.handler',  # The Lambda function handler for the authorizer
        code=lambda_function.Code.from_asset('lambda_apigw_cognito/api_iac/assets/authorizer'),
        environment={
            'API_GATEWAY_URL': 'placeholder'  # Set initial value, will update later
        }
    )

    managed_policies = [
        "AmazonSSMFullAccess",
    ]

    for policy in managed_policies:
        lambda_authorizer.role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name(policy)
        )


    return lambda_authorizer
