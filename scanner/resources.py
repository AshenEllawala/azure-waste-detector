import os
from scanner.auth import get_credential, get_subscription_id
from azure.mgmt.resourcegraph import ResourceGraphClient
from azure.mgmt.resourcegraph.models import QueryRequest
from datetime import datetime

def get_all_resources():
    credential = get_credential()
    subscription_id = get_subscription_id()

    client = ResourceGraphClient(credential)

    query = QueryRequest(
        query="""
        Resources
        | project name, type, location, tags, properties, managedBy
        """,
        subscriptions=[subscription_id]
)

    result = client.resources(query)
    return result.data

def detect_orphaned_disks(resources):
    orphaned_disks = []
    
    for resource in resources:
        if resource['type'] == 'microsoft.compute/disks':
            if not resource.get('managedBy'):
                raw_tags = resource.get('tags') or {}
                tags = {k.strip().lower(): v for k, v in raw_tags.items()}
                orphaned_disks.append({
                    'name': resource['name'],
                    'type': 'Orphaned Disk',
                    'owner': tags.get('owner', 'unknown'),
                    'environment': tags.get('environment', 'unknown'),
                    'location': resource['location']
                })
    
    return orphaned_disks

def detect_orphaned_ips(resources):
    orphaned_ips = []
    
    for resource in resources:
        if resource['type'] == 'microsoft.network/publicipaddresses':

            
            if not resource['properties'].get('ipConfiguration'):
                raw_tags = resource.get('tags') or {}
                tags = {k.strip().lower(): v for k, v in raw_tags.items()}
                orphaned_ips.append({
                    'name': resource['name'],
                    'type': 'Orphaned Public IP',
                    'owner': tags.get('owner', 'unknown'),
                    'environment': tags.get('environment', 'unknown'),
                    'location': resource['location']
                })
    
    return orphaned_ips

def detect_idle_vms(resources):
    idle_vms = []
    current_hour = datetime.now().hour
    
    for resource in resources:
        if resource['type'] == 'microsoft.compute/virtualmachines':
            raw_tags = resource.get('tags') or {}
            tags = {k.strip().lower(): v for k, v in raw_tags.items()}
            environment = tags.get('environment', '')
            power_state = resource['properties'].get('extended', {}).get('instanceView', {}).get('powerState', {}).get('displayStatus', '')
            
            if environment in ['dev', 'test'] and current_hour >= 18:
                idle_vms.append({
                    'name': resource['name'],
                    'type': 'Idle Dev/Test VM',
                    'owner': tags.get('owner', 'unknown'),
                    'environment': environment,
                    'location': resource['location'],
                    'power_state': power_state
                })
    
    return idle_vms

def scan_all_waste():
    print("Scanning Azure subscription for waste...")
    
    resources = get_all_resources()
    
    orphaned_disks = detect_orphaned_disks(resources)
    orphaned_ips = detect_orphaned_ips(resources)
    idle_vms = detect_idle_vms(resources)
    
    all_waste = orphaned_disks + orphaned_ips + idle_vms
    
    return all_waste