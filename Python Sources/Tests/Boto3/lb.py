import boto3

client = boto3.client('elbv2')

response = client.describe_load_balancers(
    Names=[
        'Kid-LB-Level-1',
    ],
)

print(response)

response = client.attach_load_balancers(
    AutoScalingGroupName='string',
    LoadBalancerNames=[
        'string',
    ]
)
