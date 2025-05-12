# SDU Shield Explorer (Gist-Backed)

## Setup (one-time)
1. Populate `d/directory_GPT/` and `d/virtual/` with your files.
2. Create a public Gist (as done) containing `file_tree.json`.
3. Set your GitHub token:
   ```
   export GITHUB_TOKEN=ghp_...  # must have gist scope
   ```

## Usage
- **Generate & publish** map:
  ```
  python file_master.py map
  ```
- **Explorer** always fetches latest map from the Gist:
  Open `index.html` in your browser or via GitHub Pages:
  https://whompinc.github.io/Files/
