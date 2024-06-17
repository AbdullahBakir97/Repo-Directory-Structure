import os
import ast
import subprocess
import tempfile
import requests

def clone_repo(repo_url, access_token=None):
    temp_dir = tempfile.mkdtemp()
    clone_url = repo_url
    if access_token:
        clone_url = repo_url.replace("https://", f"https://{access_token}@")
    subprocess.run(["git", "clone", clone_url, temp_dir], check=True)
    return temp_dir

def parse_python_file(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        node = ast.parse(file.read(), filename=file_path)
    
    classes = [n.name for n in node.body if isinstance(n, ast.ClassDef)]
    functions = [n.name for n in node.body if isinstance(n, ast.FunctionDef)]
    
    return classes, functions

def extract_endpoints(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        node = ast.parse(file.read(), filename=file_path)
    
    endpoints = []
    for n in node.body:
        if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == 'urlpatterns' for t in n.targets):
            for element in n.value.elts:
                if isinstance(element, ast.Call):
                    for arg in element.args:
                        if isinstance(arg, ast.Constant):
                            endpoints.append(arg.value)
    return endpoints

def categorize_items(base_path):
    categorized_items = {
        "Admin": [],
        "API Views": [],
        "Views": [],
        "Models": [],
        "Serializers": [],
        "Tests": [],
        "Signals": [],
        "Services": [],
        "Consumers": [],
        "Endpoints": [],
        "Queries": [],
        "Querysets": [],
        "Others": []
    }

    for root, _, files in os.walk(base_path):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                classes, functions = parse_python_file(file_path)
                relative_path = os.path.relpath(file_path, base_path)

                if "admin.py" in file:
                    categorized_items["Admin"].extend(classes + functions)
                elif "views.py" in file:
                    categorized_items["Views"].extend(classes + functions)
                elif "api" in file:
                    categorized_items["API Views"].extend(classes + functions)
                elif "models.py" in file:
                    categorized_items["Models"].extend(classes + functions)
                elif "serializers.py" in file or "serializer" in file:
                    categorized_items["Serializers"].extend(classes + functions)
                elif "tests.py" in file or "test" in file:
                    categorized_items["Tests"].extend(classes + functions)
                elif "signals.py" in file or "signal" in file:
                    categorized_items["Signals"].extend(classes + functions)
                elif "services.py" in file or "service" in file:
                    categorized_items["Services"].extend(classes + functions)
                elif "consumers.py" in file or "consumer" in file:
                    categorized_items["Consumers"].extend(classes + functions)
                elif "queries.py" in file or "query" in file:
                    categorized_items["Queries"].extend(classes + functions)
                elif "querysets.py" in file or "queryset" in file:
                    categorized_items["Querysets"].extend(classes + functions)
                elif "urls.py" in file:
                    endpoints = extract_endpoints(file_path)
                    categorized_items["Endpoints"].extend(endpoints)
                else:
                    categorized_items["Others"].extend(classes + functions)

    return categorized_items

def print_section(header, items, file=None):
    output = [f"{header}:"]
    if not items:
        output.append("No items found.")
    else:
        for item in items:
            output.append(f"- {item}")
    output.append("")

    if file:
        file.write("\n".join(output) + "\n")
    else:
        print("\n".join(output))

def analyze_github_repository(repo_url, access_token=None, output_file=None):
    try:
        repo_path = clone_repo(repo_url, access_token)
        categorized_items = categorize_items(repo_path)
        
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as file:
                for header, items in categorized_items.items():
                    print_section(header, items, file)
            print(f"Results have been written to {output_file}")
        else:
            for header, items in categorized_items.items():
                print_section(header, items)
    except subprocess.CalledProcessError as e:
        print(f"Failed to clone the repository - {e}")
    except Exception as ex:
        print(f"An unexpected error occurred - {ex}")

if __name__ == "__main__":
    repo_url = input("Enter GitHub repository URL (e.g., https://github.com/owner/repo): ").strip()
    access_token = input("Enter GitHub access token (press Enter if none): ").strip()
    output_file = input("Enter output file name (e.g., output.txt): ").strip()
    analyze_github_repository(repo_url, access_token, output_file)
