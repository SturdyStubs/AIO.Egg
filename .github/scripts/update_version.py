import json
import sys
import requests
import re
import os
import zipfile
import hashlib

# Get commit messages since last release
def get_commit_messages_since_last_release(repo, last_release_tag, token):
    # First, get the date of the last release
    release_url = f"https://api.github.com/repos/{repo}/releases/tags/{last_release_tag}"
    headers = {'Authorization': f'token {token}'}
    response = requests.get(release_url, headers=headers)

    if response.status_code != 200:
        print(f"Failed to fetch release date: {response.status_code}")
        return []

    last_release_date = response.json()['published_at']

    # Now, fetch the commits since that date
    url = f"https://api.github.com/repos/{repo}/commits"
    params = {'sha': 'main', 'since': last_release_date}
    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        commits = response.json()
        return [commit['commit']['message'] for commit in commits]
    else:
        print(f"Failed to fetch commits: {response.status_code}")
        return []


# Get MD5 hash of file
def calculate_md5(file_path):
    with open(file_path, 'rb') as file:
        return hashlib.md5(file.read()).hexdigest()

# Get SHA-1 hash of file
def calculate_sha1(file_path):
    with open(file_path, 'rb') as file:
        return hashlib.sha1(file.read()).hexdigest()

# Get SHA-256 hash of file
def calculate_sha256(file_path):
    with open(file_path, 'rb') as file:
        return hashlib.sha256(file.read()).hexdigest()

# Function to get the latest release version from GitHub API
def get_latest_release(repo):
    url = f"https://api.github.com/repos/{repo}/releases/latest"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()['tag_name']
    return None

# Function to create a ZIP file with specific files
def bundle_files(files):
    with zipfile.ZipFile('Carbon-Official-Egg.zip', 'w') as zipf:
        for file in files:
            zipf.write(file)

# Function to upload a release asset
def upload_release_asset(upload_url, file_path, token):
    headers = {'Authorization': f'token {token}', 'Content-Type': 'application/octet-stream'}
    params = {'name': os.path.basename(file_path)}
    with open(file_path, 'rb') as file:
        response = requests.post(upload_url, headers=headers, params=params, data=file)
        return response.status_code == 201

# Function to create a new release
def create_release(repo, version, token, md5_checksum, sha1_checksum, sha256_checksum, commit_messages):
    commit_messages_str = '\n'.join(f"- {msg}" for msg in commit_messages)
    url = f"https://api.github.com/repos/{repo}/releases"
    headers = {'Authorization': f'token {token}'}
    body = (f'Release of version {version}\n\n'
            f'\n\n'
            f'Commits since last release:\n{commit_messages_str}'
            f'\n\n'
            f'Checksums of RustAnalytics.cs\n'
            f'MD5: {md5_checksum}\n'
            f'SHA-1: {sha1_checksum}\n'
            f'SHA-256: {sha256_checksum}')
    data = {
        'tag_name': version,
        'name': version,
        'body': body,
        'draft': False,
        'prerelease': False
    }
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 201:
        return True, response.json()['upload_url']
    else:
        print(f"Failed to create release: {response.status_code}")
        print(f"Response: {response.json()}")
        return False, None

def increment_version(version, part):
    major, minor, patch = map(int, version.split('.'))
    if part == 'beta':
        patch += 1
    elif part == 'staging':
        minor += 1
        patch = 0
    elif part == 'production':
        major += 1
        minor = 0
        patch = 0
    return f"{major}.{minor}.{patch}"

def update_version_in_egg():
    branch = sys.argv[1]
    with open('egg-rust--all-carbon-builds.json', 'r') as file:
        data = json.load(file)
    
    current_version = data['name'].split('v')[-1]
    new_version = increment_version(current_version, branch)
    data['name'] = f"Rust - All Carbon Builds v{new_version}"

    with open('egg-rust--all-carbon-builds.json', 'w') as file:
        json.dump(data, file, indent=2)

    print(f"{new_version}")

# Main execution
def main():

    repo = 'SturdyStubs/AIO.Egg'  # Replace with your repository
    token = os.environ['PERSONAL_ACTION_TOKEN']  # Ensure GITHUB_TOKEN is set in your secrets
    files_to_bundle = ['egg-rust--all-carbon-builds.json', 'README.md']
    md5_checksum = calculate_md5('egg-rust--all-carbon-builds.json')
    sha1_checksum = calculate_sha1('egg-rust--all-carbon-builds.json')
    sha256_checksum = calculate_sha256('egg-rust--all-carbon-builds.json')
    current_version = extract_version()
    latest_release = get_latest_release(repo)
    print(f"Current Version: {current_version}")
    print(f"Latest Release: {latest_release}")
    commit_messages = get_commit_messages_since_last_release(repo, latest_release, token)

    update_version_in_egg()

    bundle_files(files_to_bundle)
    success, upload_url = create_release(repo, current_version, token, md5_checksum, sha1_checksum, sha256_checksum, commit_messages)
    if success:
        upload_url = upload_url.split('{')[0]
        if upload_release_asset(upload_url, 'Carbon-Official-Egg.zip', token):
            print("Release and assets uploaded successfully")
        else:
            print("Failed to upload assets")
    else:
        print("Failed to create release")

if __name__ == "__main__":
    main()
