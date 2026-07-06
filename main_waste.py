from scanner.resources import scan_all_waste
from scanner.costs import get_resource_costs
from scanner.report import generate_report
from scanner.advisor import get_advisor_recommendations
from scanner.alerts import send_waste_alert

def main():
    print("Starting Azure Waste Scanner - Morning Run...")
    
    waste_findings = scan_all_waste()
    advisor_findings = get_advisor_recommendations()
    all_findings = waste_findings + advisor_findings
    
    if not all_findings:
        print("No wasteful resources found. Subscription looks clean!")
        return
    
    cost_map = get_resource_costs()
    generate_report(all_findings, cost_map)
    
    print("\nSending waste alerts...")
    for finding in all_findings:
        cost = cost_map.get(finding['name'].lower(), 0.0)
        
        if finding.get('owner') == 'unknown':
            print(f"Skipping {finding['name']} - owner unknown")
            continue
        
        if finding['type'] != 'Idle Dev/Test VM':
            send_waste_alert(finding, cost)

if __name__ == "__main__":
    main()