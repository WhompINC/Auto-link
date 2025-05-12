#!/usr/bin/env python3
import os, json, base64, requests

OWNER = "WhompINC"
REPO = "Files"
BRANCH = "main"
FILE_PATH = "file_tree.json"
DOC_ROOT = "d"
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

if not GITHUB_TOKEN:
    raise SystemExit("Set GITHUB_TOKEN environment variable.")

def build_tree(path):
    tree = {}
    for name in sorted(os.listdir(path)):
        full = os.path.join(path, name)
        tree[name] = build_tree(full) if os.path.isdir(full) else "file"
    return tree

data = {b: build_tree(os.path.join(DOC_ROOT,b))
        for b in sorted(os.listdir(DOC_ROOT))
        if os.path.isdir(os.path.join(DOC_ROOT,b))}

content_str = json.dumps(data, indent=2)
content_b64 = base64.b64encode(content_str.encode()).decode()

api_url = f"https://api.github.com/repos/{OWNER}/{REPO}/contents/{FILE_PATH}"
headers = {"Authorization": f"Bearer {GITHUB_TOKEN}",
           "Accept": "application/vnd.github+json"}

resp = requests.get(api_url, headers=headers)
if resp.status_code == 200:
    sha = resp.json()['sha']
elif resp.status_code == 404:
    sha = None
else:
    raise Exception(f"GET failed: {resp.status_code}")

payload = {"message": "ci: regen map via .map",
           "content": content_b64,
           "branch": BRANCH}
if sha: payload['sha'] = sha

resp2 = requests.put(api_url, headers=headers, json=payload)
if resp2.status_code in (200,201):
    print("✅ file_tree.json updated on GitHub")
else:
    raise Exception(f"PUT failed: {resp2.status_code}, {resp2.text}")