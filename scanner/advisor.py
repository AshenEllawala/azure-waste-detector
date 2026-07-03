from auth import get_credential, get_subscription_id
from azure.mgmt.advisor import AdvisorManagementClient

def get_advisor_recommendations():
    credential = get_credential()
    subscription_id = get_subscription_id()
    
    client = AdvisorManagementClient(credential, subscription_id)
    
    recommendations = []
    
    # get all advisor recommendations
    advisor_recs = client.recommendations.list()
    
    for rec in advisor_recs:
        # filter to Cost category only
        if rec.category == "Cost":
            recommendations.append({
                'name': rec.impacted_value,
                'type': 'Advisor Recommendation',
                'description': rec.short_description.problem,
                'impact': rec.impact,
                'owner': 'unknown',
                'environment': 'unknown'
            })
    
    return recommendations