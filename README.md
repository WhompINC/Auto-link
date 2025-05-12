# SDU Shield Explorer (Gist-Backed)

## Setup
1. Place files under `d/directory_GPT/` and `d/virtual/`.
2. Ensure GITHUB_TOKEN env var is set to a PAT with 'gist' scope.

## Usage
- To update the map: `python file_master.py map`
- The `index.html` fetches from the configured Gist URL.
