#!/usr/bin/env python3
import os, json
from github import Github

# Config
GIST_ID   = "cdfaad8036ec458507db2eb66da8de2c"  # Your public Gist ID
DOC_ROOT  = "d"
TOKEN     = os.getenv("GITHUB_TOKEN")          # Must have 'gist' scope

if not TOKEN:
    raise SystemExit("Error: Please set GITHUB_TOKEN with gist write scope")

def build_tree(path):
    tree = {}
    for name in sorted(os.listdir(path)):
        full = os.path.join(path, name)
        tree[name] = build_tree(full) if os.path.isdir(full) else "file"
    return tree

data = {b: build_tree(os.path.join(DOC_ROOT, b)) for b in sorted(os.listdir(DOC_ROOT)) if os.path.isdir(os.path.join(DOC_ROOT, b))}
content = json.dumps(data, indent=2)

gh   = Github(TOKEN)
gist = gh.get_gist(GIST_ID)
gist.edit(files={ "file_tree.json": { "content": content } })
print("✅ Gist updated")
