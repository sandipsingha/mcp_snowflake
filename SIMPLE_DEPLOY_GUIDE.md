# 🚀 Simple Deployment Guide (Hardcoded Credentials)

## ✅ What Changed

The Snowflake credentials are now **hardcoded** in [`server.py`](server.py:51), making deployment much simpler!

**No more need for:**
- ❌ Prefect Secrets
- ❌ Environment variables in Horizon
- ❌ Complex secret management

## 📋 Quick Deploy Steps

### Step 1: Push to GitHub

Make sure your latest changes are pushed:

```bash
cd snowflake-mcp-server
git add .
git commit -m "Hardcode Snowflake credentials for easy deployment"
git push origin main
```

### Step 2: Go to Prefect Horizon

1. Open https://app.prefect.cloud/
2. Click **"MCP Registry"** in left sidebar (under "Operate")
3. Click **"+ Create Server"** or select existing **"mcpsnowflake"**

### Step 3: Configure Server

Fill in these settings:

#### **General**
```
Name: mcpsnowflake
Description: Snowflake MCP Server for IBM ICA
```

#### **Source**
```
Source Type: GitHub
Repository: sandipsingha/mcp_snowflake
Branch: main
Path: snowflake-mcp-server
```

**Note:** If your files are in the repository root (not in a subdirectory), leave "Path" empty.

#### **Build**
```
Entrypoint: server.py
Python Version: 3.12
Dependencies: requirements.txt
```

#### **Environment** (Optional)
```
PORT: 3000
```

**That's it!** No Snowflake credentials needed here since they're hardcoded.

### Step 4: Deploy

1. Click **"Save"** or **"Deploy"**
2. Wait 2-5 minutes for build to complete
3. Server will start automatically

### Step 5: Get Your URL

Once deployed, you'll see:
```
Status: ● Running
URL: https://mcpsnowflake-xxxxx.prefect.cloud
```

**Copy this URL** for IBM ICA Context Studio!

## 🧪 Test Your Deployment

### Test 1: Health Check
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

### Test 2: List Schemas
```bash
curl https://your-server-url.prefect.cloud/mcp/schemas
```

### Test 3: Get Customers
```bash
curl https://your-server-url.prefect.cloud/mcp/customers
```

## 🔄 Update Deployment

When you make code changes:

1. **Push to GitHub:**
   ```bash
   git add .
   git commit -m "Update server"
   git push origin main
   ```

2. **Rebuild in Horizon:**
   - Go to MCP Registry → mcpsnowflake
   - Click **"Rebuild"** button
   - Wait for build to complete

## 📊 Available Endpoints

Once deployed, your server provides these endpoints:

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Health check |
| `/mcp/schemas` | GET | List all schemas |
| `/mcp/tables/{schema}` | GET | List tables in schema |
| `/mcp/query` | POST | Execute custom query |
| `/mcp/customers` | GET | Get all customers |
| `/mcp/tickets` | GET | Get service tickets |
| `/mcp/usage` | GET | Get usage metrics |
| `/mcp/billing` | GET | Get billing history |
| `/mcp/all` | GET | Get all data combined |

## 🔍 Troubleshooting

### Build Fails

**Check build logs:**
- Go to MCP Registry → mcpsnowflake → Build Logs
- Look for specific error messages

**Common issues:**
- Wrong repository path
- Missing Dockerfile
- Syntax errors in requirements.txt

### Server Starts but Crashes

**Check runtime logs:**
- Go to MCP Registry → mcpsnowflake → Logs
- Look for Snowflake connection errors

**Possible causes:**
- Wrong Snowflake credentials (check server.py)
- Network issues
- Snowflake warehouse not running

### Can't Connect to Server

**Verify:**
- Server status is "Running" (green dot)
- URL is correct
- No firewall blocking requests

## 🔐 Security Note

⚠️ **Important:** Credentials are now hardcoded in the source code. This is convenient for demos but **NOT recommended for production**.

**For production, consider:**
- Using environment variables
- Using Prefect Secrets
- Using a secrets management service (AWS Secrets Manager, Azure Key Vault, etc.)

## ✅ Success Checklist

- [ ] Code pushed to GitHub
- [ ] Server created in Horizon
- [ ] Configuration set correctly
- [ ] Build completed successfully
- [ ] Server status shows "Running"
- [ ] Health endpoint returns 200 OK
- [ ] All MCP endpoints working

## 🎉 You're Done!

Your Snowflake MCP Server is now:
- ✅ Running 24/7 on Prefect infrastructure
- ✅ Accessible via public URL
- ✅ Ready to connect to IBM ICA Context Studio
- ✅ No complex secret management needed

**Next:** Use the server URL in IBM ICA Context Studio to connect to your Snowflake data!

## 📞 Need Help?

- **Prefect Docs:** https://docs.prefect.io/
- **Horizon Docs:** https://docs.prefect.io/latest/guides/deployment/horizon/
- **Prefect Slack:** https://prefect.io/slack