#!/bin/bash

# Script to push to GitHub using Personal Access Token
# Usage: ./push_to_github.sh YOUR_GITHUB_TOKEN

if [ -z "$1" ]; then
    echo "Usage: ./push_to_github.sh YOUR_GITHUB_TOKEN"
    echo ""
    echo "To get a token:"
    echo "1. Go to https://github.com/settings/tokens"
    echo "2. Click 'Generate new token (classic)'"
    echo "3. Select 'repo' scope"
    echo "4. Copy the token and use it as the argument"
    exit 1
fi

TOKEN=$1
REPO_URL="https://${TOKEN}@github.com/Vibhanshu-HUB007/Annotation-Tool.git"

echo "Pushing to GitHub..."
git remote set-url origin $REPO_URL
git push -u origin main

echo "Done! If successful, your code is now on GitHub."
