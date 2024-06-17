import os
import requests
import ast
import re

# GitHub API endpoint for repository contents
github_api_url = "https://api.github.com/repos/{owner}/{repo}/contents/{path}"

def extract_github_details(repo_url):
    parts = repo_url.rstrip('/').split('/')
    owner = parts[3]
    repo = parts[4]
    path = '/'.join(parts[6:]) if len(parts) > 6 else ''
    return owner, repo, path

def fetch_directory_structure_from_github(owner, repo, path='', access_token=None):
    headers = {}
    if access_token:
        headers['Authorization'] = f"token {access_token}"

    url = github_api_url.format(owner=owner, repo=repo, path=path)
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        contents = response.json()
        structure = []
        contents.sort(key=lambda x: (x['type'], x['name']))
        for item in contents:
            if item['type'] == 'dir':
                structure.append(f"├── {item['name']}/")
                structure.extend(fetch_directory_structure_from_github(owner, repo, item['path'], access_token))
            elif item['type'] == 'file':
                structure.append(f"├── {item['name']}")
        return structure
    else:
        raise ValueError(f"Failed to fetch directory structure: {response.status_code} - {response.json()['message']}")

def write_directory_structure_to_file(structure, output_file):
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write("\n".join(structure))

def fetch_file_content_from_github(owner, repo, path, access_token=None):
    headers = {}
    if access_token:
        headers['Authorization'] = f"token {access_token}"

    url = github_api_url.format(owner=owner, repo=repo, path=path)
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        file_content = response.json()
        if file_content['type'] == 'file':
            return requests.get(file_content['download_url']).text
    else:
        raise ValueError(f"Failed to fetch file content: {response.status_code} - {response.json()['message']}")

def extract_details_from_python_file(content):
    tree = ast.parse(content)
    classes = [node.name for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]
    functions = [node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
    return classes, functions

def extract_endpoints_from_urls_file(content):
    endpoints = re.findall(r'path\([\'"](.+?)[\'"]', content)
    return endpoints

def generate_detailed_report(owner, repo, important_files, access_token):
    details = []
    for file in important_files:
        try:
            content = fetch_file_content_from_github(owner, repo, file, access_token)
            if file.endswith('.py'):
                classes, functions = extract_details_from_python_file(content)
                details.append(f"\nDetails from {file}:\nClasses: {classes}\nFunctions: {functions}\n")
                if file.endswith('urls.py'):
                    endpoints = extract_endpoints_from_urls_file(content)
                    details.append(f"\nEndpoints from {file}:\n{endpoints}\n")
            elif file.endswith('README.md'):
                details.append(f"\nREADME Content:\n{content}\n")
        except ValueError as ve:
            details.append(f"\nFailed to fetch details from {file}: {ve}\n")
    return details

def append_details_to_output_file(details, output_file):
    with open(output_file, 'a', encoding='utf-8') as file:
        file.write("\n".join(details))

def identify_important_files(structure):
    important_files = []
    for line in structure:
        if line.strip().endswith('.py') or line.strip().endswith('README.md'):
            important_files.append(line.strip().lstrip('├── '))
    return important_files

# Example usage
if __name__ == "__main__":
    repo_url = input("Enter GitHub repository URL: ").strip()
    try:
        github_owner, github_repo, github_path = extract_github_details(repo_url)
        access_token = input("Enter GitHub access token (optional, press Enter to skip): ").strip()
        output_file = f"{github_repo}_directory_structure.txt"
        
        structure = fetch_directory_structure_from_github(github_owner, github_repo, github_path, access_token)
        write_directory_structure_to_file(structure, output_file)
        
        important_files = identify_important_files(structure)
        important_files = [f"{github_path}/{file}" if github_path else file for file in important_files]  # Add path prefix if needed

        details = generate_detailed_report(github_owner, github_repo, important_files, access_token)
        append_details_to_output_file(details, output_file)

        print(f"Directory structure and details written to {output_file}")
    
    except requests.exceptions.RequestException as e:
        print(f"Error: Failed to connect to GitHub API - {e}")
    except ValueError as ve:
        print(f"Error: {ve}")
    except Exception as ex:
        print(f"Error: An unexpected error occurred - {ex}")
