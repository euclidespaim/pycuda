import gzip
import os

home = 'C:\\Users\Kid\\Desktop\\up\\'
backup_dir = 'C:\\Users\Kid\\Desktop\\down\\'

home_dirs = [ name for name in os.listdir(home) if os.path.isdir(os.path.join(home, name)) ]

for directory in home_dirs:
    full_dir = os.path.join(home, directory)
    z = gzip.open(os.path.join(backup_dir, directory+'.zip'), mode='rb')
    gzip.compress(full_dir, compresslevel=5)
    gzip.close()
