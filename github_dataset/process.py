import os
import concurrent.futures
from datasets import Dataset, load_from_disk


class LucidrainsDataset:
    def __init__(self, repos_dir, max_file_size=5 * 1024 * 1024):  # 5 MB default max
        self.repos_dir = repos_dir
        self.max_file_size = max_file_size

    def collect_python_files(self):
        all_snippets = []
        with concurrent.futures.ThreadPoolExecutor() as executor:
            for snippets in executor.map(
                self._collect_python_files_in_repo,
                [
                    os.path.join(self.repos_dir, repo_name)
                    for repo_name in os.listdir(self.repos_dir)
                ],
            ):
                all_snippets.extend(snippets)
        return all_snippets

    def _collect_python_files_in_repo(self, repo_dir):
        python_files = []
        for root, _, files in os.walk(repo_dir):
            for file in files:
                if file.endswith(".c"):
                    file_path = os.path.join(root, file)
                    if os.path.getsize(file_path) <= self.max_file_size:
                        try:
                            with open(file_path, "r", encoding="utf-8") as f:
                                python_code = f.read()
                            python_files.append(
                                {
                                    "python_code": python_code,
                                    "repo_name": os.path.basename(repo_dir),
                                    "file_path": os.path.relpath(file_path, repo_dir),
                                }
                            )
                        except UnicodeDecodeError:
                            print(f"Failed to decode {file_path}")
        return python_files

    def create_dataset(self):
        python_code_snippets = self.collect_python_files()
        dataset = Dataset.from_dict(
            {
                "python_code": [
                    snippet["python_code"] for snippet in python_code_snippets
                ],
                "repo_name": [snippet["repo_name"] for snippet in python_code_snippets],
                "file_path": [snippet["file_path"] for snippet in python_code_snippets],
            }
        )
        return dataset


# Usage remains similar
repos_dir = "torvalds"
lucidrains_data = LucidrainsDataset(repos_dir)

python_code_dataset = lucidrains_data.create_dataset()

python_code_dataset.save_to_disk("torvalds")

loaded_dataset = load_from_disk("torvalds")
loaded_dataset.push_to_hub("kye/all-torvalds-c-code-1")
