from aws_cdk import Stack,  CfnOutput
from constructs import Construct

from validators.api_config_validator import ApiStackConfig

from .resources import  networking, lambda_function, api_gw


class ApiStack(Stack):

    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        env_config,
        api_config: ApiStackConfig,
        docker_tag: str,
        **kwargs
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.env_config = env_config
        self.api_config = api_config
        self.docker_tag = docker_tag
        self.init_resources()

    def init_resources(self):

        self.vpc = networking.create_or_lookup_vpc(
            self, env_config=self.env_config, resource_config=self.api_config.vpc
        )


        self.lambda_function_api = lambda_function.create_function(self, 
            env_config=self.env_config,
            resource_config=self.api_config.lambda_function,
            docker_tag=self.docker_tag,
            vpc=self.vpc
        )

          # Create the Lambda function for the authorizer
        
        self.lambda_authorizer = lambda_function.create_authorizer(self, 
            env_config=self.env_config,
        )
     
        

        self.api_gw, self.api_gw_url = api_gw.create_apigw(self, 
                                          lambda_function_api=self.lambda_function_api, 
                                          env_config=self.env_config,
                                          lambda_authorizer=self.lambda_authorizer)        



