import boto3

client =  boto3.client('sqs')
sqs = boto3.resource('sqs')

response = client.receive_message(
    QueueUrl='https://sqs.us-east-1.amazonaws.com/726298423571/Kid-Queue',
    AttributeNames=[ 'All'
   #     'All'|'Policy'|'VisibilityTimeout'|'MaximumMessageSize'|'MessageRetentionPeriod'|'ApproximateNumberOfMessages'|'ApproximateNumberOfMessagesNotVisible'|'CreatedTimestamp'|'LastModifiedTimestamp'|'QueueArn'|'ApproximateNumberOfMessagesDelayed'|'DelaySeconds'|'ReceiveMessageWaitTimeSeconds'|'RedrivePolicy'|'FifoQueue'|'ContentBasedDeduplication'|'KmsMasterKeyId'|'KmsDataKeyReusePeriodSeconds',
    ],
 #   MessageAttributeNames=[
  #      'string',
   # ],
    MaxNumberOfMessages=10,
    VisibilityTimeout=123,
    WaitTimeSeconds=0,
  #  ReceiveRequestAttemptId='string'
)

print (response)
print(message)
