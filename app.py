#!/usr/bin/env python3
import os

import aws_cdk as cdk

from init.init_settings import ConfigurationHandler
from lambda_apigw_cognito.api_iac.api_stack import ApiStack

ENV_NAME = os.getenv("CDK_ENV", "dev")
API_DOCKER_TAG = os.getenv("API_DOCKER_TAG", "latest")

if not ENV_NAME:
    raise ValueError(
        "Provide an environment for the cdk stack to deploy; Accepted values ['dev', staging', 'prod]"
    )

if not API_DOCKER_TAG:
    raise ValueError("Provide an API_DOCKER_TAG for the cdk stack to deploy")


env_config, api_config = ConfigurationHandler(
    ENV_NAME
).get_configurations()

app = cdk.App()

cdk_environment = cdk.Environment(account=env_config.ACCOUNT, region=env_config.REGION)

api_stack = ApiStack(
    app,
    f"{env_config.PROJECT_NAME}-{env_config.ENV}-WorkerStack",
    env_config=env_config,
    api_config=api_config,
    env=cdk_environment,
    docker_tag=API_DOCKER_TAG,
)


app.synth()
