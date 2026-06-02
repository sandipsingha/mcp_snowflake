# 🚀 Redeployment Guide - Fixed Prefect Cloud Secrets

## What Was Fixed

The `server.py` file now properly loads credentials from **Prefect Cloud Secrets** instead of just environment variables. The updated `get_snowflake_config()` function:

1. **First tries** to load from Prefect Cloud Secrets (for deployed flows)
2. **Falls back** to environment variables (for local development)
3. **Validates** that all required credentials are present

## 📋 Steps to Redeploy

### Step 1: Upload Secrets to Prefect Cloud (if not done already)

```bash
python setup_secrets.py
```

Choose option **"1"** to upload secrets. You should see:
```
✅ Created secret: snowflake-account
✅ Created secret: snowflake-username
✅ Created secret: snowflake-password
✅ Created secret: snowflake-warehouse
✅ Created secret: snowflake-database
✅ Created secret: snowflake-role
```

### Step 2: Redeploy the Flows

```bash
python deployment.py
```

This will:
- Deploy the updated code to Prefect Cloud
- The flows will now use the Prefect Secrets

### Step 3: Test the Deployment

Go to Prefect Cloud UI and manually trigger a flow:

1. Navigate to: https://app.prefect.cloud/
2. Click **"Deployments"** in the left sidebar
3. Click on **"get-customers"** deployment
4. Click **"Run"** → **"Quick Run"**
5. Watch the logs - you should see:
   ```
   🔍 Attempting to load credentials from Prefect Cloud Secrets...
   ✅ Connected to Snowflake: YOUR_DATABASE
   ✅ Query executed successfully: X rows
   ```

## 🔍 Verify Secrets Are Working

### Option A: Check in Prefect Cloud UI

1. Go to https://app.prefect.cloud/
2. Click **"Blocks"** → Filter by **"Secret"**
3. You should see all 6 secrets listed

### Option B: Run the verification script

```bash
python -c "from prefect.blocks.system import Secret; print('✅ Secrets loaded:', Secret.load('snowflake-account').get()[:5] + '...')"
```

## 🐛 Troubleshooting

### If flows still crash:

1. **Check the logs** in Prefect Cloud UI for the specific error
2. **Verify secrets exist**:
   ```bash
   python setup_secrets.py
   # Choose option "2" to list secrets
   ```

3. **Check your .env file** has correct values:
   ```bash
   type .env
   ```

4. **Redeploy with verbose logging**:
   ```bash
   python deployment.py
   ```

### Common Issues:

❌ **"Secret 'snowflake-account' not found"**
- Solution: Run `python setup_secrets.py` and choose option "1"

❌ **"Missing Snowflake credentials"**
- Solution: Check your `.env` file has all required values

❌ **"Authentication failed"**
- Solution: Verify your Snowflake credentials are correct in `.env`

## 📊 Expected Behavior

### Before Fix:
```
ERROR: Process for flow run exited with status code: 1
```

### After Fix:
```
INFO: 🔍 Attempting to load credentials from Prefect Cloud Secrets...
INFO: ✅ Connected to Snowflake: YOUR_DATABASE
INFO: ✅ Query executed successfully: 150 rows
```

## 🎯 Next Steps

Once deployment is successful:

1. Test all 5 deployed flows in Prefect Cloud
2. Verify data is being retrieved correctly
3. Set up scheduled runs if needed
4. Monitor flow runs in the Prefect Cloud dashboard

## 📝 Key Changes Made

**File: `server.py`**
- Added `from prefect.blocks.system import Secret`
- Modified `get_snowflake_config()` to try Prefect Secrets first
- Added fallback to environment variables for local development
- Added validation to ensure all credentials are present

This ensures the code works both:
- ✅ **Locally** (using `.env` file)
- ✅ **In Prefect Cloud** (using Prefect Secrets)