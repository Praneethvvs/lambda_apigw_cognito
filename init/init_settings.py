import os

from config import config_parser, env_configurations
from validators.api_config_validator import ApiStackConfig


class ConfigurationHandler:

    def __init__(self, env_name) -> None:
        self.env_name = env_name

    def get_configurations(self):
        # Dynamically select the configuration class based on the environment
        config_class_name = f"Config{self.env_name.capitalize()}"
        env_config = getattr(env_configurations, config_class_name)()
        api_config = config_parser.load_stack_config(
            file_path="config/resource_configurations/api_config.yml",
            model_class=ApiStackConfig,
        )
        return env_config, api_config
