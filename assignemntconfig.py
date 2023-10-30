import os

class AssignmentConfig:
    """
    This module provides utilities for configuring weekly assignments.
    It serves as a central config store to manage assignment-related naming conventions, file paths,
    and storing arbitrary information.

    Attributes:
        BASE_INPUT_FOLDER (str): The base input folder path.
        BASE_OUTPUT_FOLDER (str): The base output folder path.
    """
    BASE_INPUT_FOLDER = "input"
    BASE_OUTPUT_FOLDER = "output"

    def __init__(self, assignment_name: str):
        self.assignment_name = assignment_name
        self.data_store = {}

    @property
    def formatted_name(self) -> str:
        return self.assignment_name.replace(" ", "_")

    @property
    def input_folder_path(self) -> str:
        return os.path.join(self.BASE_INPUT_FOLDER, self.formatted_name)

    @property
    def output_folder_path(self) -> str:
        return os.path.join(self.BASE_OUTPUT_FOLDER, self.formatted_name)

    def get_input_filepath(self, filename: str) -> str:
        return os.path.join(self.input_folder_path, filename)

    def get_output_filepath(self, filename: str) -> str:
        return os.path.join(self.output_folder_path, filename)

    def store_data(self, key: str, value: any) -> None:
        """
        Store arbitrary data using a key-value pair.

        Args:
            key (str): The key to identify the data.
            value (any): The data to store.
        """
        self.data_store[key] = value

    def retrieve_data(self, key: str) -> any:
        """
        Retrieve stored data using a key.

        Args:
            key (str): The key to identify the data.

        Returns:
            any: The data associated with the key. Returns None if key is not found.
        """
        return self.data_store.get(key, None)


class AssignmentConfigManager:
    """
    Manages the singleton instance of AssignmentConfig.
    """
    _instance = None

    @staticmethod
    def get_instance(assignment_name: str = None) -> AssignmentConfig:
        """
        Get the current active instance of AssignmentConfig.
        """
        if AssignmentConfigManager._instance is None and assignment_name is not None:
            AssignmentConfigManager._instance = AssignmentConfig(assignment_name)
        return AssignmentConfigManager._instance
