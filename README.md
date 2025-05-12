# Files Explorer

This repository hosts a browser-based explorer of the `d/` directory.

## Structure

- `index.html` — Single-page UI (collapsible sidebar, live search, downloads)
- `file_master.py` — Script to scan `d/*` and generate:
  - `file_tree.json` (directory map)
  - `file_paths.txt` (flat list)
  - `bundle_<branch>.zip` for each branch
- `d/`
  - **directory_GPT/** — LOCAL files
  - **virtual/** — VIRTUAL files
- `.github/workflows/update-tree.yml` — GitHub Action to auto-run `map` on push or manual dispatch

## Usage

1. **Publish Pages** on `main` branch root: https://whompinc.github.io/Files/
2. **Run map locally**:
   ```bash
   python file_master.py map
   ```
3. **Trigger Action** to update remotely:
   ```bash
   gh workflow run update-tree.yml --repo whompinc/Files --ref main
   ```
