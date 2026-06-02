# 🔧 Fix for Prefect Horizon Build Error

## The Problem

Your Prefect Horizon deployment is failing with an incomplete Docker build. The build logs show:

```
Building your server...
#0 building with "default" instance using docker driver
#1 transferring dockerfile: 1.40kB done
...
#6 sha256:e113665b194b... 12.11MB / 12.11MB 0.3s done
```

And then it stops or times out.

## Root Cause

The issue is caused by:
1. **Missing explicit Dockerfile** - Horizon was trying to auto-generate one
2. **Incorrect prefect.yaml configuration** - Using old Prefect Cloud format instead of Horizon format
3. **Build timeout** - Complex dependencies taking too long to install

## ✅ Solution Applied

I've created the following fixes:

### 1. Created `Dockerfile`
A proper Dockerfile that:
- Uses Python 3.12 (matching Horizon's base)
- Installs system dependencies (gcc, g++)
- Properly installs Python packages
- Sets correct entrypoint

### 2. Updated `prefect.yaml`
Simplified configuration for Horizon:
- Removed build/push/pull steps (Horizon handles these)
- Changed name to match your server: `mcpsnowflake`

### 3. Created `.dockerignore`
Excludes unnecessary files to speed up builds

## 🚀 Next Steps

### Step 1: Re-upload Files to Horizon

In the Prefect Horizon UI:

1. **Go to your server** (`mcpsnowflake`)
2. **Click "Configuration"** or "Settings"
3. **Upload/Update these files**:
   - ✅ `Dockerfile` (NEW - most important!)
   - ✅ `prefect.yaml` (UPDATED)
   - ✅ `.dockerignore` (NEW)
   - ✅ `server.py` (existing)
   - ✅ `flows.py` (existing)
   - ✅ `requirements.txt` (existing)

### Step 2: Verify Configuration

In Horizon UI, ensure:

**General Settings:**
- **Name**: `mcpsnowflake`
- **Entrypoint**: `server.py`
- **Python Version**: `3.12`
- **Dependencies**: `requirements.txt`

**Environment Variables:**
```
SNOWFLAKE_ACCOUNT={{ prefect.blocks.secret.snowflake-account }}
SNOWFLAKE_USERNAME={{ prefect.blocks.secret.snowflake-username }}
SNOWFLAKE_PASSWORD={{ prefect.blocks.secret.snowflake-password }}
SNOWFLAKE_WAREHOUSE={{ prefect.blocks.secret.snowflake-warehouse }}
SNOWFLAKE_DATABASE={{ prefect.blocks.secret.snowflake-database }}
SNOWFLAKE_ROLE={{ prefect.blocks.secret.snowflake-role }}
PORT=3000
```

### Step 3: Rebuild

1. Click **"Build"** or **"Deploy"** button
2. Watch the build logs
3. Build should now complete in 2-5 minutes

### Step 4: Expected Build Output

You should see:

```
Installing mcp-build-tools...
downloading uv 0.11.18 x86_64-unknown-linux-gnu
Starting build...
Downloading source...
Configuration:
  ├── Entrypoint: server.py
  ├── Python: 3.12
  └── Dependencies: requirements.txt
Authenticating with container registry...
Building your server...
#0 building with "default" instance using docker driver
#1 [1/6] FROM base image...
#2 [2/6] WORKDIR /app
#3 [3/6] RUN apt-get update && apt-get install...
#4 [4/6] COPY requirements.txt .
#5 [5/6] RUN pip install --no-cache-dir -r requirements.txt
#6 [6/6] COPY server.py flows.py .
#7 exporting to image
#8 => exporting layers
#9 => writing image
✅ Build successful!
```

## 🔍 If Build Still Fails

### Check 1: Dockerfile is Present
Ensure the `Dockerfile` is actually uploaded to Horizon. It should be visible in the file list.

### Check 2: Requirements.txt is Valid
Verify [`requirements.txt`](requirements.txt:1) has no syntax errors:
```
fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic==2.4.2
python-dotenv==1.0.0
prefect==2.14.21
griffe==0.38.1
snowflake-connector-python==3.12.3
python-multipart==0.0.6
```

### Check 3: Secrets are Created
Verify all 6 Snowflake secrets exist in Prefect Cloud:
- `snowflake-account`
- `snowflake-username`
- `snowflake-password`
- `snowflake-warehouse`
- `snowflake-database`
- `snowflake-role`

### Check 4: Build Logs
Look for specific errors in build logs:
- **"No such file"** → File not uploaded
- **"Package not found"** → Check requirements.txt
- **"Permission denied"** → Check Dockerfile permissions
- **"Timeout"** → Reduce dependencies or optimize Dockerfile

## 🎯 Alternative: Use Pre-built Image

If builds continue to fail, you can build locally and push:

```bash
# Build locally
cd snowflake-mcp-server
docker build -t your-registry/mcpsnowflake:latest .

# Push to registry
docker push your-registry/mcpsnowflake:latest

# In Horizon, use the pre-built image
# (Configure in Horizon UI under "Custom Image")
```

## 📊 Verification

Once build succeeds:

1. **Check Status**: Server should show "Running"
2. **Test Health**: `curl https://your-url.prefect.cloud/health`
3. **Check Logs**: Look for "Snowflake MCP Server is starting!"

## 🆘 Still Having Issues?

If the build still fails after these changes:

1. **Copy the full build logs** from Horizon
2. **Check for specific error messages**
3. **Verify all files are uploaded correctly**
4. **Try building the Docker image locally first** to isolate the issue:

```bash
cd snowflake-mcp-server
docker build -t test-build .
```

If local build works but Horizon fails, it's likely a Horizon configuration issue.

## 📞 Support Resources

- **Prefect Horizon Docs**: https://docs.prefect.io/latest/guides/deployment/horizon/
- **Prefect Slack**: https://prefect.io/slack (ask in #horizon channel)
- **Prefect Support**: support@prefect.io

## ✅ Summary

The key changes to fix your build error:

1. ✅ **Added explicit Dockerfile** - No more auto-generation
2. ✅ **Simplified prefect.yaml** - Horizon-compatible format
3. ✅ **Added .dockerignore** - Faster, cleaner builds
4. ✅ **Proper Python 3.12 base** - Matches Horizon environment

**Next action**: Re-upload these files to Horizon and rebuild!