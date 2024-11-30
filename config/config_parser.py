import yaml
from pydantic import BaseModel, ValidationError


def load_stack_config(file_path: str, model_class: BaseModel) -> BaseModel:
    with open(file_path, "r") as yaml_file:
        yaml_content = yaml.safe_load(yaml_file)
        try:
            return model_class(**yaml_content)
        except ValidationError as e:
            raise ValueError(f"Invalid configuration for {file_path, model_class}: {e}")
