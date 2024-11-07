import re
import time
from azure.identity import DefaultAzureCredential
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.resourcegraph import ResourceGraphClient
from azure.mgmt.resourcegraph.models import QueryRequest
from tabulate import tabulate
from tqdm import tqdm

def get_reserved_instances(subscription_id):
    credential = DefaultAzureCredential()
    resource_graph_client = ResourceGraphClient(credential)

    query = "Resources | where type =~ 'Microsoft.Compute/reservations'"
    request = QueryRequest(subscriptions=[subscription_id], query=query)
    response = resource_graph_client.resources(request)

    reserved_instances = set()
    for resource in response.data:
        reserved_instances.add(resource['name'])
    
    return reserved_instances

def list_vm_skus(region, pattern):
    start_time = time.time()
    
    credential = DefaultAzureCredential()
    subscription_id = 'cb3f71fd-4926-40fa-b99e-06449084f4aa'  # Replace with your subscription ID
    compute_client = ComputeManagementClient(credential, subscription_id)

    reserved_instances = get_reserved_instances(subscription_id)
    
    skus = compute_client.resource_skus.list()
    table = []
    for sku in tqdm(skus, desc="Loading SKUs"):
        if sku.locations and region in sku.locations:
            if pattern == "all" or re.search(pattern, sku.name, re.IGNORECASE):
                zones = sku.location_info[0].zones if sku.location_info else []
                sku_pressure = sku.resource_type  # Placeholder for actual SKU pressure calculation
                sku_quota = next((capability.value for capability in sku.capabilities if capability.name == 'MaxResourceCount'), 'Unknown') if sku.capabilities else 'Unknown'
                allowed = 'Yes' if not sku.restrictions else 'No'
                reserved = 'Yes' if sku.name in reserved_instances else 'No'
                table.append([sku.name, ', '.join(zones) if zones else 'None', sku_pressure, sku_quota, allowed, reserved])
    
    headers = ["SKU", "Zones", "Resource Type", "Quota", "Allowed", "Reserved"]
    print(tabulate(table, headers, tablefmt="grid"))
    
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Time taken: {elapsed_time:.2f} seconds")

if __name__ == "__main__":
    region = input("Enter the region: ")
    pattern = input("Enter SKU pattern (or 'all' to list all SKUs): ")
    list_vm_skus(region, pattern)