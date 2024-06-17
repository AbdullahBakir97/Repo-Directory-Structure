import os
import requests
from github import fetch_repository_contents, extract_github_details
from repo_analyzer import analyze_repository

def analyze_github_repository(repo_url, access_token=None):
    """
    Analyzes a GitHub repository comprehensively.
    """
    try:
        # Extract GitHub details from URL
        github_owner, github_repo, _ = extract_github_details(repo_url)

        # Fetch repository contents
        contents = fetch_repository_contents(github_owner, github_repo, access_token=access_token)

        # Analyze repository
        analysis_results = analyze_repository(repo_url)
        if isinstance(analysis_results, dict) and analysis_results.get("error"):
            print(f"Error in repository analysis: {analysis_results['error']}")
        else:
            print("Analysis results:")
            print(analysis_results)

    except requests.exceptions.RequestException as e:
        print(f"Failed to connect to GitHub API - {e}")
    except ValueError as ve:
        print(f"ValueError: {ve}")
    except Exception as ex:
        print(f"An unexpected error occurred - {ex}")


# Example usage
if __name__ == "__main__":
    # Example GitHub repository URL
    repo_url = input("Enter GitHub repository URL (e.g., https://github.com/owner/repo): ").strip()

    try:
        # Prompt user for GitHub access token
        access_token = input("Enter GitHub access token (press Enter if none): ").strip()

        # Analyze GitHub repository
        analyze_github_repository(repo_url, access_token)

    except Exception as ex:
        print(f"Error: An unexpected error occurred - {ex}")
