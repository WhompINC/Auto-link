# Files Explorer

This repo hosts an interactive file explorer on GitHub Pages.

- **index.html**: Explorer UI
- **file_master.py**: Generates file_tree.json, file_paths.txt, and bundle_*.zip
- **file_tree.json**: Directory map (auto-generated)
- **file_paths.txt**: Flat list of file paths
- **bundle_*.zip**: Zipped branches
- **d/**: Contains branches (directory_GPT, virtual, etc.)
- **.github/workflows/update-tree.yml**: CI to regenerate on push or manual dispatch

## Usage

1. Place your files under `d/directory_GPT/` and `d/virtual/`
2. Commit & push to main.
3. The workflow runs on push → regenerates map.
4. View at https://whompinc.github.io/Files/
