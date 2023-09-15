[![Multi-Modality](agorabanner.png)](https://discord.gg/qUtxnK2NMf)

# Pytorch-Dataset
A PyTorch Code Dataset for Cutting-Edge Fine-tuning



## Installation
You can install the package using pip

```bash
pip install pytorch-dataset
```

# Usage
Downloader that downloads and unzips each repository in an account
```python

from pytorch import GitHubRepoDownloader

downloader = GitHubRepoDownloader(username="lucidrains", download_dir="lucidrains_repositories")
downloader.download_repositories()
```

Processor that cleans, formats, and submits the cleaned dataset to huggingface
```python
from pytorch import CodeDatasetBuilder

code_builder = CodeDatasetBuilder("lucidrains_repositories")
code_builder.save_dataset("lucidrains_python_code_dataset")
code_builder.push_to_hub("lucidrains_python_code_dataset", organization="kye")

```
# License
MIT



