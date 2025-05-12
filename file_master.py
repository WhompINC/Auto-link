#!/usr/bin/env python3
import os, json, base64, requests

OWNER = "WhompINC"
REPO = "Files"
BRANCH = "main"
FILES = ["file_tree.json", "index.html", "editor.html"]
DOC_ROOT = "d"
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

def build_tree(path):
    tree = {}
    for name in sorted(os.listdir(path)):
        full = os.path.join(path, name)
        if os.path.isdir(full):
            tree[name] = build_tree(full)
        else:
            tree[name] = "file"
    return tree

# regenerate map
data = {b: build_tree(os.path.join(DOC_ROOT,b)) for b in sorted(os.listdir(DOC_ROOT)) if os.path.isdir(os.path.join(DOC_ROOT,b))}
with open("file_tree.json","w") as f:
    json.dump(data, f, indent=2)

# commit via API
api_url = f"https://api.github.com/repos/{OWNER}/{REPO}/contents/"
headers = {"Authorization":f"Bearer {GITHUB_TOKEN}", "Accept":"application/vnd.github+json"}

for fname in FILES:
    # read content
    with open(fname,"rb") as f: raw = f.read()
    b64 = base64.b64encode(raw).decode()
    url = api_url + fname
    # get sha
    resp = requests.get(url, headers=headers)
    if resp.status_code == 200: sha = resp.json()['sha']
    else: sha = None
    payload = {"message":f"ci: update {fname} via .map","content":b64,"branch":BRANCH}
    if sha: payload['sha'] = sha
    resp2 = requests.put(url, headers=headers, json=payload)
    if resp2.status_code not in (200,201):
        print("Failed",fname,resp2.text)

print("Done")