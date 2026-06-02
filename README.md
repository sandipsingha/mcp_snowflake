# Snowflake MCP Server - Python/Prefect Version

A Python-based MCP server using FastAPI and Prefect for Snowflake data operations, deployable to Prefect Cloud.

## 🚀 Quick Start (Local Development)

### Step 1: Install Python Dependencies

```bash
cd snowflake-mcp-server
pip install -r requirements.txt
```

### Step 2: Configure Environment

Copy the example environment file:

```bash
cp .env.python.example .env
```

Edit `.env` with your Snowflake credentials:

```env
SNOWFLAKE_ACCOUNT=your-account-identifier
SNOWFLAKE_USERNAME=your-username
SNOWFLAKE_PASSWORD=your-password
SNOWFLAKE_WAREHOUSE=COMPUTE_WH
SNOWFLAKE_DATABASE=TELECOM_ANALYTICS
SNOWFLAKE_ROLE=your-role
PORT=3000
```

### Step 3: Run the Server Locally

```bash
python server.py
```

You should see:

```
🚀 Snowflake MCP Server (Python/Prefect) is starting!
   Local:    http://localhost:3000
   Health:   http://localhost:3000/health
```

### Step 4: Test the Server

```bash
# Test health check
curl http://localhost:3000/health

# Test schemas
curl http://localhost:3000/mcp/schemas

# Test customers data
curl http://localhost:3000/mcp/customers
```

---

## ☁️ Deploy to Prefect Cloud

### Prerequisites

1. **Prefect Cloud Account**: Sign up at https://app.prefect.cloud/
2. **Prefect CLI**: Already included in requirements.txt
3. **API Key**: Get from Prefect Cloud settings

### Step 1: Authenticate with Prefect Cloud

```bash
# Login to Prefect Cloud
prefect cloud login

# Or set API key directly
prefect config set PREFECT_API_KEY=your-api-key
prefect config set PREFECT_API_URL=https://api.prefect.cloud/api/accounts/[ACCOUNT_ID]/workspaces/[WORKSPACE_ID]
```

### Step 2: Create Prefect Blocks for Secrets

Store your Snowflake credentials as Prefect Secret blocks:

```bash
# Create secrets in Prefect Cloud
prefect block register -m prefect.blocks.system

# Create each secret (you can also do this via Prefect Cloud UI)
python -c "
from prefect.blocks.system import Secret

Secret(value='your-account-identifier').save('snowflake-account')
Secret(value='your-username').save('snowflake-username')
Secret(value='your-password').save('snowflake-password')
Secret(value='COMPUTE_WH').save('snowflake-warehouse')
Secret(value='TELECOM_ANALYTICS').save('snowflake-database')
Secret(value='your-role').save('snowflake-role')
"
```

**OR** create secrets via Prefect Cloud UI:
1. Go to https://app.prefect.cloud/
2. Navigate to **Blocks** → **+** → **Secret**
3. Create blocks named:
   - `snowflake-account`
   - `snowflake-username`
   - `snowflake-password`
   - `snowflake-warehouse`
   - `snowflake-database`
   - `snowflake-role`

### Step 3: Deploy Flows to Prefect Cloud

```bash
# Deploy all flows
python deployment.py
```

This will deploy all Prefect flows to your Prefect Cloud workspace.

### Step 4: Start a Prefect Agent

You need an agent running to execute the flows:

```bash
# Start an agent (keep this running)
prefect agent start -q default
```

**For production**, run the agent as a service or in a container.

### Step 5: Run Flows from Prefect Cloud

Now you can trigger flows from:
- **Prefect Cloud UI**: https://app.prefect.cloud/
- **API calls**: Use Prefect's REST API
- **Scheduled runs**: Configure in prefect.yaml

---

## 🌐 Alternative: Deploy as Web Service

If you want to deploy the FastAPI server (not just Prefect flows), use these platforms:

### Option 1: Railway

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login and deploy
railway login
railway init
railway up
```

Add environment variables in Railway dashboard.

### Option 2: Render

1. Create a new **Web Service** on https://render.com/
2. Connect your GitHub repository
3. Set build command: `pip install -r requirements.txt`
4. Set start command: `python server.py`
5. Add environment variables in Render dashboard

### Option 3: Google Cloud Run

```bash
# Build and deploy
gcloud run deploy snowflake-mcp-server \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

### Option 4: AWS App Runner

1. Create a Dockerfile:

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 3000
CMD ["python", "server.py"]
```

2. Deploy via AWS App Runner console

---

## 📋 Available Endpoints

### Health Check
```
GET /health
```

### List Schemas
```
GET /mcp/schemas
```

### List Tables
```
GET /mcp/tables/{schema}
```

### Execute Query
```
POST /mcp/query
Content-Type: application/json

{
  "query": "SELECT * FROM CUSTOMER_DATA.CUSTOMERS LIMIT 10"
}
```

### Get Customers
```
GET /mcp/customers
```

### Get Service Tickets
```
GET /mcp/tickets
```

### Get Usage Metrics
```
GET /mcp/usage
```

### Get Billing History
```
GET /mcp/billing
```

### Get All Data
```
GET /mcp/all
```

---

## 🔧 Prefect Flow Management

### View Flows

```bash
# List all flows
prefect flow ls

# View flow runs
prefect flow-run ls
```

### Trigger a Flow Manually

```bash
# Run a specific flow
prefect deployment run 'get-customers-flow/get-customers'
```

### Monitor Flows

Visit your Prefect Cloud dashboard:
- **Flow Runs**: See all executions
- **Logs**: View detailed logs
- **Metrics**: Monitor performance

---

## 🔒 Security Best Practices

### For Production:

1. **Use Prefect Secret Blocks**: Never hardcode credentials
2. **Enable HTTPS**: Use reverse proxy (nginx, Caddy)
3. **Add Authentication**: Implement API keys or OAuth
4. **Rate Limiting**: Add rate limiting middleware
5. **IP Whitelisting**: Restrict access to known IPs
6. **Rotate Credentials**: Change passwords regularly

### Example: Add API Key Authentication

```python
# Add to server.py
from fastapi import Header, HTTPException

API_KEY = os.getenv("API_KEY")

async def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")
    return x_api_key

# Add to endpoints
@app.get("/mcp/customers", dependencies=[Depends(verify_api_key)])
async def get_customers():
    ...
```

---

## 🐛 Troubleshooting

### Error: "Import prefect could not be resolved"

**Solution**: Install dependencies
```bash
pip install -r requirements.txt
```

### Error: "Unable to connect to Snowflake"

**Solution**: Check credentials and network
```bash
# Test Snowflake connection
python -c "
import snowflake.connector
conn = snowflake.connector.connect(
    account='your-account',
    user='your-user',
    password='your-password'
)
print('✅ Connected!')
"
```

### Error: "Prefect API authentication failed"

**Solution**: Re-authenticate
```bash
prefect cloud login
```

### Error: "No agent available"

**Solution**: Start a Prefect agent
```bash
prefect agent start -q default
```

---

## 📊 Differences from Node.js Version

| Feature | Node.js Version | Python Version |
|---------|----------------|----------------|
| Framework | Express | FastAPI |
| Orchestration | None | Prefect |
| Deployment | Manual | Prefect Cloud |
| Type Safety | JavaScript | Python + Pydantic |
| Async Support | Callbacks | async/await |
| Monitoring | Manual | Prefect Dashboard |

---

## 🎯 Next Steps

1. **Deploy to Prefect Cloud**: Follow deployment steps above
2. **Set up monitoring**: Use Prefect Cloud dashboard
3. **Configure schedules**: Edit prefect.yaml for automated runs
4. **Add more flows**: Create custom Prefect flows for your use case
5. **Integrate with ICA**: Connect to IBM ICA Context Studio

---

## 📝 Files Overview

- **`server.py`**: Main FastAPI application with Prefect flows
- **`requirements.txt`**: Python dependencies
- **`deployment.py`**: Prefect deployment script
- **`prefect.yaml`**: Prefect configuration
- **`.env.python.example`**: Environment variables template
- **`README_PYTHON.md`**: This file

---

## 🆘 Support

For issues:
1. Check Prefect Cloud logs
2. Review server logs: `python server.py`
3. Test Snowflake connection
4. Verify environment variables

---

**Version:** 2.0.0 (Python/Prefect)  
**Last Updated:** 2026-06-02  
**Framework:** FastAPI + Prefect  
**Deployment Target:** Prefect Cloud