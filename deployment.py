"""
Deploy Snowflake MCP flows to Prefect Cloud
"""

from prefect import serve
from flows import (
    get_customers_flow,
    get_schemas_flow,
    get_tables_flow,
    query_data_flow,
    get_all_data_flow
)

if __name__ == "__main__":
    print("=" * 60)
    print("Deploying 5 Snowflake MCP Flows to Prefect Cloud")
    print("=" * 60)
    print()
    
    # Deploy flows with serve()
    serve(
        get_schemas_flow.to_deployment(name="get-schemas"),
        get_tables_flow.to_deployment(name="get-tables"),
        query_data_flow.to_deployment(name="query-data"),
        get_customers_flow.to_deployment(name="get-customers"),
        get_all_data_flow.to_deployment(name="get-all-data"),
    )

# Made with Bob
