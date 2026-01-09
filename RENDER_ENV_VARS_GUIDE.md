# How to Add Environment Variables in Render - Step by Step

## Visual Guide

### Step 1: Navigate to Your Service
1. Go to https://dashboard.render.com
2. You'll see a list of your services
3. Click on your **backend service** (the one that's already deployed)

### Step 2: Find the Environment Tab
You have two ways to access environment variables:

**Option A: Left Sidebar**
- Look at the left sidebar menu
- Click on **"Environment"** (it has a key icon 🔑)

**Option B: Top Tabs**
- Look at the top of the page
- You'll see tabs like: **Overview**, **Logs**, **Events**, **Environment**, **Settings**
- Click on **"Environment"** tab

### Step 3: Click on "Environment Variables" Section
Once you're on the Environment page, you'll see **three sections**:

1. **Environment Variables** ← **Click on this one!**
2. Secret Files
3. Linked Environment Groups

Click on the **"Environment Variables"** section to expand it.

### Step 4: Add Environment Variables
1. Inside the "Environment Variables" section, you'll see existing variables (if any) or an empty list
2. Look for a button that says **"Add Environment Variable"** (usually blue, at the top right)
3. Click it

### Step 4: Enter Each Variable

A popup or form will appear. For each variable:

1. **Key** field: Enter the variable name (e.g., `DATABASE_URL`)
2. **Value** field: Enter the variable value
3. Click **"Save"** or **"Add"**

Repeat for each variable you need to add.

## Example: Adding CORS_ORIGINS

1. Click **"Add Environment Variable"**
2. **Key**: `CORS_ORIGINS`
3. **Value**: 
   - If you have a frontend: `https://your-app.vercel.app`
   - If testing locally: `http://localhost:5173,http://localhost:3000`
   - If you want to allow all (development only): `*`
4. Click **"Save"**

## What Happens After Adding Variables?

- Render will **automatically redeploy** your service
- You'll see a new deployment in the **"Events"** tab
- Wait 2-3 minutes for deployment to complete
- Check **"Logs"** tab to verify everything started correctly

## Common Issues

### Can't Find Environment Tab?
- Make sure you're on the **service page** (not the dashboard list)
- Look for it in the left sidebar or top navigation

### Variables Not Saving?
- Make sure you click **"Save"** after entering each variable
- Check that the Key doesn't have spaces (use underscores: `DATABASE_URL` not `DATABASE URL`)

### Need to Edit a Variable?
- Find the variable in the list
- Click the **pencil/edit icon** next to it
- Update the value
- Click **"Save"**

### Need to Delete a Variable?
- Find the variable in the list
- Click the **trash/delete icon** next to it
- Confirm deletion

## Visual Layout (if you're stuck)

The Environment page looks like this:

```
┌─────────────────────────────────────┐
│  Environment                        │
├─────────────────────────────────────┤
│  ▼ Environment Variables            │  ← Click here!
│    [Add Environment Variable] [+]   │
│    Key              Value            │
│    ────────────────────────────────│
│    (your variables will appear here)│
│                                     │
│  Secret Files                       │
│                                     │
│  Linked Environment Groups          │
└─────────────────────────────────────┘
```

After clicking "Environment Variables", you'll see:

```
┌─────────────────────────────────────┐
│  Environment Variables              │
│  [Add Environment Variable]  [+]   │  ← Click this button
├─────────────────────────────────────┤
│  Key              Value            │
│  ──────────────────────────────────│
│  (empty or existing variables)     │
└─────────────────────────────────────┘
```

## Quick Checklist

- [ ] Opened Render Dashboard
- [ ] Clicked on backend service
- [ ] Found "Environment" tab/section
- [ ] Clicked "Add Environment Variable"
- [ ] Added `DATABASE_URL`
- [ ] Added `SECRET_KEY`
- [ ] Added `CORS_ORIGINS`
- [ ] Saved all variables
- [ ] Waited for auto-redeploy
- [ ] Checked logs for success

## Still Can't Find It?

1. Make sure you're logged into Render
2. Make sure you're on the correct service (the backend, not database)
3. Try refreshing the page
4. Look for "Environment" in both the sidebar AND top tabs
5. The button might say "Add Variable" or "Add Environment Variable"
