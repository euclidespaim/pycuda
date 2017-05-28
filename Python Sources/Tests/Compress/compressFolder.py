import time
import gzip
import zlib
import zipfile
from tkinter.filedialog import *


def make_zipfile(output_filename, source_dir):
    print('Iniciando compressão gzip...')
    ini = time.time()

    relroot = os.path.abspath(os.path.join(source_dir, os.pardir))
    with zipfile.ZipFile(output_filename, "w", zipfile.ZIP_BZIP2) as zip:

        for root, dirs, files in os.walk(source_dir):
            # add directory (needed for empty dirs)
            zip.write(root, os.path.relpath(root, relroot))
            for file in files:
                filename = os.path.join(root, file)
                if os.path.isfile(filename): # regular files only
                    arcname = os.path.join(os.path.relpath(root, relroot), file)
                    zip.write(filename, arcname)

    fim = time.time()
    print('Compressao gzip aplicada...')
    print('Tempo de compressão: ', fim-ini)

make_zipfile('C:\\Users\Kid\\Desktop\\down\\myZipfile.zip', 'C:\\Users\Kid\\Desktop\\up')

