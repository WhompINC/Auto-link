#!/usr/bin/env python3
import os, sys, json, zipfile

# Constants
BASE_DIR = os.path.dirname(__file__)
DOC_ROOT = os.path.join(BASE_DIR, 'd')  # directory containing branches
TREE_JSON = os.path.join(BASE_DIR, 'file_tree.json')
PATHS_TXT = os.path.join(BASE_DIR, 'file_paths.txt')
BUNDLE_PREFIX = "bundle"  # prefix for branch bundles

def build_tree(path):
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
    paths = []
    for root, _, files in os.walk(path):
        for f in files:
            rel = os.path.relpath(os.path.join(root, f), path)
            paths.append(rel)
    return sorted(paths)

def bundle_branch(branch, path):
    zip_name = f"{BUNDLE_PREFIX}_{branch}.zip"
    if os.path.exists(zip_name):
        os.remove(zip_name)
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zf:
        for root, _, files in os.walk(path):
            for f in files:
                absf = os.path.join(root, f)
                arc = os.path.join(branch, os.path.relpath(absf, path))
                zf.write(absf, arcname=arc)
    print(f"✅ Bundled {branch} -> {zip_name}")

def cmd_map():
    # Discover branches
    branches = [d for d in sorted(os.listdir(DOC_ROOT))
                if os.path.isdir(os.path.join(DOC_ROOT, d))]
    if not branches:
        print(f"No subdirectories in {DOC_ROOT}")
        return
    # Build tree data
    data = {}
    for branch in branches:
        data[branch] = build_tree(os.path.join(DOC_ROOT, branch))
    # Write JSON
    with open(TREE_JSON, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)
    print(f"✅ Wrote {TREE_JSON}")
    # Write flat paths
    with open(PATHS_TXT, 'w', encoding='utf-8') as f:
        for branch in branches:
            f.write(f"{branch} paths:\n")
            for p in gather_paths(os.path.join(DOC_ROOT, branch)):
                f.write(p + "\n")
            f.write("\n")
    print(f"✅ Wrote {PATHS_TXT}")
    # Bundle each
    for branch in branches:
        bundle_branch(branch, os.path.join(DOC_ROOT, branch))

def cmd_open():
    url = "https://whompinc.github.io/Files/"
    print(f"[Files]({url})")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: file_master.py map | open")
    cmd = sys.argv[1].lower()
    if cmd in ('map', '.map'):
        cmd_map()
    elif cmd in ('open', '.open'):
        cmd_open()