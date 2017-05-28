import gzip

f_in = open(askopenfilename(), 'rb')
f_out = gzip.open('C:\\Users\Kid\\Desktop\\up\\Archive.gz', 'wb', 9)
f_out.writelines(f_in)
f_out.close()
f_in.close()
