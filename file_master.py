#!/usr/bin/env python3
import os, json, base64, requests, zipfile, io, sys

# ── CONFIG ───────────────────────────────────────────────────────────────────
OWNER           = "WhompINC"
REPO            = "Files"
BRANCH          = "main"
DOC_ROOT        = "d"   # contains directory_GPT/
FILE_TREE       = "file_tree.json"
GITHUB_TOKEN    = "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"
VIRTUAL_ZIP_URL = (
    "https://1drv.ms/u/c/82b91d7109d5b7b7/"
    "ESVpWwMZGMRPgbEEPelSUJABFk68nExnkxptl1g_aZmd3w"
)
# ──────────────────────────────────────────────────────────────────────────────

def build_tree(path):
    t = {}
    for name in sorted(os.listdir(path)):
        full = os.path.join(path, name)
        if os.path.isdir(full):
            t[name] = build_tree(full)
        else:
            t[name] = "file"
    return t

def build_zip_tree_from_url(url):
    r = requests.get(url)
    r.raise_for_status()
    z = zipfile.ZipFile(io.BytesIO(r.content))
    entries = sorted(z.namelist())
    tops = {e.split('/',1)[0] for e in entries if '/' in e}
    prefix = next(iter(tops))+'/' if len(tops)==1 else None
    tree = {}
    for e in entries:
        if prefix and e.startswith(prefix):
            rel = e[len(prefix):]
        else:
            rel = e
        if not rel:
            continue
        parts = rel.rstrip('/').split('/')
        node = tree
        for part in parts[:-1]:
            node = node.setdefault(part, {})
        if e.endswith('/'):
            node.setdefault(parts[-1], {})
        else:
            node[parts[-1]] = "file"
    return tree

def main():
    data = {}
    # Local
    local_dir = os.path.join(DOC_ROOT, "directory_GPT")
    if os.path.isdir(local_dir):
        data["directory_GPT"] = build_tree(local_dir)
    else:
        print("⚠️  Warning: d/directory_GPT not found", file=sys.stderr)
    # Virtual
    try:
        print("📥 Downloading and mapping virtual.zip…")
        data["virtual"] = build_zip_tree_from_url(VIRTUAL_ZIP_URL)
    except Exception as e:
        print("❌ Error mapping virtual.zip:", e, file=sys.stderr)
        data["virtual"] = {}

    # Write JSON
    content = json.dumps(data, indent=2)
    with open(FILE_TREE, "w") as f:
        f.write(content)

    # Push to GitHub
    api = f"https://api.github.com/repos/{OWNER}/{REPO}/contents/{FILE_TREE}"
    hdr = {"Authorization":f"Bearer {GITHUB_TOKEN}","Accept":"application/vnd.github+json"}
    r1 = requests.get(api, headers=hdr)
    sha = r1.json().get("sha") if r1.status_code == 200 else None

    payload = {
        "message": f"ci: regenerate {FILE_TREE} via .map",
        "content": base64.b64encode(content.encode()).decode(),
        "branch": BRANCH
    }
    if sha:
        payload["sha"] = sha

    r2 = requests.put(api, headers=hdr, json=payload)
    if r2.status_code in (200,201):
        print(f"✅ {FILE_TREE} updated on GitHub")
    else:
        print(f"❌ Failed to update: {r2.status_code} {r2.text}", file=sys.stderr)

if __name__ == "__main__":
    if len(sys.argv) >= 2 and sys.argv[1] == "map":
        main()
    else:
        print("Usage: python file_master.py map")
        sys.exit(1)
