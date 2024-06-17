import os
import subprocess
import tempfile
import shutil
import glob
import re
from typing import List, Dict
from repository_db import store_analysis_result

# Regular expressions for extracting information from files
CLASS_REGEX = re.compile(r'class\s+([^\(:]+)')
FUNCTION_REGEX = re.compile(r'def\s+([^\(:]+)')
ENDPOINT_REGEX = re.compile(r'@app\.route\(\'([^\']+)')

def clone_repository(repo_url: str, temp_dir: str) -> None:
    """
    Clones the GitHub repository into a temporary directory.
    """
    try:
        subprocess.run(['git', 'clone', repo_url, temp_dir], check=True)
    except subprocess.CalledProcessError as e:
        raise ValueError(f"Failed to clone repository: {e}")

def detect_languages(temp_dir: str) -> List[str]:
    """
    Detects the programming language(s) used in the repository.
    """
    languages = []
    extensions = set()

    for root, _, files in os.walk(temp_dir):
        for file in files:
            extension = os.path.splitext(file)[1]
            extensions.add(extension)

    for ext in extensions:
        if ext in ['.py', '.pyw']:
            languages.append('Python')
        elif ext in ['.java']:
            languages.append('Java')
        # Add more languages as needed

    return languages

def parse_files(temp_dir: str) -> Dict[str, List[str]]:
    """
    Parses each file in the repository to extract classes, functions, and endpoints.
    """
    classes = []
    functions = []
    endpoints = []

    for root, _, files in os.walk(temp_dir):
        for file in files:
            file_path = os.path.join(root, file)

            if file_path.endswith('.py'):
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                    # Extract classes
                    class_matches = CLASS_REGEX.findall(content)
                    classes.extend(class_matches)

                    # Extract functions
                    function_matches = FUNCTION_REGEX.findall(content)
                    functions.extend(function_matches)

                    # Extract endpoints (assuming Flask-like decorators)
                    endpoint_matches = ENDPOINT_REGEX.findall(content)
                    endpoints.extend(endpoint_matches)

    return {
        'classes': classes,
        'functions': functions,
        'endpoints': endpoints
    }

def analyze_repository(repo_url: str) -> Dict[str, List[str]]:
    """
    Analyzes the GitHub repository by cloning it, detecting languages, and parsing files.
    """
    analysis_result = {
        'classes': [],
        'functions': [],
        'endpoints': []
    }

    temp_dir = tempfile.mkdtemp(prefix='repo_')

    try:
        # Clone repository
        clone_repository(repo_url, temp_dir)

        # Detect languages
        languages = detect_languages(temp_dir)
        if languages:
            print(f"Detected Languages: {', '.join(languages)}")

        # Parse files
        analysis_result = parse_files(temp_dir)
    except ValueError as e:
        print(f"Error: {e}")
    finally:
        # Clean up temporary directory
        shutil.rmtree(temp_dir, ignore_errors=True)

    return analysis_result

# Example usage
if __name__ == "__main__":
    # Example GitHub repository URL
    repo_url = "https://github.com/username/repository"

    try:
        # Analyze repository
        repo_analysis_result = analyze_repository(repo_url)
        print("Repository Analysis Result:")
        print(repo_analysis_result)

        # Store analysis result in the database
        store_analysis_result(repo_url, repo_analysis_result)
        print("Analysis result stored in the database.")
    
    except Exception as e:
        print(f"Error: An unexpected error occurred - {e}")
