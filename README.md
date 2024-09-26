# check-aks-sku-available
How can i check the SKU in a given AZ where my cluster is running


The ResourceSkus API provides information about the available SKUs for a given subscription and location.

The provided script already uses the ComputeManagementClient to list available SKUs in a specified location. This is the correct approach to query available SKUs for consumption in a given region.

If you need to check availability in specific availability zones within a region, you can filter the SKUs based on the zones they support. Here's an updated version of your script to include zone information:

```python


import os
from azure.identity import DefaultAzureCredential
from azure.mgmt.containerservice import ContainerServiceClient
from azure.mgmt.compute import ComputeManagementClient

# Set up Azure credentials
credential = DefaultAzureCredential()
subscription_id = os.environ["AZURE_SUBSCRIPTION_ID"]

# Initialize clients
container_service_client = ContainerServiceClient(credential, subscription_id)
compute_client = ComputeManagementClient(credential, subscription_id)

def get_aks_cluster_location(resource_group_name, cluster_name):
    cluster = container_service_client.managed_clusters.get(resource_group_name, cluster_name)
    return cluster.location

def get_available_skus(location):
    skus = compute_client.resource_skus.list()
    available_skus = [sku for sku in skus if location in [loc.location for loc in sku.locations]]
    return available_skus

def main(resource_group_name, cluster_name):
    location = get_aks_cluster_location(resource_group_name, cluster_name)
    available_skus = get_available_skus(location)
    
    for sku in available_skus:
        zones = sku.location_info[0].zones if sku.location_info else []
        print(f"SKU: {sku.name}, Resource Type: {sku.resource_type}, Locations: {sku.locations}, Zones: {zones}")

if __name__ == "__main__":
    resource_group_name = "your_resource_group_name"
    cluster_name = "your_cluster_name"
    main(resource_group_name, cluster_name)

```

Explanation:
Zones Information: The script now includes zone information by accessing sku.location_info[0].zones.
Print Zones: The print statement includes the zones where the SKU is available.
Prerequisites:
Ensure you have the required Azure SDK packages installed:
```python
pip install azure-identity azure-mgmt-containerservice azure-mgmt-compute
```
Set the AZURE_SUBSCRIPTION_ID environment variable with your Azure subscription ID.
