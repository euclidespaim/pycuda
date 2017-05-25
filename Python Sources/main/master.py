import subprocess
import threading


import re
import zipfile
from tkinter.filedialog import askopenfilename


class MasterDegree (threading.Thread):

    def transmissao():
        print("Testando transmissao e zipthreads...")
        downl = str(subprocess.getoutput('speedtest-cli --simple'))
        print (downl)
        '''extract numbers from the string'''
        down = (re.findall(r"[+-]? *(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?", downl))

        return down

    def run(self):
        f = zipfile.ZipFile(self.outfile, 'w', zipfile.ZIP_DEFLATED)
        f.write(self.infile)
        f.close()
        print ('Finished background zip of: ', self.infile)

    def zip(self):
        z = zipfile.ZipFile(self.outfile, 'w', zipfile.zipfile.ZIP_BZIP2)
        z.write(self.infile)
        z.close()
        print('Finish background print 0f:', self.infile)

    def seleciona(file,):
        Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
        file = askopenfilename() # show an "Open" dialog box and return the path to the selected file
        print(file)

    def main():

        t = threading.Thread(name="trans", target=transmissao)
        t.start()
        t.join()


