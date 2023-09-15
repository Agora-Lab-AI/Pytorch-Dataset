import os
import requests
import zipfile

class GitHubRepoDownloader:
    """
    # Example usage:
    # downloader = GitHubRepoDownloader(username="lucidrains", download_dir="lucidrains_repositories")
    # downloader.download_repositories()
    
    """
    def __init__(self, username, download_dir):
        self.username = username
        self.api_url = f"https://api.github.com/users/{username}/repos"
        self.download_dir = download_dir
        os.makedirs(self.download_dir, exist_ok=True)

    def download_repositories(self):
        response = requests.get(self.api_url)
        if response.status_code == 200:
            repositories = response.json()
            for repo in repositories:
                repo_name = repo["name"]
                repo_url = repo["html_url"]
                zip_url = f"{repo_url}/archive/refs/heads/master.zip"
                zip_file_path = os.path.join(self.download_dir, f"{repo_name}.zip")
                zip_response = requests.get(zip_url)
                if zip_response.status_code == 200:
                    with open(zip_file_path, "wb") as zip_file:
                        zip_file.write(zip_response.content)
                    self._unzip_repository(zip_file_path)
                    print(f"Downloaded and unzipped {repo_name}")
                else:
                    print(f"Failed to download {repo_name}")
        else:
            print(f"Failed to fetch repositories for user {self.username}")
        print("All repositories downloaded and unzipped.")

    def _unzip_repository(self, zip_file_path):
        with zipfile.ZipFile(zip_file_path, "r") as zip_ref:
            zip_ref.extractall(self.download_dir)

