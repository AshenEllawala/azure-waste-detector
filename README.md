from resources import scan_all_waste
from costs import get_resource_costs
from report import generate_report

def main():
    print("Starting Azure Waste Detector...")
    
    # Step 1: detect all wasteful resources
    print("Scanning for wasteful resources...")
    waste_findings = scan_all_waste()
    
    # Step 2: check if anything was found
    if not waste_findings:
        print("No wasteful resources found. Subscription looks clean!")
        return
    
    # Step 3: get cost data for found resources
    print("Fetching cost data...")
    cost_map = get_resource_costs()
    
    # Step 4: generate and print the report
    print("Generating report...")
    generate_report(waste_findings, cost_map)

if __name__ == "__main__":
    main()