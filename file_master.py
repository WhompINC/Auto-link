#!/usr/bin/env python3
import os, json, base64, requests, zipfile, io

OWNER        = "WhompINC"
REPO         = "Files"
BRANCH       = "main"
DOC_ROOT     = "d"
FILE_TREE    = "file_tree.json"
GITHUB_TOKEN = "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"
VIRTUAL_ZIP_URL = "https://1drv.ms/u/c/82b91d7109d5b7b7/ESVpWwMZGMRPgbEEPelSUJABFk68nExnkxptl1g_aZmd3w"

def build_tree(path):
    tree = {}
    for name in sorted(os.listdir(path)):
        full = os.path.join(path, name)
        if os.path.isdir(full):
            tree[name] = build_tree(full)
        else:
            tree[name] = "file"
    return tree

def build_zip_tree_from_url(url):
    resp = requests.get(url)
    resp.raise_for_status()
    z = zipfile.ZipFile(io.BytesIO(resp.content))
    paths = [m for m in sorted(z.namelist()) if not m.endswith('/')]
    # Determine common top‐level folder (if any)
    tops = set(p.split('/',1)[0] for p in paths)
    strip_prefix = None
    if len(tops) == 1:
        strip_prefix = next(iter(tops)) + '/'
    tree = {}
    for member in paths:
        # remove prefix if it matches
        if strip_prefix and member.startswith(strip_prefix):
            member = member[len(strip_prefix):]
        parts = member.split('/')
        node = tree
        for p in parts[:-1]:
            node = node.setdefault(p, {})
        node[parts[-1]] = "file"
    return tree

def main():
    data = {}
    # Local
    local_dir = os.path.join(DOC_ROOT, "directory_GPT")
    if os.path.isdir(local_dir):
        data["directory_GPT"] = build_tree(local_dir)
    else:
        print("Warning: d/directory_GPT not found")

    # Virtual
    try:
        print("Fetching virtual.zip…")
        data["virtual"] = build_zip_tree_from_url(VIRTUAL_ZIP_URL)
    except Exception as e:
        print("Error mapping virtual.zip:", e)
        data["virtual"] = {}

    # Write JSON
    content = json.dumps(data, indent=2)
    with open(FILE_TREE, "w") as f:
        f.write(content)

    # Push to GitHub
    api = f"https://api.github.com/repos/{OWNER}/{REPO}/contents/{FILE_TREE}"
    hdr = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept":        "application/vnd.github+json"
    }
    r1 = requests.get(api, headers=hdr)
    sha = r1.json().get("sha") if r1.status_code == 200 else None

    payload = {
        "message": f"ci: regenerate {FILE_TREE} via .map",
        "content": base64.b64encode(content.encode()).decode(),
        "branch":  BRANCH
    }
    if sha: payload["sha"] = sha

    r2 = requests.put(api, headers=hdr, json=payload)
    if r2.status_code in (200,201):
        print(f"✅ {FILE_TREE} updated on GitHub")
    else:
        print(f"❌ Failed to update: {r2.status_code} {r2.text}")

if __name__ == "__main__":
    main()
