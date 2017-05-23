import boto3
import time

client =  boto3.client('sqs')
sqs = boto3.resource('sqs')

message = sqs.Message('https://sqs.us-east-1.amazonaws.com/726298423571/Kid-Queue','aAQEBVtWLS40ZPaKXIJ+AhmV1IpUZ9CDmGlZexseqtvpzI0nmIxrRFWDN7w4ehqexgNMZ2W2bKdNvGm6aGcFVhTK8+3hB/qUD//MYba0yeff9qWDsjhZ6rZFxXuKbcqL2qpMrN7pL3tluVr0nqhmVjG9VAUIos99v4BcWp/NdcJHhVDXyWUL0yLEKZV7zkXOIhlNaXn1H8Eh9/QkMWtsGb9Cmy9f/7CEEkpzO+fasktEsNd+Vz9HYSB4FJEUgS7R3g9d7sab0GQdJKm2jXct96SYM8eWYAtnqupp6ci7ahPC6TumFXmb/CWlL+xk8I0btP3N9dcQ823H9MsP3ObeccWVPJLsWq+oAL7HWcdzDPVNwvT5Mvrz+sNflohi2hdbQej9m')

ini = time.time()
x = 2000
z = x

while x > 0 :
    x =x-1
    response = client.send_message(
        QueueUrl='https://sqs.us-east-1.amazonaws.com/726298423571/Kid-Queue',
        MessageBody='Enviando mensagem pra fila',
        DelaySeconds=0,
        MessageAttributes={
            'string': {
                'StringValue': 'string',
               # 'BinaryValue': b'bytes',
               # 'StringListValues': [
               #     'string',
               # ],
                #'BinaryListValues': [
                 #   b'bytes',
                #],
                'DataType': 'String'
            }
        },
        #MessageDeduplicationId='string',
        #MessageGroupId='string'
    )
fim = time.time()

tempo = fim - ini
throuput = (z / tempo)
print(response)
print (fim - ini)
print(tempo)
print(z)
print (throuput)
