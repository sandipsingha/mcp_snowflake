"""
Setup Prefect Cloud Secrets for Snowflake Credentials
Run this to store your Snowflake credentials securely in Prefect Cloud
"""

import asyncio
from prefect.blocks.system import Secret
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()


async def create_secret(name: str, value: str):
    """Create or update a Prefect secret"""
    try:
        secret = Secret(value=value)
        await secret.save(name=name, overwrite=True)
        print(f"✅ Created secret: {name}")
        return True
    except Exception as e:
        print(f"❌ Error creating {name}: {str(e)}")
        return False


async def setup_all_secrets():
    """Setup all Snowflake secrets in Prefect Cloud"""
    print("\n" + "="*60)
    print("Setting up Snowflake Secrets in Prefect Cloud")
    print("="*60 + "\n")
    
    # Get credentials from .env file
    secrets = {
        "snowflake-account": os.getenv("SNOWFLAKE_ACCOUNT"),
        "snowflake-username": os.getenv("SNOWFLAKE_USERNAME"),
        "snowflake-password": os.getenv("SNOWFLAKE_PASSWORD"),
        "snowflake-warehouse": os.getenv("SNOWFLAKE_WAREHOUSE"),
        "snowflake-database": os.getenv("SNOWFLAKE_DATABASE"),
        "snowflake-role": os.getenv("SNOWFLAKE_ROLE"),
    }
    
    # Check if all values are present
    missing = [name for name, value in secrets.items() if not value]
    if missing:
        print("❌ Missing environment variables in .env file:")
        for name in missing:
            print(f"   - {name.upper().replace('-', '_')}")
        print("\nPlease update your .env file with all Snowflake credentials.")
        return False
    
    # Create all secrets
    print("Creating secrets in Prefect Cloud...\n")
    success_count = 0
    for name, value in secrets.items():
        if await create_secret(name, value):
            success_count += 1
    
    print("\n" + "="*60)
    if success_count == len(secrets):
        print("✅ All secrets created successfully!")
        print("="*60)
        print("\nYour Prefect Cloud flows can now access Snowflake!")
        print("Try running a flow from: https://app.prefect.cloud/")
        return True
    else:
        print(f"⚠️  Created {success_count}/{len(secrets)} secrets")
        print("="*60)
        return False


async def list_secrets():
    """List all existing secrets"""
    print("\n" + "="*60)
    print("Existing Prefect Secrets")
    print("="*60 + "\n")
    
    try:
        # Try to load each secret to see if it exists
        secret_names = [
            "snowflake-account",
            "snowflake-username", 
            "snowflake-password",
            "snowflake-warehouse",
            "snowflake-database",
            "snowflake-role"
        ]
        
        for name in secret_names:
            try:
                secret = await Secret.load(name)
                print(f"✅ {name}: exists")
            except:
                print(f"❌ {name}: not found")
                
    except Exception as e:
        print(f"Error listing secrets: {str(e)}")


async def main():
    """Main function"""
    print("\n" + "="*60)
    print("Prefect Cloud Secrets Manager")
    print("="*60)
    
    while True:
        print("\nOptions:")
        print("1. Setup all Snowflake secrets from .env file")
        print("2. List existing secrets")
        print("3. Exit")
        
        choice = input("\nEnter your choice (1-3): ").strip()
        
        if choice == "1":
            await setup_all_secrets()
        elif choice == "2":
            await list_secrets()
        elif choice == "3":
            print("\n👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please enter 1, 2, or 3.")


if __name__ == "__main__":
    asyncio.run(main())

# Made with Bob
