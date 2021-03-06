import gzip
import bz2
import subprocess
import re
import threading
import time
from tkinter.filedialog import askopenfilename


def gzipcomp():
    f_in = open(askopenfilename(), 'rb')
    f_out = gzip.open('C:\\Users\Kid\\Desktop\\up\\myarchive.gz', 'wb', 9)
    f_out.writelines(f_in)
    f_out.close()
    f_in.close()
    print('Compressao gzip aplicada...')

def zlibcomp():

    f_in = open(askopenfilename(), 'rb')
    f_out = bz2.open('C:\\Users\Kid\\Desktop\\up\\myarchive.bz', 'w', 9)
    f_out.writelines(f_in)
    f_out.close()
    f_in.close()
    print('Compressao bz2 aplicada...')

def transmissao():
    print("Testando transmissao...")
    downl = str(subprocess.getoutput('speedtest-cli --simple'))
    print (downl)
    '''extract numbers from a string'''
    down = (re.findall(r"[+-]? *(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?", downl))

    return down

def main():

    t = threading.Thread(name='t', target=transmissao)
    lista = transmissao()
    print (lista[1])
    test = float(lista[1])

    if test < 55:
        c = threading.Thread(name='gzipcomp', target=gzipcomp())
        c.start()
        c.join()
    else:
        z = threading.Thread(name='zlibcomp', target=zlibcomp())
        z.start()
        z.join()
if __name__ == '__main__':
    main()
