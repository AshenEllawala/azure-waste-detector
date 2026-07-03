from scanner.resources import scan_all_waste
from scanner.costs import get_resource_costs
from scanner.report import generate_report
from scanner.advisor import get_advisor_recommendations

def main():
    print("Starting Azure Waste Detector...")
    
    # Step 1: detect wasteful resources directly
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

if __name__ == "__main__":
    main()