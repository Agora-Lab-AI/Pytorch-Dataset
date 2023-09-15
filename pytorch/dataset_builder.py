import os
import re
from datasets import Dataset, load_from_disk

class CodeDatasetBuilder:
    def __init__(self, root_dir):
        self.root_dir = root_dir

    def collect_code_files(self, file_extension=".py", exclude_files=None):
        code_snippets = []
        exclude_files = set(exclude_files) if exclude_files else set()
        
        for root, _, files in os.walk(self.root_dir):
            for file in files:
                if file.endswith(file_extension) and file not in exclude_files:
                    with open(os.path.join(root, file), "r", encoding="utf-8") as f:
                        code = f.read()
                        # Remove import statements to exclude dependencies
                        code = re.sub(r'^import .*\n', '', code, flags=re.MULTILINE)
                        code = re.sub(r'^from .*\n', '', code, flags=re.MULTILINE)
                    code_snippets.append(code)
        
        return code_snippets

    def create_dataset(self, file_extension=".py", exclude_files=None):
        code_snippets = self.collect_code_files(file_extension, exclude_files)
        dataset = Dataset.from_dict({"code": code_snippets})
        return dataset

    def save_dataset(self, dataset_name):
        dataset = self.create_dataset()
        dataset.save_to_disk(dataset_name)

    def load_dataset(self, dataset_name):
        loaded_dataset = load_from_disk(dataset_name)
        return loaded_dataset

    def push_to_hub(self, dataset_name, organization=None):
        dataset = self.load_dataset(dataset_name)
        organization = organization or "username"
        dataset.push_to_hub(f"{organization}/{dataset_name}")

# Example usage:
# code_builder = CodeDatasetBuilder("lucidrains_repositories")
# code_builder.save_dataset("lucidrains_python_code_dataset")
# code_builder.push_to_hub("lucidrains_python_code_dataset", organization="kye")
