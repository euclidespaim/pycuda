import os
import zipfile

import time


def zipdir(path, ziph):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file))

if __name__ == '__main__':
    print('Iniciando Compressão!!')
    ini = time.time()

    zipf = zipfile.ZipFile('Python.zip', 'w', zipfile.ZIP_DEFLATED)
    zipdir('tmp/', zipf)
    zipf.close()

    fim = time.time()
    print('Compressao gzip aplicada...')
    print('Tempo de compressão: ', fim-ini)
