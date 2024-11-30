from aws_cdk import Stack
from aws_cdk import aws_ec2 as ec2

from validators.api_config_validator import VpcConfig
from validators.env_config_validator import EnvConfig


def create_vpc(stack: Stack, env_config: EnvConfig, resource_config: VpcConfig):
    vpc = ec2.Vpc.from_lookup(
        stack,
        f"{env_config.PROJECT_NAME}-{env_config.ENV}-Vpc",
        # This can be the VPC ID, or name, or tags
        vpc_id=resource_config.lookup_id,
    )

    return vpc
