import gzip
import subprocess
import re
import threading
from threading import Thread

class NetworkTest(object):

    threads=[]

    def transmissao(down=int):
        print("Testando transmissao...")
        downl = str(subprocess.getoutput('speedtest-cli --simple'))
        print (downl)
        '''print([x for x in downl().iterint()])'''
        down = (re.findall(r"[+-]? *(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?", downl))
        '''upl = subprocess.getoutput('speedtest-cli --csv')'''

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

    t = threading.Thread(name='transmissao', target= transmissao)
    c1 = threading.Thread(name='compressao', target=compressao)
    c2 = threading.Thread(name='compress', target=compress)
    t.start()

    lista = NetworkTest.transmissao()
    print (lista[1])
    test = float(lista[1])

    if test < 50:
        c1.start()
        print('Compressao de nivel 1 aplicada...')
    else:
        c2.start()
        print('Compressao de nivel 2 aplicada...')

    return 0

if __name__ == '__main__':
    main()
