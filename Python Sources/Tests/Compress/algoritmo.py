import gzip
import bz2
import zlib
import subprocess
import re
import threading
import time


class NetworkTest(object):

    def transmissao():
        print("Testando transmissao...")
        downl = str(subprocess.getoutput('speedtest-cli --simple'))
        print (downl)
        '''extract numbers from a string'''
        down = (re.findall(r"[+-]? *(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?", downl))

        return down

    def gzipcomp(self):

        f_in = open('C:\\Users\Kid\\Desktop\\up\\file.txt', 'rb')
        f_out = gzip.open('C:\\Users\Kid\\Desktop\\up\\file.txt.gz', 'wb', 9)
        f_out.writelines(f_in)
        f_out.close()
        f_in.close()
        print('Compressao gzip aplicada...')

    def zlibcomp():

        f_in = open('C:\\Users\Kid\\Desktop\\up\\file.txt', 'rb')
        f_out = bz2.open('C:\\Users\Kid\\Desktop\\up\\file.txt.bz', 'w', 9)
        f_out.writelines(f_in)
        f_out.close()
        f_in.close()
        print('Compressao zlib aplicada...')

def main (transmissao=None, gzipcomp=NetworkTest):

    print ('Realizando testes na rede...')

    t = threading.Thread(name='t', target=transmissao)
    lista = NetworkTest.transmissao()
    print (lista[1])
    test = float(lista[1])

    if test < 60:
        c = threading.Thread(name='gzipcomp', target=gzipcomp())
        print (threading.currentThread().getName() , 'Starting')
        time.sleep(2)
        print('Compressao de nivel 1 aplicada...')
    else:
        z = threading.Thread(name='zlibcomp', target=zlibcomp())
        print (threading.currentThread().getName(), 'Starting')
        time.sleep(2)
        print('Compressao de nivel 2 aplicada...')


if __name__ == '__main__':
    main()
