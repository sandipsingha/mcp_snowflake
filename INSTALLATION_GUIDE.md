# Installation Guide - Python MCP Server

## ⚠️ Important: Python Version Requirement

**The Snowflake connector requires Python 3.11 or earlier** due to compilation requirements on Windows.

Python 3.13 is too new and doesn't have pre-built wheels for:
- `snowflake-connector-python`
- `pydantic-core`

## 🔧 Solution Options

### Option 1: Use Python 3.11 (Recommended)

1. **Download Python 3.11**:
   - Visit: https://www.python.org/downloads/
   - Download Python 3.11.x (latest 3.11 version)
   - Install it

2. **Create a virtual environment with Python 3.11**:
   ```bash
   # Navigate to project directory
   cd snowflake-mcp-server
   
   # Create virtual environment with Python 3.11
   py -3.11 -m venv venv
   
   # Activate it
   .\venv\Scripts\activate
   
   # Install dependencies
   pip install -r requirements.txt
   ```

3. **Run the server**:
   ```bash
   python server.py
   ```

### Option 2: Install Visual Studio Build Tools (For Python 3.13)

If you want to continue using Python 3.13:

1. **Download Visual Studio Build Tools**:
   - Visit: https://visualstudio.microsoft.com/visual-cpp-build-tools/
   - Download "Build Tools for Visual Studio 2022"

2. **Install with C++ components**:
   - Run the installer
   - Select "Desktop development with C++"
   - Install (requires ~7GB)

3. **Restart terminal and try again**:
   ```bash
   pip install -r requirements.txt
   ```

### Option 3: Use Docker (No compilation needed)

Create a `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Expose port
EXPOSE 3000

# Run server
CMD ["python", "server.py"]
```

Build and run:
```bash
docker build -t snowflake-mcp-server .
docker run -p 3000:3000 --env-file .env snowflake-mcp-server
```

### Option 4: Deploy to Cloud (Easiest)

Deploy directly to a cloud platform that handles dependencies:

#### Railway:
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login and deploy
railway login
railway init
railway up
```

#### Render:
1. Go to https://render.com/
2. Create new Web Service
3. Connect your GitHub repo
4. Set:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python server.py`
5. Add environment variables
6. Deploy

## 📋 Verification

After successful installation, test:

```bash
# Start server
python server.py

# In another terminal, test
curl http://localhost:3000/health
```

You should see:
```json
{
  "status": "healthy",
  "database": "TELECOM_ANALYTICS",
  "warehouse": "COMPUTE_WH",
  "version": "2.0.0",
  "framework": "FastAPI + Prefect"
}
```

## 🆘 Still Having Issues?

If you continue to face issues:

1. **Check Python version**:
   ```bash
   python --version
   ```
   Should show Python 3.11.x

2. **Use virtual environment**:
   Always use a virtual environment to avoid conflicts

3. **Clear pip cache**:
   ```bash
   pip cache purge
   pip install -r requirements.txt
   ```

4. **Contact support** with:
   - Python version
   - Operating system
   - Full error message