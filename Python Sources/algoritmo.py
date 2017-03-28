import gzip
import subprocess
from threading import Thread

class NetworkTest(object):

    threads=[]

    def transmissao(upl,):
        downl = subprocess.getoutput('speedtest-cli --csv')
        '''upl = subprocess.getoutput('speedtest-cli --csv')'''
        print("transmitindo...")

        print(downl)
        print(upl)


    def compressao(self):
        content = b"Lots of content here"
        with gzip.open('c:/Users/kid/desktop/up/file.txt.gz', 'wb') as f:
            f.write(content)

        print('entrou...')

def main ():
    print ('Realizando teste de rede...')

    scan = NetworkTest()
    scan.transmissao()

    '''if len(upl) < 10:'''
    zip = NetworkTest()
    zip.compressao()

    return 0
if __name__ == '__main__':
    main()
