import os
import requests
import zipfile
import time
from zipfile import BadZipFile

class GitHubRepoDownloader:
    """
    A utility class to download and unzip GitHub repositories.
    """
    def __init__(self, username, download_dir, api_token=None, specific_repos=None):
        self.username = username
        self.api_url = f"https://api.github.com/users/{username}/repos"
        self.download_dir = download_dir
        self.api_token = api_token
        self.specific_repos = specific_repos if specific_repos else []
        os.makedirs(self.download_dir, exist_ok=True)

    def _get_repositories(self):
        headers = {}
        if self.api_token:
            headers["Authorization"] = f"token {self.api_token}"

        all_repositories = []
        page = 1
        while True:
            response = requests.get(f"{self.api_url}?page={page}", headers=headers)
            if response.status_code != 200:
                response.raise_for_status()
            if not response.json():
                break
            all_repositories.extend(response.json())
            page += 1
            if "X-RateLimit-Remaining" in response.headers and int(response.headers["X-RateLimit-Remaining"]) == 0:
                time.sleep(60)
        return all_repositories

    def download_repositories(self):
        repositories = self._get_repositories()
        for repo in repositories:
            repo_name = repo["name"]
            if self.specific_repos and repo_name not in self.specific_repos:
                continue
            repo_url = repo["html_url"]
            zip_url = f"{repo_url}/archive/refs/heads/master.zip"
            zip_file_path = os.path.join(self.download_dir, f"{repo_name}.zip")
            zip_response = requests.get(zip_url)
            if zip_response.status_code == 200:
                with open(zip_file_path, "wb") as zip_file:
                    zip_file.write(zip_response.content)
                try:
                    self._unzip_repository(zip_file_path)
                    os.remove(zip_file_path)
                    print(f"Downloaded and unzipped {repo_name}")
                except BadZipFile:
                    print(f"Invalid ZIP file for {repo_name}")
            else:
                print(f"Failed to download {repo_name}")

    def _unzip_repository(self, zip_file_path):
        with zipfile.ZipFile(zip_file_path, "r") as zip_ref:
            zip_ref.extractall(self.download_dir)

# Example usage:
downloader = GitHubRepoDownloader(
    username="kyegomez", 
    download_dir="pytorch_repositories", 
    api_token=""
)
downloader.download_repositories()


