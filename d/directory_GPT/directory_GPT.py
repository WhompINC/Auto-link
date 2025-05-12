#!/usr/bin/env python3
"""
Minimal Directory GPT Manager
Auto-initializes and maintains only the project root directory, with full command support.
"""
import os, sys, shutil, hashlib, zipfile
from pathlib import Path

# Root at script directory
BASE = Path(__file__).parent.resolve()
BOT_MASTER = BASE / 'bot_local_master'
CLOUD_ENV = BASE / 'cloud_env'
BACKUP = BASE / '.backup_rewind01'
ZIP_FILE = BASE / 'local_master.zip'

# Utility
def compute_md5(path: Path) -> str:
    h = hashlib.md5()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(4096), b''):
            h.update(chunk)
    return h.hexdigest()

# Core Commands
def map_cmd():
    for root, dirs, files in os.walk(str(BASE)):
        rel = os.path.relpath(root, str(BASE))
        print(rel + "/")
        for f in files:
            print("  " + f)

def open_cmd(path=""):
    tgt = BASE / path if path else BASE
    if tgt.is_dir():
        for p in sorted(tgt.iterdir()):
            print(p.name)
    elif tgt.is_file():
        print(tgt.read_text())
    else:
        print(f"[open] Not found: {path}")

def snapshot():
    if not BACKUP.exists():
        shutil.copytree(BASE, BACKUP)
        print(f"[snapshot] saved to {BACKUP}")
    else:
        print("[snapshot] already exists.")

def rewind():
    if BACKUP.exists():
        shutil.rmtree(BASE)
        shutil.copytree(BACKUP, BASE)
        print(f"[rewind] restored from {BACKUP}")
    else:
        print("[rewind] no snapshot.")

def macro():
    print("[macro] computing checksums...")
    for r, _, files in os.walk(str(BASE)):
        for f in files:
            compute_md5(Path(r)/f)
    print("[macro] done.")

def sync():
    if BOT_MASTER.exists():
        shutil.rmtree(BOT_MASTER)
    shutil.copytree(BASE, BOT_MASTER)
    print("[sync] mirror created at bot_local_master")

def package():
    with zipfile.ZipFile(ZIP_FILE, 'w', zipfile.ZIP_DEFLATED) as zf:
        for f in BOT_MASTER.rglob('*'):
            zf.write(f, f.relative_to(BASE))
    print(f"[package] created {ZIP_FILE}")

def debug():
    print(f"BASE: {BASE}")
    print(f"BOT_MASTER exists: {BOT_MASTER.exists()}")
    print(f"CLOUD_ENV exists: {CLOUD_ENV.exists()}")
    print(f"BACKUP exists: {BACKUP.exists()}")
    print(f"ZIP parent exists: {ZIP_FILE.parent.exists()}")

# Auto-run map once
print(f"[init] Managing directory: {BASE}")
map_cmd()

# Dispatch
if __name__ == '__main__':
    cmd = sys.argv[1] if len(sys.argv) > 1 else 'help'
    arg = sys.argv[2] if len(sys.argv) > 2 else ''
    commands = {
        'map': map_cmd,
        'open': lambda: open_cmd(arg),
        'snapshot': snapshot,
        'rewind': rewind,
        'macro': macro,
        'sync': sync,
        'package': package,
        'debug': debug,
        'help': lambda: print("Commands: map, open <path>, snapshot, rewind, macro, sync, package, debug")
    }
    func = commands.get(cmd)
    if func:
        func()
    else:
        print(f"Unknown command: {cmd}")
