from scanner.auth import get_credential, get_subscription_id
from azure.mgmt.advisor import AdvisorManagementClient

def get_advisor_recommendations():
    credential = get_credential()
    subscription_id = get_subscription_id()
    
    client = AdvisorManagementClient(credential, subscription_id)
    
    recommendations = []
    seen = set()  # track duplicates
    
    advisor_recs = client.recommendations.list()
    
    for rec in advisor_recs:
        if rec.category == "Cost" and \
           rec.impacted_field != "Microsoft.Subscriptions/subscriptions":
            # skip if already seen
            if unique_key in seen:
                continue
                
            seen.add(unique_key)
            recommendations.append({
                'name': rec.impacted_field or rec.impacted_value or 'unknown',
                'type': 'Advisor Recommendation',
                'description': rec.short_description.problem,
                'impact': rec.impact,
                'owner': 'unknown',
                'environment': 'unknown',
                'location': 'N/A'
            })
    
    return recommendations