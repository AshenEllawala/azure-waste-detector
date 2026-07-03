# Azure Idle Resource & Cost Waste Detector

## Problem
Companies waste 27-32% of cloud spend on idle and orphaned 
Azure resources. Azure provides detection via Advisor but 
no automated owner-routing or remediation.

## What This Solves
Automated scanner that detects wasteful resources, matches 
them to owners via tags, routes alerts to the right person, 
and auto-shuts down idle dev/test VMs after hours.

## Architecture
(diagram coming Week 4)

## Waste Detection Rules
- Unattached managed disks
- Orphaned public IPs
- Dev/test VMs running after 6pm

## Tech Stack
- Python (Azure SDK)
- Azure Resource Graph API
- Azure Cost Management API
- Azure Advisor API
- Azure Automation (runbook)
- Logic Apps (approval email)
- Azure Policy (tag governance)

## Weekly Progress
- [x] Week 1 — Environment setup, tagging, governance
- [ ] Week 2 — Data collection layer (APIs)
- [ ] Week 3 — Owner matching and alerts
- [ ] Week 4 — Automation and shutdown runbook
- [ ] Week 5 — Polish, dashboard, case study writeup

## What I'd Improve for Production
(filling this in as I build)

## Author
Ashen Ellawala  
BICT (Network Technology) — University of Kelaniya
