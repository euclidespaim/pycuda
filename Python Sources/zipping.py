import gzip
import bz2

def gzipcomp():

    f_in = open('C:\\Users\Kid\\Desktop\\up\\file.txt', 'rb')
    f_out = gzip.open('C:\\Users\Kid\\Desktop\\up\\file.txt.gz', 'wb', 9)
    f_out.writelines(f_in)
    f_out.close()
    f_in.close()

def zlibcomp():

    f_in = open('C:\\Users\Kid\\Desktop\\up\\file.txt', 'rb')
    f_out = bz2.open('C:\\Users\Kid\\Desktop\\up\\file.txt.bz', 'w', 9)
    f_out.writelines(f_in)
    f_out.close()
    f_in.close()

def main():

    gzipcomp()
    zlibcomp()

if __name__ == '__main__':
    main()
