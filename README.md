# check-aks-sku-available
How can i check the SKU in a given AZ where my AKS cluster is running for example?
- This code looks at a region allows you to enter a letter for the SKU needed for example: NV. 

![image](https://github.com/user-attachments/assets/d89da4c4-f373-4813-9ab9-7cf34d772027)


If you need to check availability in specific availability zones within a region, you can filter the SKUs based on the zones they support. Here's an updated version of your script to include zone information:

```python


import re
from azure.identity import DefaultAzureCredential
from azure.mgmt.compute import ComputeManagementClient
from tabulate import tabulate

def list_vm_skus(region, pattern):
    credential = DefaultAzureCredential()
    subscription_id = 'INSERT-SUBID-HERE'  # Replace with your subscription ID
    compute_client = ComputeManagementClient(credential, subscription_id)

    skus = compute_client.resource_skus.list()
    table = []
    for sku in skus:
        if sku.locations and region in sku.locations:
            if pattern == "all" or re.search(pattern, sku.name, re.IGNORECASE):
                zones = sku.location_info[0].zones if sku.location_info else []
                # Assuming SKU pressure and quota can be derived from some properties of the SKU
                # Replace these with actual properties or calculations as needed
                sku_pressure = sku.resource_type  # Placeholder for actual SKU pressure calculation
                sku_quota = sku.capabilities[0].value if sku.capabilities else 'Unknown'  # Placeholder for actual quota
                table.append([sku.name, ', '.join(zones) if zones else 'None', sku_pressure, sku_quota])
    
    headers = ["SKU", "Zones", "Resource Type", "Quota"]
    print(tabulate(table, headers, tablefmt="grid"))

if __name__ == "__main__":
    region = input("Enter the region: ")
    pattern = input("Enter SKU pattern (or 'all' to list all SKUs): ")
    list_vm_skus(region, pattern)

```

```python
pip install azure-identity azure-mgmt-containerservice azure-mgmt-compute
```

TO-DO
1) calculate pressure
2) Check Quota if its allowed or not
