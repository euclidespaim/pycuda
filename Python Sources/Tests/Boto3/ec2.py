import boto3

client = boto3.client('elbv2')

response = client.describe_load_balancers(
    Names=[
        'Kid-LB-Level-1',
    ],
)

print(response)

response = client.add_tags(
    ResourceArns=[
        'arn:aws:elasticloadbalancing:us-east-1:726298423571:loadbalancer/app/Kid-LB-Level-1/53827a291e40e400',
    ],
    Tags=[
        {
            'Key': 'DICOM',
            'Value': 'tag'
        },
    ]
)

print(response)
