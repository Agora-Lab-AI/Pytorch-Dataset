import os
from datasets import Dataset, load_from_disk
import re

class LucidrainsDataset:
    """    
    This class, LucidrainsDataset, has the following methods:

    __init__(self, repos_dir): Initializes the class with the path to the lucidrains directory.

    collect_python_files(self): Collects Python code snippets from all repositories in the lucidrains directory.

    _collect_python_files_in_repo(self, repo_dir): Collects Python files from a single repository directory.

    create_dataset(self): Creates a dataset from the collected Python code snippets.

    ```
    # Initialize the LucidrainsDataset with the path to the repositories directory
    repos_dir = "lucidrains_repositories"
    lucidrains_data = LucidrainsDataset(repos_dir)

    # Collect Python code snippets and create a dataset
    python_code_dataset = lucidrains_data.create_dataset()

    # Save the dataset
    python_code_dataset.save_to_disk("lucidrains_python_code_dataset")

    # Load the saved dataset for further use
    loaded_dataset = load_dataset("lucidrains_python_code_dataset")
    ```

    """
    def __init__(self, repos_dir):
        self.repos_dir = repos_dir

    def collect_python_files(self):
        python_code_snippets = []
        for repo_name in os.listdir(self.repos_dir):
            repo_dir = os.path.join(self.repos_dir, repo_name)
            if os.path.isdir(repo_dir):
                python_files = self._collect_python_files_in_repo(repo_dir)
                python_code_snippets.extend(python_files)
        return python_code_snippets

    def _collect_python_files_in_repo(self, repo_dir):
        python_files = []
        for root, _, files in os.walk(repo_dir):
            for file in files:
                if file.endswith(".py") and file != "setup.py":
                    with open(os.path.join(root, file), "r", encoding="utf-8") as f:
                        python_code = f.read()
                        # Remove import statements to exclude dependencies
                        python_code = re.sub(r'^import .*\n', '', python_code, flags=re.MULTILINE)
                        python_code = re.sub(r'^from .*\n', '', python_code, flags=re.MULTILINE)
                    python_files.append(python_code)
        return python_files

    def create_dataset(self):
        python_code_snippets = self.collect_python_files()
        dataset = Dataset.from_dict({"python_code": python_code_snippets})
        return dataset

# Initialize the LucidrainsDataset with the path to the repositories directory
repos_dir = "lucidrains_repositories"
lucidrains_data = LucidrainsDataset(repos_dir)

# Collect Python code snippets and create a dataset
python_code_dataset = lucidrains_data.create_dataset()

# Save the dataset
python_code_dataset.save_to_disk("lucidrains_python_code_dataset")

# Load the saved dataset for further use
loaded_dataset = load_from_disk("lucidrains_python_code_dataset")

# Push the dataset to the Hugging Face Datasets Hub
loaded_dataset.push_to_hub("kye/all-kye-code")