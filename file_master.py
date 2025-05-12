#!/usr/bin/env python3
import os, json
from github import Github

# Config
GIST_ID   = "cdfaad8036ec458507db2eb66da8de2c"
DOC_ROOT  = "d"
import os
TOKEN = os.getenv("GITHUB_TOKEN")
if not TOKEN:
    raise SystemExit("Error: please set GITHUB_TOKEN as an environment variable.")


def build_tree(path):
    tree={}
    for name in sorted(os.listdir(path)):
        full=os.path.join(path,name)
        tree[name]=build_tree(full) if os.path.isdir(full) else "file"
    return tree

data={}
for branch in sorted(os.listdir(DOC_ROOT)):
    p=os.path.join(DOC_ROOT,branch)
    if os.path.isdir(p):
        data[branch]=build_tree(p)

content=json.dumps(data,indent=2)
gh=Github(TOKEN)
gist=gh.get_gist(GIST_ID)
gist.edit(files={ "file_tree.json": { "content": content } })
print("✅ Gist updated with latest map")