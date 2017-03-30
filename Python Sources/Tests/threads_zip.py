import subprocess
import threading, zipfile
import bz2
import re

class AsyncZip(threading.Thread):

    def transmissao():
        print("Testando transmissao...")
        downl = str(subprocess.getoutput('speedtest-cli --simple'))
        print (downl)
        '''extract numbers from the string'''
        down = (re.findall(r"[+-]? *(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?", downl))

        return down

    def __init__(self, infile, outfile):
        threading.Thread.__init__(self)
        self.infile = infile
        self.outfile = outfile

    def function_zip(self):
        background = AsyncZip('C:\\Users\Kid\\Desktop\\up\\000001.dcm', 'C:\\Users\Kid\\Desktop\\up\\myarchive.bz')
        background.start()
        f = zipfile.ZipFile(self.outfile, 'w', zipfile.ZIP_DEFLATED)
        f.write(self.infile)
        f.close()
        print('Compress bz2 aplicada.')
        background.join()
        print ('Finished background zip of: ', self.infile)
        pass

    def function_bzip(self):
        background = AsyncZip('C:\\Users\Kid\\Desktop\\up\\000001.dcm', 'C:\\Users\Kid\\Desktop\\up\\myarchive.zip')
        background.start()
        z = zipfile.ZipFile(self.outfile, 'w', zipfile.zipfile.ZIP_BZIP2)
        z.write(self.infile)
        z.close()
        print ('The main program continues to run in foreground.')
        background.join()    # Wait for the background task to finish
        print('Finish background print 0f:', self.infile)
        pass

lista = AsyncZip.transmissao()
print ('Aplicando compressao com base na velocidade de upload da rede:'+lista[2]+' Mbit/s')
test = float(lista[2])

if test < 6:
    AsyncZip.function_zip(0)
    print ('Main program waited until background zip done.')
else:
    AsyncZip.function_bzip(0)
    print ('Main program waited until background bzip done.')
