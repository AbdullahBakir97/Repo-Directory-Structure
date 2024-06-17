# GitHub Repository Analyzer

This project provides Python scripts to analyze the structure of a GitHub repository, categorizing items such as classes, functions, views, models, serializers, tests, signals, services, consumers, queries, querysets, and endpoints. The results can be printed to the console or written to a specified text file.

## Features
- Clone a GitHub repository.
- Parse and categorize Python files in the repository.
- Extract endpoints from URL configuration files.
- Output results to the console or a text file.
- Fetch directory structure directly from the GitHub API.

## Requirements
- Python 3.6+
- Git
- `requests` library

## Installation

### Clone the Repository:

```
git clone https://github.com/yourusername/github-repo-analyzer.git
cd github-repo-analyzer
```

### Set Up a Virtual Environment:

```
python -m venv venv
source venv/bin/activate  # On Windows use venv\Scripts\activate
```

### Install Dependencies:

```
pip install -r requirements.txt
```

## Usage
### Analyzing Repository Structure Locally

#### Run the Script:

```
python main.py
```

#### Provide Input:
Enter the GitHub repository URL (e.g., https://github.com/owner/repo).
Enter the GitHub access token if the repository is private (press Enter if none).
Enter the output file name where results should be written (e.g., output.txt).

```
python main.py
Enter GitHub repository URL (e.g., https://github.com/owner/repo): https://github.com/yourusername/sample-repo
Enter GitHub access token (press Enter if none):
Enter output file name (e.g., analysis_results.txt): analysis_results.txt
```

#### Output:

```
Results have been written to analysis_results.txt
```

### Fetching Directory Structure from GitHub API

#### Run the Script:

```
python fetch_structure.py
```

#### Provide Input:
Enter the GitHub repository URL (e.g., https://github.com/owner/repo).
Enter the GitHub access token if the repository is private (press Enter if none).

```
python fetch_structure.py
Enter GitHub repository URL (e.g., https://github.com/owner/repo): https://github.com/yourusername/sample-repo
Enter GitHub access token (press Enter if none):
```

#### Output:

```
Directory structure written to sample-repo_directory_structure.txt
```

## Script Breakdown

### `main.py`

This script performs the following tasks:

- **Clones the Repository:** Uses subprocess to run Git commands and clone the repository to a temporary directory.
- **Parses Python Files:** Uses the `ast` module to parse Python files and extract classes and functions.
- **Categorizes Items:** Walks through the cloned repository directory and categorizes items into specific types based on file names and content.
- **Extracts Endpoints:** Parses URL configuration files to extract endpoints.
- **Outputs Results:** Prints the categorized items to the console or writes them to a specified text file.

### `fetch_structure.py`

This script fetches the directory structure of a GitHub repository using the GitHub API.

- **Extracts GitHub Details:** Parses the repository URL to get the owner, repo name, and path.
- **Fetches Directory Structure:** Uses the GitHub API to fetch the directory structure recursively and sorts contents by type.
- **Writes Directory Structure to a File:** Outputs the fetched directory structure to a specified text file.

## Contributing

1. **Fork the Repository.**
2. **Create a new branch** for your feature or bugfix.
3. **Make your changes.**
4. **Submit a pull request.**

## License

This project is licensed under the MIT License. See the LICENSE file for details.
