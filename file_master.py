#!/usr/bin/env python3
import os, json, base64, requests

OWNER = "WhompINC"
REPO = "Files"
BRANCH = "main"
FILE_TREE = "file_tree.json"
DOC_ROOT = "d"
GITHUB_TOKEN = "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"

def build_tree(path):
    tree = {}
    for name in sorted(os.listdir(path)):
        full = os.path.join(path, name)
        if os.path.isdir(full):
            tree[name] = build_tree(full)
        else:
            tree[name] = "file"
    return tree

data = {}
for branch in sorted(os.listdir(DOC_ROOT)):
    p = os.path.join(DOC_ROOT, branch)
    if os.path.isdir(p):
        data[branch] = build_tree(p)

content_str = json.dumps(data, indent=2)
with open(FILE_TREE, "w") as f:
    f.write(content_str)

api_url = f"https://api.github.com/repos/{OWNER}/{REPO}/contents/{FILE_TREE}"
hdrs = {"Authorization": f"Bearer {GITHUB_TOKEN}", "Accept": "application/vnd.github+json"}
resp = requests.get(api_url, headers=hdrs)
if resp.status_code == 200:
    sha = resp.json()["sha"]
elif resp.status_code == 404:
    sha = None
else:
    raise SystemExit(f"Error fetching {FILE_TREE}: {resp.status_code}")

b64 = base64.b64encode(content_str.encode()).decode()
payload = {"message": f"ci: update {FILE_TREE}", "content": b64, "branch": BRANCH}
if sha: payload["sha"] = sha

resp2 = requests.put(api_url, headers=hdrs, json=payload)
if resp2.status_code in (200,201):
    print("✅ file_tree.json updated on GitHub")
else:
    print(f"❌ Failed: {resp2.status_code} {resp2.text}")