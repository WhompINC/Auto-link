#!/usr/bin/env python3
import os, sys, json, zipfile, subprocess

BASE_DIR = os.path.dirname(__file__)
DOC_ROOT = os.path.join(BASE_DIR, 'd')
TREE_JSON = os.path.join(BASE_DIR, 'file_tree.json')
PATHS_TXT = os.path.join(BASE_DIR, 'file_paths.txt')
BUNDLE_PREFIX = "bundle"

def build_tree(path):
    tree = {}
    for name in sorted(os.listdir(path)):
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
    print(f"Bundled {branch} -> {zip_name}")
    return zip_name

def cmd_map():
    branches = [d for d in sorted(os.listdir(DOC_ROOT)) if os.path.isdir(os.path.join(DOC_ROOT, d))]
    if not branches:
        print("No branches found.")
        return
    data = {b: build_tree(os.path.join(DOC_ROOT, b)) for b in branches}
    with open(TREE_JSON, 'w') as f:
        json.dump(data, f, indent=2)
    with open(PATHS_TXT, 'w') as f:
        for b in branches:
            f.write(f"{b} paths:\n")
            for p in gather_paths(os.path.join(DOC_ROOT, b)):
                f.write(p + "\n")
            f.write("\n")
    bundles = [bundle_branch(b, os.path.join(DOC_ROOT, b)) for b in branches]
    # Auto commit & push
    try:
        subprocess.run(["git", "add", "file_tree.json", "file_paths.txt"] + bundles, check=True)
        subprocess.run(["git", "commit", "-m", "ci: regen map & bundles via .map"], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("Pushed updates to GitHub.")
    except subprocess.CalledProcessError as e:
        print("Git push failed:", e)

def cmd_open():
    print("[Files](https://whompinc.github.io/Files/)")

if __name__=="__main__":
    if len(sys.argv)<2:
        print("Usage: python file_master.py map|open")
        sys.exit(1)
    if sys.argv[1] in ("map", ".map"):
        cmd_map()
    else:
        cmd_open()
