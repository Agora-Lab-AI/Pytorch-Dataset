from setuptools import setup, find_packages

setup(
  name = 'autoregressive-linear-attention-cuda',
  packages = find_packages(exclude=[]),
  version = '0.0.1',
  license='MIT',
  description = 'Autoregressive Linear Attention CUDA kernel',
  author = 'Phil Wang',
  author_email = 'lucidrains@gmail.com',
  long_description_content_type = 'text/markdown',
  url = 'https://github.com/lucidrains/autoregressive-linear-attention-cuda',
  keywords = [
    'artificial intelligence',
    'deep learning',
    'transformers',
    'attention mechanism',
    'linear attention',
    'cuda'
  ],
  install_requires=[
    'torch>=1.6'
  ],
  classifiers=[
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'Topic :: Scientific/Engineering :: Artificial Intelligence',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.6',
  ],
)
