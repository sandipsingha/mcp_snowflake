"""
Test script to verify Prefect Cloud Secrets are accessible
"""
import asyncio
from prefect.blocks.system import Secret

async def test_secrets():
    """Test loading secrets from Prefect Cloud"""
    secrets_to_test = [
        "snowflake-account",
        "snowflake-username", 
        "snowflake-password",
        "snowflake-warehouse",
        "snowflake-database",
        "snowflake-role"
    ]
    
    print("=" * 60)
    print("Testing Prefect Cloud Secrets")
    print("=" * 60)
    
    for secret_name in secrets_to_test:
        try:
            secret = await Secret.load(secret_name)
            value = secret.get()
            # Show first 3 chars only for security
            masked_value = value[:3] + "..." if len(value) > 3 else "***"
            print(f"✅ {secret_name}: {masked_value}")
        except Exception as e:
            print(f"❌ {secret_name}: {str(e)}")
    
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(test_secrets())

# Made with Bob
