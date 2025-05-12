# SDU Shield Explorer

This repository hosts a browser-based file explorer of the `directory_GPT` (LOCAL) and `virtual` directories.

## Files

- `index.html`: Single‐page application that loads `file_tree.json` and displays files.
- `file_tree.json`: Auto‐generated JSON map of the directory structure.
- `file_master.py`: Script to regenerate `file_tree.json`.
- `directory_GPT/` and `virtual/`: Directories to browse.

## Setup

1. **Run Locally**  
   ```bash
   python file_master.py    # generates file_tree.json
   open index.html in a browser
   ```

2. **GitHub Pages**  
   - Push this repo to GitHub under `whompinc/Directory`.
   - Enable Pages on `main` branch, root folder.
   - Your site will be at `https://whompinc.github.io/Directory/`.

3. **Automatic Updates**  
   A GitHub Actions workflow (`.github/workflows/update-tree.yml`) regenerates `file_tree.json` on each push or via manual dispatch.

