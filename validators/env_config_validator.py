from pydantic import BaseModel


class EnvConfig(BaseModel):
    PROJECT_NAME: str
    ENV: str
    DEBUG: str
    ACCOUNT: str
    REGION: str
