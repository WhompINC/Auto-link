#!/usr/bin/env python3
import os, sys, json, zipfile

# Constants
DOC_ROOT      = os.path.join(os.path.dirname(__file__), 'd')  # e.g. /mnt/data/d
TREE_JSON     = "file_tree.json"
PATHS_TXT     = "file_paths.txt"
BUNDLE_PREFIX = "bundle"  # will create bundle_<branch>.zip for each

def build_tree(path):
    """Recursively build a JSON-like tree, marking files as "file"."""
    tree = {}
    try:
        entries = sorted(os.listdir(path))
    except FileNotFoundError:
        return tree
    for name in entries:
        full = os.path.join(path, name)
        if os.path.isdir(full):
            tree[name] = build_tree(full)
        else:
            tree[name] = "file"
    return tree

def gather_paths(path):
    """Return a flat list of relative file paths under 'path'."""
    paths = []
    for root, _, files in os.walk(path):
        for f in files:
            rel = os.path.relpath(os.path.join(root, f), path)
            paths.append(rel)
    return sorted(paths)

def bundle_branch(branch, path):
    """Zip up the contents of 'path' into bundle_<branch>.zip."""
    zip_name = f"{BUNDLE_PREFIX}_{branch}.zip"
    # Remove old zip
    if os.path.exists(zip_name):
        os.remove(zip_name)
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zf:
        for root, _, files in os.walk(path):
            for f in files:
                absf = os.path.join(root, f)
                # store files under branch/...
                arc = os.path.join(branch, os.path.relpath(absf, path))
                zf.write(absf, arcname=arc)
    print(f"✅ Bundled {branch} → {zip_name}")

def cmd_map():
    # 1. Discover branches
    branches = [
        d for d in sorted(os.listdir(DOC_ROOT))
        if os.path.isdir(os.path.join(DOC_ROOT, d))
    ]
    if not branches:
        print(f"No subdirectories found in {DOC_ROOT}; nothing to map.")
        return

    # 2. Build combined tree
    data = {}
    for branch in branches:
        path = os.path.join(DOC_ROOT, branch)
        data[branch] = build_tree(path)

    # 3. Write JSON tree
    with open(TREE_JSON, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)
    print(f"✅ {TREE_JSON} updated")

    # 4. Write flat paths
    with open(PATHS_TXT, 'w', encoding='utf-8') as f:
        for branch in branches:
            f.write(f"{branch} paths:\n")
            for p in gather_paths(os.path.join(DOC_ROOT, branch)):
                f.write(p + "\n")
            f.write("\n")
    print(f"✅ {PATHS_TXT} updated")

    # 5. Bundle each branch
    for branch in branches:
        bundle_branch(branch, os.path.join(DOC_ROOT, branch))

def cmd_open():
    """Print the markdown link to your Pages site."""
    url = "https://whompinc.github.io/Files/"
    print(f"[Files]({url})")

if __name__ == "__main__":
    if len(sys.argv) < 2:
