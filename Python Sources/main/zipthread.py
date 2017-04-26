import subprocess
import threading, zipfile
import re
from tkinter.filedialog import askopenfilename, Tk


class AsyncZip(threading.Thread):

    def __init__(self, infile, outfile):
        threading.Thread.__init__(self)
        self.infile = infile
        self.outfile = outfile

    def transmissao():
        print("Testando transmissao e zipthreads...")
        downl = str(subprocess.getoutput('speedtest-cli --simple'))
        print (downl)
        '''extract numbers from the string'''
        down = (re.findall(r"[+-]? *(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?", downl))

        return down

    def runz(self, outfile):
        f = zipfile.ZipFile(self.outfile, 'w', zipfile.ZIP_DEFLATED)
        f.write(self.infile)
        f.close()
        print ('Finished background zip of: ', self.infile)

    def zipz(self, outfile):
        z = zipfile.ZipFile(self.outfile, 'w', zipfile.zipfile.ZIP_BZIP2)
        z.write(self.infile)
        z.close()
        print('Finish background print 0f:', self.infile)

    def seleciona(file,):
        Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
        file = askopenfilename() # show an "Open" dialog box and return the path to the selected file
        print(file)


lista = AsyncZip.transmissao()
print ('Aplicando compressao com base na velocidade de upload da rede:'+lista[2]+' Mbit/s')
test = float(lista[2])

if test < 5:
    Tk().withdraw()
    background = AsyncZip.runz(askopenfilename(), 'C:\\Users\Kid\\Desktop\\up\\myarchive.gz')
    background.start()
    print ('The main program continues to run in foreground.')
    background.join()    # Wait for the background task to finish
    print ('Compressao gzip aplicada.')
else:
    Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
    background = AsyncZip.zipz(askopenfilename(), 'C:\\Users\Kid\\Desktop\\up\\myarchive.bz')
    background.start()
    print('Compress bz2 aplicada.')
    background.join()
    print ('Main program waited until background was done.')
