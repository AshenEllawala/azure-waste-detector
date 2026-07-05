import requests
import os
from dotenv import load_dotenv

load_dotenv()

def send_waste_alert(finding, cost):
    url = os.environ.get("LOGIC_APP_WASTE_URL")
    
    payload = {
        "owner": finding.get("owner", "unknown"),
        "resource_name": finding.get("name", "unknown"),
        "resource_type": finding.get("type", "unknown"),
        "environment": finding.get("environment", "unknown"),
        "location": finding.get("location", "unknown"),
        "monthly_cost": cost
    }
    owner = payload['owner']
    if '@' not in owner:
        print(f"Skipping {finding['name']} - owner '{owner}' is not a valid email")
        return
    
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 202:
            print(f"Alert sent to {payload['owner']} for {payload['resource_name']}")
        else:
            print(f"Alert failed for {payload['resource_name']}: {response.status_code}")
    except Exception as e:
        print(f"Error sending alert: {e}")


def send_vm_alert(finding, cost):
    url = os.environ.get("LOGIC_APP_VM_URL")
    
    if not url:
        print("LOGIC_APP_VM_URL not configured")
        return
    
    owner = finding.get('owner', 'unknown')
    if '@' not in owner:
        print(f"Skipping VM alert for {finding['name']} - owner not a valid email")
        return
    
    payload = {
        "owner": owner,
        "resource_name": finding.get("name", "unknown"),
        "resource_group": "monitor_project",
        "subscription_id": os.environ.get("AZURE_SUBSCRIPTION_ID"),
        "environment": finding.get("environment", "unknown"),
        "monthly_cost": cost
    }
    
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 202:
            print(f"VM approval email sent to {owner} for {finding['name']}")
        else:
            print(f"VM alert failed: {response.status_code}")
    except Exception as e:
        print(f"Error sending VM alert: {e}")