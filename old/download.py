import os
import requests
import zipfile

# GitHub username
username = "kyegomez"

# API endpoint to fetch user's repositories
api_url = f"https://api.github.com/users/{username}/repos"

# Directory to store the downloaded repositories
download_dir = "lucidrains_repositories"

# Create the download directory if it doesn't exist
os.makedirs(download_dir, exist_ok=True)

# Make a GET request to fetch the user's repositories
response = requests.get(api_url)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    repositories = response.json()

    # Iterate over the repositories
    for repo in repositories:
        repo_name = repo["name"]
        repo_url = repo["html_url"]
        zip_url = f"{repo_url}/archive/refs/heads/master.zip"
        zip_file_path = os.path.join(download_dir, f"{repo_name}.zip")

        # Download the ZIP file
        zip_response = requests.get(zip_url)

        # Check if the ZIP file download was successful
        if zip_response.status_code == 200:
            with open(zip_file_path, "wb") as zip_file:
                zip_file.write(zip_response.content)
            
            # Unzip the repository
            with zipfile.ZipFile(zip_file_path, "r") as zip_ref:
                zip_ref.extractall(download_dir)

            print(f"Downloaded and unzipped {repo_name}")
        else:
            print(f"Failed to download {repo_name}")

else:
    print(f"Failed to fetch repositories for user {username}")

print("All repositories downloaded and unzipped.")

