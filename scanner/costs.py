from scanner.auth import get_credential, get_subscription_id
from azure.mgmt.costmanagement import CostManagementClient
from azure.mgmt.costmanagement.models import QueryDefinition, QueryTimePeriod, QueryDataset, QueryGrouping, QueryAggregation
from datetime import datetime, timedelta, timezone

def get_resource_costs():
    credential = get_credential()
    subscription_id = get_subscription_id()
    
    client = CostManagementClient(credential)
    
    # last 30 days
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
    
    result = client.query.usage(scope, query)
    
    # build dictionary - resource name = key, cost = value
    cost_map = {}
    
    for row in result.rows:
        cost_amount = round(float(row[0]), 2)
        resource_id = str(row[1])
        resource_name = resource_id.split('/')[-1].lower()
        cost_map[resource_name] = cost_amount
    
    return cost_map


def get_cost_for_resource(resource_name, cost_map):
    return cost_map.get(resource_name.lower(), 0.0)