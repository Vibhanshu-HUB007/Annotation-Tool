# How to Push to GitHub

Since GitHub CLI installation requires sudo access, here are two easy ways to push:

## Option 1: Use Personal Access Token (Easiest)

1. **Get a GitHub Personal Access Token:**
   - Go to: https://github.com/settings/tokens
   - Click "Generate new token (classic)"
   - Name it: "Annotation Tool Push"
   - Select scope: **repo** (check the box)
   - Click "Generate token"
   - **Copy the token immediately** (you won't see it again!)

2. **Push using the script:**
   ```bash
   ./push_to_github.sh YOUR_TOKEN_HERE
   ```

## Option 2: Manual Push with Token

1. **Get a token** (same as Option 1)

2. **Push manually:**
   ```bash
   git remote set-url origin https://YOUR_TOKEN@github.com/Vibhanshu-HUB007/Annotation-Tool.git
   git push -u origin main
   ```

## Option 3: Install GitHub CLI (if you have sudo access)

Run this in your terminal (will ask for password):
```bash
curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg && sudo chmod go+r /usr/share/keyrings/githubcli-archive-keyring.gpg && echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null && sudo apt update && sudo apt install gh -y
```

Then:
```bash
gh auth login
git push -u origin main
```

---

## Current Status

✅ **All code is committed and ready to push!**
- 67 files committed
- Commit message: "Initial commit: Oral Cytology WSI Annotation Tool with deployment configuration"

Just need authentication to push to GitHub.
