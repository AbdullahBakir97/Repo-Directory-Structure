import requests

github_api_url = "https://api.github.com/repos/{owner}/{repo}/contents/{path}"

def extract_github_details(repo_url):
    """
    Extracts GitHub owner, repository name, and path from the provided GitHub repository URL.
    """
    parts = repo_url.rstrip('/').split('/')
    owner = parts[3]
    repo = parts[4]
    path = '/'.join(parts[6:]) if len(parts) > 6 else ''
    return owner, repo, path

def fetch_repository_contents(owner, repo, path='', access_token=None):
    """
    Fetches contents (files and directories) of a GitHub repository using the GitHub API.
    """
    headers = {}
    if access_token:
        headers['Authorization'] = f"token {access_token}"

    url = github_api_url.format(owner=owner, repo=repo, path=path)
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        contents = response.json()
        return contents
    else:
        raise ValueError(f"Failed to fetch repository contents: {response.status_code} - {response.json().get('message', 'Unknown error')}")
