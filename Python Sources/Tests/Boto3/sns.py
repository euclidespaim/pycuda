import boto3

client = boto3.client('sns')

response = client.publish(
    TopicArn='arn:aws:sns:us-east-1:726298423571:DICOM',
    Message='Testando Topico',
    Subject='Bundas',
#   MessageStructure='Bundas Cabeludas',
  # MessageAttributes={
   #     'String': {
    #        'DataType': 'String',
     #       'StringValue': 'String',
      #  }
    #}
)

print(response)
