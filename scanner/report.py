from datetime import datetime

def generate_report(waste_findings, cost_map):
    
    today = datetime.now().strftime("%Y-%m-%d")
    total_cost = 0.0
    
    print(f"\nAZURE WASTE REPORT - {today}")
    print("=" * 40)
    print(f"TOTAL WASTEFUL RESOURCES FOUND: {len(waste_findings)}")
    
    # first calculate total cost
    for finding in waste_findings:
        cost = cost_map.get(finding['name'].lower(), 0.0)
        total_cost = total_cost + cost
    
    print(f"TOTAL ESTIMATED MONTHLY WASTE: ${total_cost:.2f}")
    print("=" * 40)
    
    # then print each finding in detail
    for finding in waste_findings:
        cost = cost_map.get(finding['name'].lower(), 0.0)
        
        print(f"\n[{finding['type']}] {finding['name']}")
        print(f"  Owner       : {finding['owner']}")
        print(f"  Environment : {finding['environment']}")
        print(f"  Location    : {finding['location']}")
        print(f"  Monthly Cost: ${cost:.2f}")
    
    print("\n" + "=" * 40)
    print("ACTION REQUIRED: Contact resource owners above")
    print("=" * 40)