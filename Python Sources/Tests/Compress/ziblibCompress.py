import gzip
import os
import time

import zlib


def make_zipfile(output_filename, source_dir):
    print('Iniciando compressão gzip...')
    ini = time.time()

    relroot = os.path.abspath(os.path.join(source_dir, os.pardir))
    with gzip.GzipFile(source_dir,'rb') as f:
        for root, dirs, files in os.walk(source_dir):
            # add directory (needed for empty dirs)
            f.write(root, os.path.relpath(root, relroot))
            for file in files:
                filename = os.path.join(root, file)
                if os.path.isfile(filename): # regular files only
                    arcname = os.path.join(os.path.relpath(root, relroot), file)
                    f.write(filename, arcname)

    fim = time.time()
    print('Compressao gzip aplicada...')
    print('Tempo de compressão: ', fim-ini)

make_zipfile('C:\\Users\Kid\\Desktop\\up', 'C:\\Users\Kid\\Desktop\\down\\dicom.gz')
