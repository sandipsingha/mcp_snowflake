# 🚀 Deploy to Prefect Horizon from GitHub

## ✅ Current Status

You've successfully:
- ✅ Connected GitHub repository: `sandipsingha/mcp_snowflake`
- ✅ Pushed the fixed configuration files to GitHub
- ✅ Ready to deploy!

## 📋 Step-by-Step Deployment

### Step 1: Navigate to Servers

1. In Prefect Horizon, click **"MCP Registry"** in the left sidebar (under "Operate")
2. You should see your existing server `mcpsnowflake` or click **"+ Create Server"** if starting fresh

### Step 2: Create/Update Server Configuration

Click on your server or create a new one with these settings:

#### **General Configuration**
```
Name: mcpsnowflake
Description: Snowflake MCP Server for IBM ICA Context Studio
```

#### **Source Configuration**
```
Source Type: GitHub
Repository: sandipsingha/mcp_snowflake
Branch: main (or your default branch)
Path: snowflake-mcp-server (if your files are in a subdirectory)
```

#### **Build Configuration**
```
Entrypoint: server.py
Python Version: 3.12
Dependencies: requirements.txt
```

**Important**: Horizon will automatically detect and use your `Dockerfile` from the repository!

#### **Environment Variables**

Add these in the "Environment" section:

```bash
SNOWFLAKE_ACCOUNT={{ prefect.blocks.secret.snowflake-account }}
SNOWFLAKE_USERNAME={{ prefect.blocks.secret.snowflake-username }}
SNOWFLAKE_PASSWORD={{ prefect.blocks.secret.snowflake-password }}
SNOWFLAKE_WAREHOUSE={{ prefect.blocks.secret.snowflake-warehouse }}
SNOWFLAKE_DATABASE={{ prefect.blocks.secret.snowflake-database }}
SNOWFLAKE_ROLE={{ prefect.blocks.secret.snowflake-role }}
PORT=3000
```

### Step 3: Verify Secrets Exist

Before deploying, ensure these secrets are created in Prefect Cloud:

1. Go to **Blocks** → **Secrets** (in the left sidebar)
2. Verify these 6 secrets exist:
   - `snowflake-account`
   - `snowflake-username`
   - `snowflake-password`
   - `snowflake-warehouse`
   - `snowflake-database`
   - `snowflake-role`

If any are missing, create them now.

### Step 4: Deploy/Build

1. Click **"Save"** or **"Deploy"** button
2. Horizon will:
   - ✅ Clone your GitHub repository
   - ✅ Detect the `Dockerfile`
   - ✅ Build the Docker image
   - ✅ Deploy the server

3. **Watch the build logs** - should take 2-5 minutes

### Step 5: Expected Build Output

You should see something like:

```
Cloning repository sandipsingha/mcp_snowflake...
✅ Repository cloned successfully

Detecting configuration...
✅ Found Dockerfile
✅ Found requirements.txt
✅ Found server.py

Building Docker image...
#1 [1/6] FROM python:3.12-slim
#2 [2/6] WORKDIR /app
#3 [3/6] RUN apt-get update && apt-get install -y gcc g++
#4 [4/6] COPY requirements.txt .
#5 [5/6] RUN pip install --no-cache-dir -r requirements.txt
#6 [6/6] COPY server.py flows.py .
✅ Build successful!

Starting server...
✅ Server is running
```

### Step 6: Verify Deployment

Once the build completes:

1. **Check Server Status**:
   - Should show "Running" or "Healthy" with a green indicator

2. **Get Server URL**:
   - Horizon will provide a URL like: `https://mcpsnowflake-xxxxx.prefect.cloud`

3. **Test Health Endpoint**:
   ```bash
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

4. **Test MCP Endpoints**:
   ```bash
   # List schemas
   curl https://your-server-url.prefect.cloud/mcp/schemas

   # Get customers
   curl https://your-server-url.prefect.cloud/mcp/customers
   ```

## 🔄 Updating Your Deployment

When you make changes to your code:

### Option A: Automatic Deployment (Recommended)

1. **Push changes to GitHub**:
   ```bash
   git add .
   git commit -m "Update server configuration"
   git push origin main
   ```

2. **Trigger rebuild in Horizon**:
   - Go to your server in Horizon
   - Click **"Rebuild"** or **"Deploy"** button
   - Horizon will pull latest code and rebuild

### Option B: Manual Deployment

1. Make changes locally
2. Push to GitHub
3. In Horizon, click **"Rebuild"**

## 🔍 Troubleshooting

### Build Fails: "Repository not found"

**Solution**: 
- Verify repository name is correct: `sandipsingha/mcp_snowflake`
- Check GitHub permissions in Integrations
- Ensure repository is not private (or grant Horizon access)

### Build Fails: "Dockerfile not found"

**Solution**:
- Verify `Dockerfile` is in the repository root or specified path
- Check the "Path" setting in server configuration
- If files are in `snowflake-mcp-server/` subdirectory, set Path to `snowflake-mcp-server`

### Build Fails: "Requirements installation failed"

**Solution**:
- Check `requirements.txt` syntax
- Verify all package versions are compatible
- Look at build logs for specific package errors

### Server Starts but Crashes

**Solution**:
- Check server logs in Horizon
- Verify all environment variables are set
- Ensure secrets are created and accessible
- Test Snowflake connection locally first

### "Module not found" Error

**Solution**:
- Ensure both `server.py` and `flows.py` are in repository
- Check imports in `server.py` match packages in `requirements.txt`
- Verify `Dockerfile` copies all necessary files

## 📊 Monitoring

### View Logs
```
Horizon → Servers → mcpsnowflake → Logs
```

### Check Build History
```
Horizon → Servers → mcpsnowflake → Build Logs
```

### Monitor Performance
```
Horizon → Servers → mcpsnowflake → Observability
```

## 🎯 Best Practices

1. **Use Git Tags**: Tag releases for version control
   ```bash
   git tag -a v1.0.0 -m "Initial release"
   git push origin v1.0.0
   ```

2. **Branch Strategy**: Use branches for development
   - `main` → Production
   - `develop` → Testing
   - `feature/*` → New features

3. **Environment-Specific Configs**: Use different branches or configs for dev/staging/prod

4. **Monitor Logs**: Regularly check logs for errors

5. **Test Locally First**: Always test changes locally before pushing

## 🔐 Security Notes

- ✅ Never commit `.env` files to GitHub
- ✅ Use Prefect Secrets for sensitive data
- ✅ Keep `.gitignore` updated
- ✅ Use environment variables for configuration
- ✅ Regularly rotate credentials

## 📞 Need Help?

- **Prefect Horizon Docs**: https://docs.prefect.io/latest/guides/deployment/horizon/
- **GitHub Integration**: https://docs.prefect.io/latest/guides/deployment/horizon/github/
- **Prefect Slack**: https://prefect.io/slack

## ✅ Quick Checklist

Before deploying, verify:

- [ ] GitHub repository connected in Horizon
- [ ] All files pushed to GitHub (Dockerfile, server.py, flows.py, requirements.txt)
- [ ] All 6 Snowflake secrets created in Prefect Cloud
- [ ] Server configuration set correctly (entrypoint, python version, etc.)
- [ ] Environment variables configured
- [ ] Repository path is correct (if files are in subdirectory)

## 🎉 Success!

Once deployed, your server will:
- ✅ Auto-deploy on git push (if configured)
- ✅ Run 24/7 on Prefect infrastructure
- ✅ Scale automatically
- ✅ Be accessible via public URL
- ✅ Integrate with IBM ICA Context Studio

**Your Snowflake MCP Server is now live!** 🚀