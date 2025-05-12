#!/usr/bin/env python3
import os, json
from github import Github

GIST_ID = "cdfaad8036ec458507db2eb66da8de2c"
GIST_FILE = "file_tree.json"
DOC_ROOT = "d"
TOKEN = os.getenv("GITHUB_TOKEN")

if not TOKEN:
    raise SystemExit("Set GITHUB_TOKEN with gist scope")

def build_tree(path):
    tree={}
    for n in sorted(os.listdir(path)):
        f=os.path.join(path,n)
        if os.path.isdir(f):
            tree[n]=build_tree(f)
        else:
            tree[n]="file"
    return tree

data={b:build_tree(os.path.join(DOC_ROOT,b)) for b in sorted(os.listdir(DOC_ROOT)) if os.path.isdir(os.path.join(DOC_ROOT,b))}
content=json.dumps(data,indent=2)

gh=Github(TOKEN)
gist=gh.get_gist(GIST_ID)
gist.edit(files={GIST_FILE:{"content":content}})
print("✅ Gist updated")