import json
import sys
import requests
import re
import os
import zipfile
import hashlib

def get_commit_messages_since_last_release(repo, last_release_tag, token):
    release_url = f"https://api.github.com/repos/{repo}/releases/tags/{last_release_tag}"
    headers = {'Authorization': f'token {token}'}
    response = requests.get(release_url, headers=headers)

    if response.status_code != 200:
        print(f"Failed to fetch release date: {response.status_code}")
        return []

    last_release_date = response.json()['published_at']
    url = f"https://api.github.com/repos/{repo}/commits"
    params = {'sha': 'main', 'since': last_release_date}
    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        commits = response.json()
        return [commit['commit']['message'] for commit in commits]
    else:
        print(f"Failed to fetch commits: {response.status_code}")
        return []

def calculate_md5(file_path):
    with open(file_path, 'rb') as file:
        return hashlib.md5(file.read()).hexdigest()

def calculate_sha1(file_path):
    with open(file_path, 'rb') as file:
        return hashlib.sha1(file.read()).hexdigest()

def calculate_sha256(file_path):
    with open(file_path, 'rb') as file:
        return hashlib.sha256(file.read()).hexdigest()

def get_latest_release(repo):
    url = f"https://api.github.com/repos/{repo}/releases/latest"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()['tag_name']
    return None

def bundle_files(files):
    with zipfile.ZipFile('Carbon-Official-Egg.zip', 'w') as zipf:
        for file in files:
            zipf.write(file)

def upload_release_asset(upload_url, file_path, token):
    headers = {'Authorization': f'token {token}', 'Content-Type': 'application/octet-stream'}
    params = {'name': os.path.basename(file_path)}
    with open(file_path, 'rb') as file:
        response = requests.post(upload_url, headers=headers, params=params, data=file)
        return response.status_code == 201

def create_release(repo, version, token, md5_checksum, sha1_checksum, sha256_checksum, commit_messages):
    commit_messages_str = '\n'.join(f"- {msg}" for msg in commit_messages)
    url = f"https://api.github.com/repos/{repo}/releases"
    headers = {'Authorization': f'token {token}'}
    body = (f'Release of version {version}\n\n'
            f'Commits since last release:\n{commit_messages_str}\n\n'
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

def update_version_in_egg(branch):
    with open('egg-rust--all-carbon-builds.json', 'r') as file:
        data = json.load(file)
    
    current_version = data['name'].split('v')[-1]
    new_version = increment_version(current_version, branch)
    data['name'] = f"Rust - All Carbon Builds v{new_version}"

    with open('egg-rust--all-carbon-builds.json', 'w') as file:
        json.dump(data, file, indent=2)

    print(new_version)
    return new_version

def main():
    repo = 'SturdyStubs/AIO.Egg'
    token = os.environ['PERSONAL_ACCESS_TOKEN']
    branch = sys.argv[1]
    
    latest_release = get_latest_release(repo)
    commit_messages = get_commit_messages_since_last_release(repo, latest_release, token)

    new_version = update_version_in_egg(branch)

    files_to_bundle = ['egg-rust--all-carbon-builds.json', 'README.md']
    bundle_files(files_to_bundle)
    
    md5_checksum = calculate_md5('egg-rust--all-carbon-builds.json')
    sha1_checksum = calculate_sha1('egg-rust--all-carbon-builds.json')
    sha256_checksum = calculate_sha256('egg-rust--all-carbon-builds.json')
    
    success, upload_url = create_release(repo, new_version, token, md5_checksum, sha1_checksum, sha256_checksum, commit_messages)
    if success:
        upload_url = upload_url.split('{')[0]
        if upload_release_asset(upload_url, 'Carbon-Official-Egg.zip', token):
            print("Release and assets uploaded successfully")
        else:
            print("Failed to upload assets")
            exit(1)
    else:
        print("Failed to create release")

if __name__ == "__main__":
    main()
