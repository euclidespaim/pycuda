import boto3

# Create SQS client
sqs = boto3.client('sqs')

# Create a SQS queue with long polling enabled
response = sqs.create_queue(
    QueueName='Kid-Queue',
    Attributes={'ReceiveMessageWaitTimeSeconds': '20'}
)

print(response['QueueUrl'])
