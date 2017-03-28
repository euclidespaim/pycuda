import gzip
from threading import Thread

class NetworkTest(object):

    threads=[]

    def transmissao(self):
        print("transmitindo...")



    def compressao(self):
        content = b"Lots of content here"
        with gzip.open('c:/Users/kid/desktop/up/file.txt.gz', 'wb') as f:
            f.write(content)
        print('entrou...')

def main ():
    rede = 0

    scan = NetworkTest()
    scan.transmissao()

    if ( rede < 10):
        zip = NetworkTest()
        zip.compressao()

    return 0
if __name__ == '__main__':
    main()
