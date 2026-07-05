import time
from scanner.auth import get_credential, get_subscription_id
from azure.mgmt.costmanagement import CostManagementClient
from azure.mgmt.costmanagement.models import QueryDefinition, QueryTimePeriod, QueryDataset, QueryGrouping, QueryAggregation
from datetime import datetime, timedelta, timezone

def get_resource_costs():
    credential = get_credential()
    subscription_id = get_subscription_id()
    
    client = CostManagementClient(credential)
    
    end_date = datetime.now(timezone.utc)
    start_date = end_date - timedelta(days=30)
    
    scope = f"/subscriptions/{subscription_id}"
    
    query = QueryDefinition(
        type="ActualCost",
        timeframe="Custom",
        time_period=QueryTimePeriod(
            from_property=start_date,
            to=end_date
        ),
        dataset=QueryDataset(
            granularity="None",
            aggregation={
                "totalCost": QueryAggregation(
                    name="Cost",
                    function="Sum"
                )
            },
            grouping=[
                QueryGrouping(
                    type="Dimension",
                    name="ResourceId"
                )
            ]
        )
    )
    
    for attempt in range(3):
        try:
            result = client.query.usage(scope, query)
            cost_map = {}
            for row in result.rows:
                cost_amount = round(float(row[0]), 2)
                resource_id = str(row[1])
                resource_name = resource_id.split('/')[-1].lower()
                cost_map[resource_name] = cost_amount
            return cost_map
            
        except Exception as e:
            if '429' in str(e):
                wait_time = (attempt + 1) * 30
                print(f"Rate limited by Azure. Waiting {wait_time} seconds...")
                time.sleep(wait_time)
            else:
                raise e
    
    print("Cost data unavailable after 3 attempts. Returning empty cost map.")
    return {}


def get_cost_for_resource(resource_name, cost_map):
    return cost_map.get(resource_name.lower(), 0.0)