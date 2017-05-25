import boto3

client = boto3.client('sns')

topico = 25;

while topico > 0:
    topico = topico - 1;
    response = client.publish(
        TopicArn='arn:aws:sns:us-east-1:726298423571:DICOM',
        Message='Testando Topico',
        Subject='Enviando img DICOM',
    #   MessageStructure='texto',
        MessageAttributes={
             'Binary': {
                 'DataType': 'Binary',
                 'BinaryValue': b'bytes'
             }
        }
)


print(response)
