from scanner.resources import scan_all_waste
from scanner.costs import get_resource_costs
from scanner.report import generate_report
from scanner.alerts import send_vm_alert

def main():
    print("Starting Azure VM Scanner - Evening Run...")
    
    waste_findings = scan_all_waste()
    
    vm_findings = [f for f in waste_findings if f['type'] == 'Idle Dev/Test VM']
    
    if not vm_findings:
        print("No idle VMs found.")
        return
    
    cost_map = get_resource_costs()
    generate_report(vm_findings, cost_map)
    
    print("\nSending VM approval emails...")
    for finding in vm_findings:
        cost = cost_map.get(finding['name'].lower(), 0.0)
        
        if finding.get('owner') == 'unknown':
            print(f"Skipping {finding['name']} - owner unknown")
            continue
        
        send_vm_alert(finding, cost)

if __name__ == "__main__":
    main()