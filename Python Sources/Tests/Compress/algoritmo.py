import gzip
import bz2
import zlib
import subprocess
import re
import threading
import time
from tkinter.filedialog import *


class NetworkTest(object):

    def transmissao():
        print("Testando transmissao...")
        downl = str(subprocess.getoutput('speedtest-cli --simple'))
        print (downl)
        '''extract numbers from a string'''
        down = (re.findall(r"[+-]? *(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?", downl))

        return down

    def gzipcomp():
        print('Iniciando compressão gzip...')
        f_in = open(askopenfilename(), 'rb')
        f_out = gzip.open('C:\\Users\Kid\\Desktop\\up\\Archive.gz', 'wb', 9)
        f_out.writelines(f_in)
        f_out.close()
        f_in.close()
        print('Compressao gzip aplicada...')
        return  f_out

    def zlibcomp():
        print('Iniciando compressão zlib...')
        f_in = open(askopenfilename(), 'rb')
        f_out = bz2.open('C:\\Users\Kid\\Desktop\\up\\Archive.bz', 'w', 9)
        f_out.writelines(f_in)
        f_out.close()
        f_in.close()
        print('Compressao zlib aplicada...')
        return  f_out

def main (transmissao=None, gzipcomp=None, zlibcomp=None):

    print ('Realizando testes na rede...')

    t = threading.Thread(name='t', target=transmissao)
    lista = NetworkTest.transmissao()
    print (lista[1])
    test = float(lista[1])

    if test < 65:
        c = threading.Thread(name='gzipcomp', target=NetworkTest.gzipcomp())
        print (threading.currentThread().getName() , 'Starting')
        time.sleep(2)
        print('Compressao de nivel 1 aplicada...')
    else:
        z = threading.Thread(name='zlibcomp', target=NetworkTest.zlibcomp())
        print (threading.currentThread().getName(), 'Starting')
        time.sleep(2)
        print('Compressao de nivel 2 aplicada...')


if __name__ == '__main__':
    main()
