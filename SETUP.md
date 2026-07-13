# Setup Guide

## Prerequisites
- Python 3.11+
- Azure subscription (free tier works)
- Docker (for Grafana)

## Step 1 — Clone the repo
git clone https://github.com/AshenEllawala/azure-waste-detector
cd azure-waste-detector

## Step 2 — Install dependencies
pip install -r requirements.txt

## Step 3 — Create Service Principal
az ad sp create-for-rbac \
  --name "waste-detector-sp" \
  --role "Reader" \
  --scopes /subscriptions/<your-subscription-id>

az role assignment create \
  --assignee <appId> \
  --role "Cost Management Reader" \
  --scope /subscriptions/<your-subscription-id>

## Step 4 — Create .env file
AZURE_CLIENT_ID=<appId>
AZURE_CLIENT_SECRET=<password>
AZURE_TENANT_ID=<tenant>
AZURE_SUBSCRIPTION_ID=<subscription-id>
LOGIC_APP_WASTE_URL=<your-logic-app-url>
LOGIC_APP_VM_URL=<your-logic-app-url>
LOG_ANALYTICS_WORKSPACE_ID=<workspace-id>
LOG_ANALYTICS_KEY=<primary-key>

## Step 5 — Tag your test resources
Every resource needs these tags:
owner: your-email@domain.com
environment: dev or test

## Step 6 — Create Logic Apps
Import the JSON files from docs/logic-apps/ folder
into two separate Logic Apps in Azure portal

## Step 7 — Run the scanner
python main_waste.py

## Step 8 — View Grafana dashboard
docker run -d --name grafana -p 3000:3000 grafana/grafana
Import docs/grafana-dashboard.json into Grafana
Connect Azure Monitor data source