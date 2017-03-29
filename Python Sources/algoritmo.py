import gzip
import subprocess
import re
import threading
from threading import Thread

import time

import zlib


class NetworkTest(object):

    threads=[]

    def transmissao(down=int):
        print("Testando transmissao...")
        downl = str(subprocess.getoutput('speedtest-cli --simple'))
        print (downl)
        '''extract numbers from a string'''
        down = (re.findall(r"[+-]? *(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?", downl))

        return down

    def compressao(self):
        try:
            content = b"Lots of content here"
            with gzip.open('c:/Users/kid/desktop/up/file.txt.gz', 'wb') as f:
                f.write(content)
                print('Compressao de nivel 0 aplicada...')
        except:
            print('Algo deu errado!!')

    def compress(self):
        try:
            content = b"Lots of content here"
            with gzip.open('c:/Users/kid/desktop/up/file.txt.gz', 'wb') as f:
                f.write(content)
                print('Compressao de nível 0 aplicada...')
        except:
            print('Algo saiu errado aqui!')

def main (transmissao=None, compressao=None, compress=None):

    print ('Realizando testes na rede...')

    t = threading.Thread(name='t', target= transmissao)
    c1 = threading.Thread(name='c1', target=compressao)
    c2 = threading.Thread(name='c2', target=compress)
    t.start()

    lista = NetworkTest.transmissao()
    print (lista[1])
    test = float(lista[1])

    if test < 51:
        c1.start()
        print (threading.currentThread().getName() , 'Starting')
        time.sleep(2)
        print('Compressao de nivel 1 aplicada...')
    else:
        c2.start()
        print (threading.currentThread().getName(), 'Starting')
        time.sleep(2)
        print('Compressao de nivel 2 aplicada...')

    return 0

if __name__ == '__main__':
    main()
