import os
from datasets import Dataset, load_from_disk

class CodeDatasetBuilder:
    """
    A utility class to build and manage code datasets.

    Args:
        root_dir (str): The root directory to search for code files.

    Attributes:
        root_dir (str): The root directory to search for code files.

    Example:
        code_builder = CodeDatasetBuilder("lucidrains_repositories")
        code_builder.save_dataset("lucidrains_python_code_dataset", exclude_files=["setup.py"], exclude_dirs=["tests"])
        code_builder.push_to_hub("lucidrains_python_code_dataset", organization="kye")
    """

    def __init__(self, root_dir):
        self.root_dir = root_dir

    def collect_code_files(self, file_extension=".py", exclude_files=None, exclude_dirs=None):
        """
        Collects code snippets from files in the specified directory and its subdirectories.

        Args:
            file_extension (str, optional): The file extension of code files to include (default is ".py").
            exclude_files (list of str, optional): List of file names to exclude from collection (default is None).
            exclude_dirs (list of str, optional): List of directory names to exclude from collection (default is None).

        Returns:
            list of str: List of code snippets.
        """
        code_snippets = []
        exclude_files = set(exclude_files) if exclude_files else set()
        exclude_dirs = set(exclude_dirs) if exclude_dirs else set()

        try:
            for root, dirs, files in os.walk(self.root_dir):
                # Exclude specified directories
                dirs[:] = [d for d in dirs if d not in exclude_dirs]

                for file in files:
                    if file.endswith(file_extension) and file not in exclude_files:
                        with open(os.path.join(root, file), "r", encoding="utf-8") as f:
                            code = f.read()
                        code_snippets.append(code)
        except Exception as e:
            raise RuntimeError(f"Error while collecting code files: {e}")

        return code_snippets

    def create_dataset(self, file_extension=".py", exclude_files=None, exclude_dirs=None):
        """
        Creates a dataset from collected code snippets.

        Args:
            file_extension (str, optional): The file extension of code files to include (default is ".py").
            exclude_files (list of str, optional): List of file names to exclude from collection (default is None).
            exclude_dirs (list of str, optional): List of directory names to exclude from collection (default is None).

        Returns:
            datasets.Dataset: The code dataset.
        """
        code_snippets = self.collect_code_files(file_extension, exclude_files, exclude_dirs)
        dataset = Dataset.from_dict({"code": code_snippets})
        return dataset

    def save_dataset(self, dataset_name, file_extension=".py", exclude_files=None, exclude_dirs=None):
        """
        Saves the code dataset to disk.

        Args:
            dataset_name (str): The name for the saved dataset.
            file_extension (str, optional): The file extension of code files to include (default is ".py").
            exclude_files (list of str, optional): List of file names to exclude from collection (default is None).
            exclude_dirs (list of str, optional): List of directory names to exclude from collection (default is None).

        Raises:
            RuntimeError: If there is an error while saving the dataset.
        """
        dataset = self.create_dataset(file_extension, exclude_files, exclude_dirs)
        try:
            dataset.save_to_disk(dataset_name)
        except Exception as e:
            raise RuntimeError(f"Error while saving the dataset: {e}")

    def load_dataset(self, dataset_name):
        """
        Loads a code dataset from disk.

        Args:
            dataset_name (str): The name of the saved dataset.

        Returns:
            datasets.Dataset: The loaded code dataset.
        """
        try:
            loaded_dataset = load_from_disk(dataset_name)
            return loaded_dataset
        except Exception as e:
            raise RuntimeError(f"Error while loading the dataset: {e}")

    def push_to_hub(self, dataset_name):
        """
        Pushes the code dataset to the Hugging Face Model Hub.

        Args:
            dataset_name (str): The name of the saved dataset.
            organization (str, optional): The organization on the Model Hub to push to (default is "username").
        """
        try:
            self.load_dataset.push_to_hub(f"{dataset_name}")
        except Exception as e:
            raise RuntimeError(f"Error while pushing the dataset to the Hugging Face Model Hub: {e}")

# Example usage:
code_builder = CodeDatasetBuilder("huggingface")

code_builder.save_dataset(
    "huggingface", 
    exclude_files=["setup.py"], 
    exclude_dirs=["tests"]
)



code_builder.push_to_hub("all-hf-python-2")
