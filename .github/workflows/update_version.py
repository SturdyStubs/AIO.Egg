import json
import sys

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

def main():
    branch = sys.argv[1]
    with open('egg-rust--all-carbon-builds.json', 'r') as file:
        data = json.load(file)
    
    current_version = data['name'].split('v')[-1]
    new_version = increment_version(current_version, branch)
    data['name'] = f"Rust - All Carbon Builds v{new_version}"

    with open('egg-rust--all-carbon-builds.json', 'w') as file:
        json.dump(data, file, indent=2)

    print(f"{new_version}")

if __name__ == "__main__":
    main()
