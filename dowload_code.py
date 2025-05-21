import requests
import base64
import os
github_token = os.getenv("GITHUB_TOKEN")


headers = {
    "Authorization": f"token {github_token}",
    "Accept": "application/vnd.github.v3+json"
}

def get_file_content(owner, repo, path, branch="master"):
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}?ref={branch}"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        content = response.json()
        if content.get("type") == "file":
            return base64.b64decode(content["content"]).decode("utf-8")
    return None

def get_python_files(owner, repo, path="", branch="master"):
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}?ref={branch}"
    response = requests.get(url, headers=headers)
    files = []
    if response.status_code == 200:
        contents = response.json()
        for item in contents:
            if item["type"] == "file" and item["name"].endswith(".py"):
                files.append(item["path"])
            elif item["type"] == "dir":
                files.extend(get_python_files(owner, repo, item["path"], branch))
    return files

owner = "NhutHao5504"
repo = "deepse-project"
branch = "master"

python_files = get_python_files(owner, repo, path="", branch=branch)
print(f"Tim thay {len(python_files)} file Python trong repo.")

os.makedirs("data/raw", exist_ok=True)

for i, file_path in enumerate(python_files):
    content = get_file_content(owner, repo, file_path, branch=branch)
    if content:
        local_path = f"data/raw/file_{i}.py"
        with open(local_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Da luu file: {local_path}")
