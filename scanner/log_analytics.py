import os
import json
import hmac
import hashlib
import base64
import requests
from datetime import datetime, timezone
from dotenv import load_dotenv

load_dotenv()

def build_signature(workspace_id, key, date, content_length, method, content_type, resource):
    x_headers = f"x-ms-date:{date}"
    string_to_hash = f"{method}\n{content_length}\n{content_type}\n{x_headers}\n{resource}"
    bytes_to_hash = bytes(string_to_hash, encoding="utf-8")
    decoded_key = base64.b64decode(key)
    encoded_hash = base64.b64encode(
        hmac.new(decoded_key, bytes_to_hash, digestmod=hashlib.sha256).digest()
    ).decode()
    return f"SharedKey {workspace_id}:{encoded_hash}"


def post_to_log_analytics(log_type, data):
    workspace_id = os.environ.get("LOG_ANALYTICS_WORKSPACE_ID")
    key = os.environ.get("LOG_ANALYTICS_KEY")
    
    if not workspace_id or not key:
        print("Log Analytics credentials not configured")
        return
    
    body = json.dumps(data)
    method = "POST"
    content_type = "application/json"
    resource = "/api/logs"
    rfc1123date = datetime.now(timezone.utc).strftime('%a, %d %b %Y %H:%M:%S GMT')
    content_length = len(body)
    
    signature = build_signature(
        workspace_id, key, rfc1123date,
        content_length, method, content_type, resource
    )
    
    uri = f"https://{workspace_id}.ods.opinsights.azure.com{resource}?api-version=2016-04-01"
    
    headers = {
        "Content-Type": content_type,
        "Authorization": signature,
        "Log-Type": log_type,
        "x-ms-date": rfc1123date
    }
    
    response = requests.post(uri, data=body, headers=headers)
    
    if response.status_code == 200:
        print(f"Successfully wrote {len(data)} findings to Log Analytics")
    else:
        print(f"Failed to write to Log Analytics: {response.status_code}")


def write_waste_findings(all_findings, cost_map):
    logs = []
    total_waste = 0.0
    
    for finding in all_findings:
        cost = cost_map.get(finding['name'].lower(), 0.0)
        total_waste += cost
        
        logs.append({
            "TimeGenerated": datetime.now(timezone.utc).isoformat(),
            "ResourceName": finding.get('name', 'unknown'),
            "ResourceType": finding.get('type', 'unknown'),
            "Owner": finding.get('owner', 'unknown'),
            "Environment": finding.get('environment', 'unknown'),
            "Location": finding.get('location', 'unknown'),
            "MonthlyCost": cost,
            "TotalWasteCost": total_waste
        })
    
    if logs:
        post_to_log_analytics("AzureWasteFindings", logs)
    else:
        print("No findings to write to Log Analytics")