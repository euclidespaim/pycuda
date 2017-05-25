import boto3
import gzip
import bz2
import zlib
import subprocess
import re
import mritopng
import threading
import time
from tkinter.filedialog import *

class switch(object):
    def __init__(self, value):
        self.value = value
        self.fall = False

    def __iter__(self):
        """Return the match method once, then stop"""
        yield self.match
        raise StopIteration

    def match(self, *args):
        """Indicate whether or not to enter a case suite"""
        if self.fall or not args:
            return True
        elif self.value in args: # changed for v1.5, see below
            self.fall = True
            return True
        else:
            return False


class NetworkTest(object):

    """"Testa a qualidade da rede e retira o valor de upload da lista"""
    def transmissao():
        print("Testando transmissao...")
        downl = str(subprocess.getoutput('speedtest-cli --simple'))
        print (downl)
        # Extrai upload da lista
        down = (re.findall(r"[+-]? *(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?", downl))

        return down


    def gzipcomp():
        try:
            print('Iniciando compressão gzip...')
            f_in = open(askopenfilename(), 'rb')
            f_out = gzip.open('C:\\Users\Kid\\Desktop\\up\\Archive.gz', 'wb', 9)
            f_out.writelines(f_in)
            f_out.close()
            f_in.close()
            print('Compressao gzip aplicada...')
        except ValueError:
            print ("Oops!  That was no valid number.  Try again...")
        return  f_out

    def zlibcomp():
        try:
            print('Iniciando compressão zlib...')
            f_in = open(askopenfilename(), 'rb')
            f_out = bz2.open('C:\\Users\Kid\\Desktop\\up\\Archive.bz', 'w', 9)
            f_out.writelines(f_in)
            f_out.close()
            f_in.close()
            print('Compressao zlib aplicada...')
        except ValueError:
            print ("Oops!  That was no valid number.  Try again...")
        return  f_out

def main (transmissao=None, gzipcomp=None, zlibcomp=None):

    print ('Realizando testes na rede...')

    t = threading.Thread(name='t', target=transmissao)
    lista = NetworkTest.transmissao()
    f = float(lista[2])
    print ('float: ', f)
    v = int(f)
    print ('int: ', v)


    for case in switch(v):
        if case(5):
            c = threading.Thread(name='gzipcomp', target=NetworkTest.gzipcomp())
            print (threading.currentThread().getName() , 'Starting')
            time.sleep(2)
            print('Compressao de nivel 1 aplicada...')
            break

        if case(4):
            z = threading.Thread(name='zlibcomp', target=NetworkTest.zlibcomp())
            print (threading.currentThread().getName(), 'Starting')
            time.sleep(2)
            print('Compressao de nivel 2 aplicada...')
            break

        if case(3):
            z = threading.Thread(name='zlibcomp', target=NetworkTest.zlibcomp())
            print (threading.currentThread().getName(), 'Starting')
            time.sleep(2)
            print('Compressao de nivel 3 aplicada...')
            break

        if case(2):
            mritopng.main()
            print (threading.currentThread().getName(), 'Starting')
            time.sleep(2)
            print('Compressao de nivel 4 aplicada...')
            break

    #Publica no Topico
    client = boto3.client('sns')

    response = client.publish(
        TopicArn='arn:aws:sns:us-east-1:726298423571:DICOM',
        Message='Img .dcm ',
        Subject= 'Enviando img DICOM',
    #   MessageStructure='',
        MessageAttributes={
             'Binary': {
                'DataType': 'binary',
         #       'StringValue': 'String',
            }
        }
    )



if __name__ == '__main__':
    main()
