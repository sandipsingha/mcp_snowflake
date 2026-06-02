"""
Simplified Prefect flows for Snowflake MCP Server
Designed to run in Prefect Cloud with minimal dependencies
"""

from prefect import flow, task
from prefect.blocks.system import Secret
import snowflake.connector
from typing import List, Dict, Any
import logging
import asyncio

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@task(name="get_snowflake_credentials", retries=2)
def get_snowflake_credentials() -> Dict[str, str]:
    """Get Snowflake credentials from Prefect Secrets"""
    logger.info("🔍 Loading Snowflake credentials from Prefect Cloud Secrets...")
    
    try:
        # Secret.load() is synchronous, not async
        credentials = {
            'account': Secret.load("snowflake-account").get(),
            'user': Secret.load("snowflake-username").get(),
            'password': Secret.load("snowflake-password").get(),
            'warehouse': Secret.load("snowflake-warehouse").get(),
            'database': Secret.load("snowflake-database").get(),
            'role': Secret.load("snowflake-role").get()
        }
        logger.info("✅ Successfully loaded all Snowflake credentials")
        return credentials
            
    except Exception as e:
        logger.error(f"❌ Failed to load credentials: {e}")
        raise


@task(name="execute_snowflake_query", retries=2, retry_delay_seconds=5)
def execute_query(credentials: Dict[str, str], sql: str) -> List[Dict[str, Any]]:
    """Execute a Snowflake query"""
    conn = None
    try:
        logger.info(f"🔌 Connecting to Snowflake database: {credentials['database']}")
        conn = snowflake.connector.connect(**credentials)
        
        cursor = conn.cursor(snowflake.connector.DictCursor)
        logger.info(f"📊 Executing query: {sql[:100]}...")
        cursor.execute(sql)
        results = cursor.fetchall()
        
        logger.info(f"✅ Query successful: {len(results)} rows returned")
        cursor.close()
        return results
        
    except Exception as e:
        logger.error(f"❌ Query failed: {e}")
        raise
    finally:
        if conn:
            conn.close()
            logger.info("🔒 Connection closed")


@flow(name="get_customers_flow", log_prints=True)
def get_customers_flow():
    """Get all customers from Snowflake"""
    logger.info("🚀 Starting get_customers_flow")
    
    credentials = get_snowflake_credentials()
    sql = "SELECT * FROM CUSTOMER_DATA.CUSTOMERS LIMIT 100"
    results = execute_query(credentials, sql)
    
    logger.info(f"✅ Retrieved {len(results)} customers")
    return results


@flow(name="get_schemas_flow", log_prints=True)
def get_schemas_flow():
    """Get all schemas from Snowflake"""
    logger.info("🚀 Starting get_schemas_flow")
    
    credentials = get_snowflake_credentials()
    sql = f"SHOW SCHEMAS IN DATABASE {credentials['database']}"
    results = execute_query(credentials, sql)
    
    schemas = [row['name'] for row in results]
    logger.info(f"✅ Found {len(schemas)} schemas")
    return schemas


@flow(name="get_tables_flow", log_prints=True)
def get_tables_flow(schema_name: str = "CUSTOMER_DATA"):
    """Get tables in a schema"""
    logger.info(f"🚀 Starting get_tables_flow for schema: {schema_name}")
    
    credentials = get_snowflake_credentials()
    sql = f"SHOW TABLES IN SCHEMA {schema_name}"
    results = execute_query(credentials, sql)
    
    tables = [row['name'] for row in results]
    logger.info(f"✅ Found {len(tables)} tables in {schema_name}")
    return tables


@flow(name="query_data_flow", log_prints=True)
def query_data_flow(sql: str):
    """Execute custom SQL query"""
    logger.info(f"🚀 Starting query_data_flow")
    
    credentials = get_snowflake_credentials()
    results = execute_query(credentials, sql)
    
    logger.info(f"✅ Query returned {len(results)} rows")
    return results


@flow(name="get_all_data_flow", log_prints=True)
def get_all_data_flow():
    """Get all data from multiple tables"""
    logger.info("🚀 Starting get_all_data_flow")
    
    credentials = get_snowflake_credentials()
    
    # Get customers
    customers = execute_query(credentials, "SELECT * FROM CUSTOMER_DATA.CUSTOMERS LIMIT 50")
    logger.info(f"✅ Retrieved {len(customers)} customers")
    
    # Get tickets
    tickets = execute_query(credentials, "SELECT * FROM SERVICE_DATA.SERVICE_TICKETS LIMIT 50")
    logger.info(f"✅ Retrieved {len(tickets)} tickets")
    
    return {
        'customers': customers,
        'tickets': tickets,
        'total_records': len(customers) + len(tickets)
    }


if __name__ == "__main__":
    # Test locally
    print("Testing flows locally...")
    get_customers_flow()

# Made with Bob
