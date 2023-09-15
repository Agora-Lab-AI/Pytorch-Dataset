import os
import requests
import zipfile
from zipfile import BadZipFile

class GitHubRepoDownloader:
    """
    A utility class to download and unzip GitHub repositories.

    Args:
        username (str): GitHub username.
        download_dir (str): Directory to store the downloaded repositories.

    Attributes:
        username (str): GitHub username.
        api_url (str): API endpoint to fetch user's repositories.
        download_dir (str): Directory to store the downloaded repositories.

    Example:
        downloader = GitHubRepoDownloader(username="lucidrains", download_dir="lucidrains_repositories")
        downloader.download_repositories()
    """

    def __init__(self, username, download_dir):
        self.username = username
        self.api_url = f"https://api.github.com/users/{username}/repos"
        self.download_dir = download_dir
        os.makedirs(self.download_dir, exist_ok=True)

    def download_repositories(self):
        """
        Downloads and unzips repositories from the user's GitHub account.

        Raises:
            RuntimeError: If there is an error during download or unzip.
        """
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
                    try:
                        self._unzip_repository(zip_file_path)
                        print(f"Downloaded and unzipped {repo_name}")
                    except BadZipFile:
                        print(f"Invalid ZIP file for {repo_name}")
                else:
                    print(f"Failed to download {repo_name}")
        else:
            raise RuntimeError(f"Failed to fetch repositories for user {self.username}")
        print("All repositories downloaded and unzipped.")

    def _unzip_repository(self, zip_file_path):
        """
        Unzips a repository ZIP file.

        Args:
            zip_file_path (str): Path to the ZIP file to unzip.

        Raises:
            BadZipFile: If the ZIP file is invalid.
        """
        with zipfile.ZipFile(zip_file_path, "r") as zip_ref:
            zip_ref.extractall(self.download_dir)

# Example usage:
downloader = GitHubRepoDownloader(username="lucidrains", download_dir="lucidrains_repositories")
try:
    downloader.download_repositories()
except RuntimeError as e:
    print(f"Error: {e}")

