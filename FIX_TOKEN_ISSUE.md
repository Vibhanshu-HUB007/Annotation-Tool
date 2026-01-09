# Fix GitHub Token Permission Issue

## Problem
You're getting a 403 error: "Permission denied to Vibhanshu-HUB007"

This means your token doesn't have the correct permissions to push to the repository.

## Solution: Create a New Token with Correct Permissions

### Step 1: Create a New Token

1. Go to: **https://github.com/settings/tokens**
2. Click: **"Generate new token"** → **"Generate new token (classic)"**
3. **Name**: `Annotation Tool Push`
4. **Expiration**: Choose your preference (90 days recommended)
5. **Scopes**: **CRITICAL - Check the `repo` checkbox**
   - This gives full control of private repositories
   - Make sure the entire `repo` section is checked, not just individual items
6. Click **"Generate token"**
7. **Copy the token immediately** (you won't see it again!)

### Step 2: Use the New Token

```bash
cd /media/vibhanshu92/Data/Annotation-Tool
./push_to_github.sh YOUR_NEW_TOKEN_HERE
```

## Alternative: Manual Push

If the script doesn't work, try manually:

```bash
cd /media/vibhanshu92/Data/Annotation-Tool
git remote set-url origin https://YOUR_NEW_TOKEN@github.com/Vibhanshu-HUB007/Annotation-Tool.git
git push -u origin main
```

## Verify Token Permissions

To check if your token has the right permissions:

```bash
curl -H "Authorization: token YOUR_TOKEN" https://api.github.com/user
```

If you see your user info, the token is valid. If you get an error, the token is invalid or expired.

## Common Issues

1. **Token doesn't have `repo` scope**: Create a new token and make sure `repo` is checked
2. **Token expired**: Generate a new token
3. **Repository doesn't exist**: Create it at https://github.com/new first
4. **Wrong username**: Make sure the repository URL matches your GitHub username

## Quick Test

Test your token with this command:

```bash
curl -H "Authorization: token YOUR_TOKEN" https://api.github.com/repos/Vibhanshu-HUB007/Annotation-Tool
```

If you see repository info, the token works. If you see "Bad credentials" or "Not Found", create a new token.
