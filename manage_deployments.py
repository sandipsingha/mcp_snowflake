"""
Script to manage Prefect Cloud deployments
Lists and optionally deletes deployments
"""

import asyncio
from prefect.client.orchestration import get_client


async def list_deployments():
    """List all deployments in the workspace"""
    async with get_client() as client:
        deployments = await client.read_deployments()
        
        if not deployments:
            print("✅ No deployments found in your workspace!")
            return []
        
        print(f"\n📋 Found {len(deployments)} deployment(s):\n")
        for i, deployment in enumerate(deployments, 1):
            print(f"{i}. Name: {deployment.name}")
            print(f"   ID: {deployment.id}")
            print(f"   Flow: {deployment.flow_id}")
            print(f"   Created: {deployment.created}")
            print()
        
        return deployments


async def delete_deployment(deployment_id: str, deployment_name: str):
    """Delete a specific deployment"""
    async with get_client() as client:
        try:
            await client.delete_deployment(deployment_id)
            print(f"✅ Deleted deployment: {deployment_name}")
            return True
        except Exception as e:
            print(f"❌ Error deleting {deployment_name}: {str(e)}")
            return False


async def delete_all_deployments():
    """Delete all deployments"""
    deployments = await list_deployments()
    
    if not deployments:
        return
    
    print("\n⚠️  This will delete ALL deployments!")
    confirm = input("Type 'yes' to confirm: ")
    
    if confirm.lower() != 'yes':
        print("❌ Cancelled")
        return
    
    print("\n🗑️  Deleting deployments...\n")
    for deployment in deployments:
        await delete_deployment(deployment.id, deployment.name)
    
    print("\n✅ All deployments deleted!")


async def main():
    """Main function"""
    print("=" * 60)
    print("Prefect Cloud Deployment Manager")
    print("=" * 60)
    
    while True:
        print("\nOptions:")
        print("1. List all deployments")
        print("2. Delete all deployments")
        print("3. Exit")
        
        choice = input("\nEnter your choice (1-3): ").strip()
        
        if choice == "1":
            await list_deployments()
        elif choice == "2":
            await delete_all_deployments()
        elif choice == "3":
            print("\n👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please enter 1, 2, or 3.")


if __name__ == "__main__":
    asyncio.run(main())

# Made with Bob
