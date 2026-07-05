from scanner.resources import scan_all_waste
from scanner.costs import get_resource_costs
from scanner.report import generate_report
from scanner.advisor import get_advisor_recommendations
from scanner.alerts import send_waste_alert, send_vm_alert

def main():
    print("Starting Azure Waste Detector...")
    
    # Step 1: detect wasteful resources
    print("Scanning for wasteful resources...")
    waste_findings = scan_all_waste()
    
    # Step 2: get advisor recommendations
    print("Fetching Advisor recommendations...")
    advisor_findings = get_advisor_recommendations()
    
    # Step 3: combine both sources
    all_findings = waste_findings + advisor_findings
    
    # Step 4: check if anything found
    if not all_findings:
        print("No wasteful resources found. Subscription looks clean!")
        return
    
    # Step 5: get cost data
    print("Fetching cost data...")
    cost_map = get_resource_costs()
    
    # Step 6: generate report
    print("Generating report...")
    generate_report(all_findings, cost_map)
    
    # Step 7: send alerts to owners
    print("\nSending alerts to resource owners...")
    for finding in all_findings:
        cost = cost_map.get(finding['name'].lower(), 0.0)
        
        # skip if owner unknown - can't route alert
        if finding.get('owner') == 'unknown':
            print(f"Skipping alert for {finding['name']} - owner unknown")
            continue
        
        if finding['type'] == 'Idle Dev/Test VM':
            send_vm_alert(finding, cost)
        else:
            send_waste_alert(finding, cost)

if __name__ == "__main__":
    main()