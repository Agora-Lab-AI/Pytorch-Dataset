[![Multi-Modality](agorabanner.png)](https://discord.gg/qUtxnK2NMf)

# Pytorch-Dataset
A PyTorch Code Dataset for Cutting-Edge Fine-tuning



## Installation
You can install the package using pip

```bash
pip install pytorch-dataset
```

# Usage
```python

from pytorch import GitHubDatasetGenerator

generator = GitHubDatasetGenerator('username', 'token')
dataset = generator.generate_dataset()
generator.save_dataset(dataset, 'dataset.jsonl')
```

# License
MIT



