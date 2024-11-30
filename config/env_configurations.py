from .config_base import ConfigBase


class ConfigDev(ConfigBase):
    """Development environment specific configuration."""

    ENV = "dev"
    DEBUG = False
    ACCOUNT = "664418975681"
    REGION = "us-east-1"


class ConfigStaging(ConfigBase):
    """Staging environment specific configuration."""

    ENV = "staging"
    DEBUG = False
    ACCOUNT = ""
    REGION = ""


class ConfigProd(ConfigBase):
    """Production environment specific configuration."""

    ENV = "prod"
    DEBUG = False
    ACCOUNT = ""
    REGION = ""
