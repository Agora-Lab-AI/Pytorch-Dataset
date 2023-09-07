import requests
import json
import base64

class GitHubDatasetGenerator:
    def __init__(self, username, token):
        self.username = username
        self.token = token
        self.base_url = "https://api.github.com"
        self.headers = {'Authorization': f'token {self.token}'}

    def get_repos(self):
        url = f"{self.base_url}/users/{self.username}/repos"
        response = requests.get(url, headers=self.headers)
        return json.loads(response.text)

    def get_files(self, repo_name):
        url = f"{self.base_url}/repos/{self.username}/{repo_name}/contents"
        response = requests.get(url, headers=self.headers)
        return json.loads(response.text)

    def get_file_content(self, download_url):
        response = requests.get(download_url)
        return response.text

    def generate_dataset(self):
        dataset = []
        repos = self.get_repos()
        for repo in repos:
            repo_name = repo['name']
            files = self.get_files(repo_name)
            for file in files:
                if file['name'].endswith('.py') or file['name'] == 'README.md':
                    file_content = self.get_file_content(file['download_url'])
                    dataset.append({
                        'repo': repo_name,
                        'file': file['name'],
                        'url': file['html_url'],
                        'content': file_content
                    })
        return dataset

    def save_dataset(self, dataset, filename):
        with open(filename, 'w') as f:
            for data in dataset:
                f.write(json.dumps(data))
                f.write('\n')


# generator = GitHubDatasetGenerator('username', 'token')
# dataset = generator.generate_dataset()
# generator.save_dataset(dataset, 'dataset.jsonl')