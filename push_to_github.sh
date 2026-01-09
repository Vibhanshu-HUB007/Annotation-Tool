#!/bin/bash

# Script to push to GitHub using Personal Access Token
# Usage: ./push_to_github.sh YOUR_GITHUB_TOKEN

if [ -z "$1" ]; then
    echo "Usage: ./push_to_github.sh YOUR_GITHUB_TOKEN"
    echo ""
    echo "To get a token with correct permissions:"
    echo "1. Go to https://github.com/settings/tokens"
    echo "2. Click 'Generate new token (classic)'"
    echo "3. IMPORTANT: Select 'repo' scope (check the entire 'repo' checkbox)"
    echo "4. Click 'Generate token'"
    echo "5. Copy the token and use it as the argument"
    exit 1
fi

TOKEN=$1

# Verify token has repo access
echo "Verifying token permissions..."
REPO_CHECK=$(curl -s -H "Authorization: token $TOKEN" -H "Accept: application/vnd.github.v3+json" https://api.github.com/repos/Vibhanshu-HUB007/Annotation-Tool 2>&1)
if echo "$REPO_CHECK" | grep -q "Bad credentials\|Not Found"; then
    echo "ERROR: Token authentication failed or repository not accessible"
    echo "Please ensure:"
    echo "1. Token has 'repo' scope enabled"
    echo "2. Repository exists at: https://github.com/Vibhanshu-HUB007/Annotation-Tool"
    exit 1
fi

echo "Token verified. Pushing to GitHub..."

# Use token in URL format
REPO_URL="https://${TOKEN}@github.com/Vibhanshu-HUB007/Annotation-Tool.git"

# Reset remote and push
git remote set-url origin $REPO_URL
git push -u origin main

if [ $? -eq 0 ]; then
    echo "✅ Success! Your code is now on GitHub!"
    echo "Repository: https://github.com/Vibhanshu-HUB007/Annotation-Tool"
else
    echo "❌ Push failed. Common issues:"
    echo "1. Token doesn't have 'repo' scope - create a new token with full repo access"
    echo "2. Repository doesn't exist - create it at https://github.com/new"
    echo "3. Token expired - generate a new token"
fi
