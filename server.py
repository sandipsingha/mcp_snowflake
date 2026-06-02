"""
Snowflake MCP Server - Python/Prefect Version
A Prefect-based MCP server for Snowflake data operations
"""

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
import snowflake.connector
from prefect import flow, task
from prefect.blocks.system import Secret
import os
from dotenv import load_dotenv
import logging
from contextlib import contextmanager
import asyncio

# Load environment variables (for local development)
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# FastAPI app
app = FastAPI(
    title="Snowflake MCP Server",
    description="MCP Server for Snowflake connection to IBM ICA Context Studio",
    version="2.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class QueryRequest(BaseModel):
    query: Optional[str] = None
    schema: Optional[str] = None
    table: Optional[str] = None
    limit: int = 100
    offset: int = 0


# Snowflake connection configuration
async def load_secret_async(secret_name: str) -> str:
    """Load a secret asynchronously"""
    secret = await Secret.load(secret_name)
    return secret.get()

def get_snowflake_config() -> Dict[str, str]:
    """Get Snowflake configuration from environment variables or Prefect Secrets"""
    
    # Try to load from Prefect Cloud Secrets first (for deployed flows)
    try:
        logger.info("🔍 Attempting to load credentials from Prefect Cloud Secrets...")
        
        # Run async secret loading in sync context
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            config = {
                'account': loop.run_until_complete(load_secret_async("snowflake-account")),
                'user': loop.run_until_complete(load_secret_async("snowflake-username")),
                'password': loop.run_until_complete(load_secret_async("snowflake-password")),
                'warehouse': loop.run_until_complete(load_secret_async("snowflake-warehouse")),
                'database': loop.run_until_complete(load_secret_async("snowflake-database")),
                'role': loop.run_until_complete(load_secret_async("snowflake-role"))
            }
            logger.info("✅ Successfully loaded credentials from Prefect Cloud Secrets")
            return config
        finally:
            loop.close()
            
    except Exception as e:
        # Fall back to environment variables (for local development)
        logger.info(f"⚠️ Could not load from Prefect Secrets ({str(e)}), falling back to environment variables...")
        config = {
            'account': os.getenv('SNOWFLAKE_ACCOUNT'),
            'user': os.getenv('SNOWFLAKE_USERNAME'),
            'password': os.getenv('SNOWFLAKE_PASSWORD'),
            'warehouse': os.getenv('SNOWFLAKE_WAREHOUSE'),
            'database': os.getenv('SNOWFLAKE_DATABASE'),
            'role': os.getenv('SNOWFLAKE_ROLE')
        }
        
        # Validate that we have credentials
        if not all(config.values()):
            missing = [k for k, v in config.items() if not v]
            raise ValueError(f"❌ Missing Snowflake credentials: {', '.join(missing)}")
        
        logger.info("✅ Successfully loaded credentials from environment variables")
        return config


@contextmanager
def get_snowflake_connection():
    """Context manager for Snowflake connections"""
    config = get_snowflake_config()
    conn = None
    try:
        conn = snowflake.connector.connect(**config)
        logger.info(f"✅ Connected to Snowflake: {config['database']}")
        yield conn
    except Exception as e:
        logger.error(f"❌ Snowflake connection error: {str(e)}")
        raise
    finally:
        if conn:
            conn.close()
            logger.info("🔒 Snowflake connection closed")


@task(name="execute_snowflake_query", retries=2, retry_delay_seconds=5)
def execute_query_task(sql_text: str) -> List[Dict[str, Any]]:
    """Prefect task to execute Snowflake query"""
    with get_snowflake_connection() as conn:
        cursor = conn.cursor(snowflake.connector.DictCursor)
        try:
            cursor.execute(sql_text)
            results = cursor.fetchall()
            logger.info(f"✅ Query executed successfully: {len(results)} rows")
            return results
        except Exception as e:
            logger.error(f"❌ Query execution error: {str(e)}")
            raise
        finally:
            cursor.close()


@flow(name="get_schemas_flow")
def get_schemas_flow() -> List[str]:
    """Prefect flow to get all schemas"""
    config = get_snowflake_config()
    sql = f"SHOW SCHEMAS IN DATABASE {config['database']}"
    results = execute_query_task(sql)
    return [row['name'] for row in results]


@flow(name="get_tables_flow")
def get_tables_flow(schema: str) -> List[str]:
    """Prefect flow to get tables in a schema"""
    sql = f"SHOW TABLES IN SCHEMA {schema}"
    results = execute_query_task(sql)
    return [row['name'] for row in results]


@flow(name="query_data_flow")
def query_data_flow(sql_text: str) -> List[Dict[str, Any]]:
    """Prefect flow to execute custom query"""
    return execute_query_task(sql_text)


@flow(name="get_customers_flow")
def get_customers_flow() -> List[Dict[str, Any]]:
    """Prefect flow to get all customers"""
    sql = "SELECT * FROM CUSTOMER_DATA.CUSTOMERS"
    return execute_query_task(sql)


@flow(name="get_tickets_flow")
def get_tickets_flow() -> List[Dict[str, Any]]:
    """Prefect flow to get all service tickets"""
    sql = "SELECT * FROM SERVICE_DATA.SERVICE_TICKETS"
    return execute_query_task(sql)


@flow(name="get_usage_flow")
def get_usage_flow() -> List[Dict[str, Any]]:
    """Prefect flow to get all usage metrics"""
    sql = "SELECT * FROM USAGE_DATA.USAGE_METRICS"
    return execute_query_task(sql)


@flow(name="get_billing_flow")
def get_billing_flow() -> List[Dict[str, Any]]:
    """Prefect flow to get all billing history"""
    sql = "SELECT * FROM BILLING_DATA.BILLING_HISTORY"
    return execute_query_task(sql)


@flow(name="get_all_data_flow")
def get_all_data_flow() -> Dict[str, Any]:
    """Prefect flow to get all data combined"""
    customers = get_customers_flow()
    tickets = get_tickets_flow()
    usage = get_usage_flow()
    billing = get_billing_flow()
    
    return {
        'customers': customers,
        'tickets': tickets,
        'usage': usage,
        'billing': billing
    }


# FastAPI endpoints
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    config = get_snowflake_config()
    return {
        "status": "healthy",
        "database": config['database'],
        "warehouse": config['warehouse'],
        "version": "2.0.0",
        "framework": "FastAPI + Prefect"
    }


@app.get("/mcp/schemas")
async def list_schemas():
    """List all schemas"""
    try:
        schemas = get_schemas_flow()
        return {
            "success": True,
            "schemas": schemas,
            "count": len(schemas)
        }
    except Exception as e:
        logger.error(f"Error listing schemas: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/mcp/tables/{schema}")
async def list_tables(schema: str):
    """List tables in a schema"""
    try:
        tables = get_tables_flow(schema)
        return {
            "success": True,
            "schema": schema,
            "tables": tables,
            "count": len(tables)
        }
    except Exception as e:
        logger.error(f"Error listing tables: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/mcp/query")
async def execute_query(request: QueryRequest):
    """Execute custom query or query specific table"""
    try:
        if request.query:
            sql_text = request.query
        elif request.schema and request.table:
            sql_text = f"SELECT * FROM {request.schema}.{request.table} LIMIT {request.limit} OFFSET {request.offset}"
        else:
            raise HTTPException(
                status_code=400,
                detail="Either provide a custom query or specify schema and table"
            )
        
        logger.info(f"Executing query: {sql_text}")
        results = query_data_flow(sql_text)
        
        return {
            "success": True,
            "data": results,
            "count": len(results),
            "query": sql_text
        }
    except Exception as e:
        logger.error(f"Error executing query: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/mcp/customers")
async def get_customers():
    """Get all customers"""
    try:
        results = get_customers_flow()
        return {
            "success": True,
            "data": results,
            "count": len(results)
        }
    except Exception as e:
        logger.error(f"Error fetching customers: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/mcp/tickets")
async def get_tickets():
    """Get all service tickets"""
    try:
        results = get_tickets_flow()
        return {
            "success": True,
            "data": results,
            "count": len(results)
        }
    except Exception as e:
        logger.error(f"Error fetching tickets: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/mcp/usage")
async def get_usage():
    """Get all usage metrics"""
    try:
        results = get_usage_flow()
        return {
            "success": True,
            "data": results,
            "count": len(results)
        }
    except Exception as e:
        logger.error(f"Error fetching usage: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/mcp/billing")
async def get_billing():
    """Get all billing history"""
    try:
        results = get_billing_flow()
        return {
            "success": True,
            "data": results,
            "count": len(results)
        }
    except Exception as e:
        logger.error(f"Error fetching billing: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/mcp/all")
async def get_all_data():
    """Get all data combined"""
    try:
        data = get_all_data_flow()
        return {
            "success": True,
            "data": data,
            "counts": {
                "customers": len(data['customers']),
                "tickets": len(data['tickets']),
                "usage": len(data['usage']),
                "billing": len(data['billing'])
            }
        }
    except Exception as e:
        logger.error(f"Error fetching all data: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 3000))
    
    print("\n" + "="*60)
    print("🚀 Snowflake MCP Server (Python/Prefect) is starting!")
    print("="*60)
    print(f"\n   Local:    http://localhost:{port}")
    print(f"   Health:   http://localhost:{port}/health")
    print(f"   Schemas:  http://localhost:{port}/mcp/schemas")
    print("\n📊 Available endpoints:")
    print("   GET  /health              - Health check")
    print("   GET  /mcp/schemas         - List all schemas")
    print("   GET  /mcp/tables/:schema  - List tables in schema")
    print("   POST /mcp/query           - Execute custom query")
    print("   GET  /mcp/customers       - Get all customers")
    print("   GET  /mcp/tickets         - Get all service tickets")
    print("   GET  /mcp/usage           - Get all usage metrics")
    print("   GET  /mcp/billing         - Get all billing history")
    print("   GET  /mcp/all             - Get all data combined")
    print("\n" + "="*60 + "\n")
    
    uvicorn.run(app, host="0.0.0.0", port=port)

# Made with Bob
