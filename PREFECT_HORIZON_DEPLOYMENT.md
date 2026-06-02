# Prefect Horizon Deployment Guide

## 🚀 Overview

This guide explains how to deploy the Snowflake MCP Server to **Prefect Horizon**, the new managed deployment platform from Prefect.

## 📋 Prerequisites

1. **Prefect Cloud Account** with Horizon access
2. **Snowflake Credentials** ready
3. **GitHub Repository** (optional, for CI/CD)

## 🔧 Configuration Files

The following files are configured for Prefect Horizon:

### 1. `Dockerfile`
- Uses Python 3.12 (matching Horizon's base image)
- Installs system dependencies (gcc, g++)
- Installs Python packages from `requirements.txt`
- Exposes port 3000
- Runs the FastAPI server

### 2. `prefect.yaml`
- Simplified configuration for Horizon
- No build/push/pull steps (Horizon handles this)
- Name matches your Horizon server name: `mcpsnowflake`

### 3. `.dockerignore`
- Excludes unnecessary files from Docker build
- Reduces image size and build time

## 📝 Step-by-Step Deployment

### Step 1: Set Up Secrets in Prefect Cloud

Before deploying, create these secrets in Prefect Cloud:

1. Go to https://app.prefect.cloud/
2. Navigate to **Blocks** → **Secrets**
3. Create the following secrets:

| Secret Name | Value |
|------------|-------|
| `snowflake-account` | Your Snowflake account identifier |
| `snowflake-username` | Your Snowflake username |
| `snowflake-password` | Your Snowflake password |
| `snowflake-warehouse` | Your Snowflake warehouse name |
| `snowflake-database` | Your Snowflake database name |
| `snowflake-role` | Your Snowflake role |

### Step 2: Deploy to Prefect Horizon

#### Option A: Deploy via Prefect Horizon UI

1. **Go to Prefect Horizon**:
   - Navigate to https://app.prefect.cloud/
   - Click on **Servers** in the left sidebar
   - Click **Create Server** or select your existing server

2. **Configure Server**:
   - **Name**: `mcpsnowflake` (must match `prefect.yaml`)
   - **Entrypoint**: `server.py`
   - **Python Version**: 3.12
   - **Dependencies**: `requirements.txt`

3. **Set Environment Variables**:
   Add these environment variables in the Horizon UI:
   ```
   SNOWFLAKE_ACCOUNT={{ prefect.blocks.secret.snowflake-account }}
   SNOWFLAKE_USERNAME={{ prefect.blocks.secret.snowflake-username }}
   SNOWFLAKE_PASSWORD={{ prefect.blocks.secret.snowflake-password }}
   SNOWFLAKE_WAREHOUSE={{ prefect.blocks.secret.snowflake-warehouse }}
   SNOWFLAKE_DATABASE={{ prefect.blocks.secret.snowflake-database }}
   SNOWFLAKE_ROLE={{ prefect.blocks.secret.snowflake-role }}
   PORT=3000
   ```

4. **Upload Code**:
   - Upload your project files or connect to GitHub
   - Ensure `server.py`, `flows.py`, `requirements.txt`, and `Dockerfile` are included

5. **Deploy**:
   - Click **Deploy** or **Build**
   - Wait for the build to complete (may take 2-5 minutes)

#### Option B: Deploy via CLI (if supported)

```bash
# Navigate to project directory
cd snowflake-mcp-server

# Login to Prefect Cloud
prefect cloud login

# Deploy to Horizon
prefect deploy --name mcpsnowflake
```

### Step 3: Verify Deployment

1. **Check Build Logs**:
   - In Horizon UI, go to your server
   - Click on **Build Logs**
   - Verify the build completed successfully

2. **Check Server Status**:
   - Server should show as "Running" or "Healthy"
   - Check the **Logs** tab for any errors

3. **Test Endpoints**:
   Once deployed, Horizon will provide a URL. Test it:
   ```bash
   # Replace with your Horizon server URL
   curl https://your-server-url.prefect.cloud/health
   ```

   Expected response:
   ```json
   {
     "status": "healthy",
     "database": "TELECOM_ANALYTICS",
     "warehouse": "COMPUTE_WH",
     "version": "2.0.0",
     "framework": "FastAPI + Prefect"
   }
   ```

## 🔍 Troubleshooting

### Build Fails with "Failed to install dependencies"

**Cause**: Missing system dependencies or incompatible package versions

**Solution**:
1. Check [`Dockerfile`](Dockerfile:1) has gcc and g++ installed
2. Verify [`requirements.txt`](requirements.txt:1) versions are compatible
3. Check build logs for specific error messages

### Build Timeout

**Cause**: Build taking too long (>10 minutes)

**Solution**:
1. Optimize [`Dockerfile`](Dockerfile:1) by using multi-stage builds
2. Reduce dependencies in [`requirements.txt`](requirements.txt:1)
3. Use Docker layer caching

### Server Starts but Crashes

**Cause**: Missing environment variables or Snowflake connection issues

**Solution**:
1. Verify all secrets are created in Prefect Cloud
2. Check environment variables are correctly set in Horizon
3. Test Snowflake credentials locally first
4. Check server logs in Horizon UI

### "Module not found" Errors

**Cause**: Missing files in deployment

**Solution**:
1. Ensure [`server.py`](server.py:1) and [`flows.py`](flows.py:1) are uploaded
2. Check [`.dockerignore`](.dockerignore:1) isn't excluding necessary files
3. Verify all imports in [`server.py`](server.py:1) are in [`requirements.txt`](requirements.txt:1)

## 📊 Monitoring

### View Logs
```bash
# In Horizon UI
Servers → mcpsnowflake → Logs
```

### Check Metrics
```bash
# In Horizon UI
Servers → mcpsnowflake → Observability
```

### Test Endpoints
```bash
# Health check
curl https://your-server-url.prefect.cloud/health

# List schemas
curl https://your-server-url.prefect.cloud/mcp/schemas

# Get customers
curl https://your-server-url.prefect.cloud/mcp/customers
```

## 🔄 Updating Deployment

To update your deployment:

1. **Make code changes** locally
2. **Commit and push** to GitHub (if using Git integration)
3. **Rebuild in Horizon**:
   - Go to Servers → mcpsnowflake
   - Click **Rebuild** or **Deploy**
4. **Wait for build** to complete
5. **Verify** the changes are live

## 🎯 Best Practices

1. **Use Secrets**: Never hardcode credentials in code
2. **Monitor Logs**: Regularly check logs for errors
3. **Test Locally First**: Always test changes locally before deploying
4. **Version Control**: Use Git for code management
5. **Environment Variables**: Use environment variables for configuration
6. **Health Checks**: Implement proper health check endpoints
7. **Error Handling**: Add comprehensive error handling in code

## 📞 Support

- **Prefect Docs**: https://docs.prefect.io/
- **Prefect Slack**: https://prefect.io/slack
- **Horizon Docs**: https://docs.prefect.io/latest/guides/deployment/horizon/

## 🎉 Success!

Once deployed, your Snowflake MCP Server will be:
- ✅ Running 24/7 on Prefect's infrastructure
- ✅ Automatically scaled and managed
- ✅ Accessible via a public URL
- ✅ Integrated with Prefect Cloud for monitoring

You can now connect this server to IBM ICA Context Studio!