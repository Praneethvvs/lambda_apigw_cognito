from pydantic import BaseModel




class VpcConfig(BaseModel):
    lookup_id: str


class LambdaFunctionConfig(BaseModel):
    ecr_repo_name: str
    memory_size: int
    timeout: int


class ApiStackConfig(BaseModel):
    vpc: VpcConfig
    lambda_function: LambdaFunctionConfig


