#!/usr/bin/env python3

import os
from dataclasses import is_dataclass
from typing import Any, Dict, Optional, Type, TypeVar

import dotenv
import yaml

T = TypeVar('T')


class Project:
    """Project configuration manager that loads settings from YAML files."""

    def __init__(self, project_file: Optional[str] = None):
        """Initialize the project with a specific YAML file
        or use DEFAULT_PROJECT from env."""
        dotenv.load_dotenv()

        if project_file is None:
            project_file = os.environ.get("DEFAULT_PROJECT")
            if project_file is None:
                raise ValueError(
                    "No project file specified"
                    "and DEFAULT_PROJECT not found in environment"
                )

        if not os.path.exists(project_file):
            raise FileNotFoundError(f"Project file not found: {project_file}")

        self.project_file = project_file

        # Load and parse YAML
        with open(project_file, "r", encoding="utf-8") as f:
            self.config_data = yaml.safe_load(f) or {}

    def Settings(self, settings_class: Type[T]) -> T:
        """
        Create an instance of the given dataclass type populated with
        values from the YAML config using dataclasses-json.

        Args:
            settings_class: The dataclass type to instantiate and populate

        Returns:
            An instance of settings_class populated with YAML values

        Example:
            @dataclass_json
            @dataclass
            class MySettings:
                base_dim: int = 500
                languages: List[LanguageSettings] = field(default_factory=list)

            settings = project.Settings(MySettings)
        """
        if not is_dataclass(settings_class):
            raise TypeError(f"Settings class {settings_class}"
                            " must be a dataclass")

        # Use dataclasses-json to create instance from dict
        return settings_class.from_dict(self.config_data)  # type: ignore

    def get_raw_config(self) -> Dict[str, Any]:
        """Get the raw YAML configuration data."""
        return self.config_data.copy()
