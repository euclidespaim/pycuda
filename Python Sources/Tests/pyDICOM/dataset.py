import pydicom

ds = pydicom.read_file("C:\\Users\Kid\\Desktop\\up\\Archive.dcm") # (rtplan.dcm is in the testfiles directory)


print (ds)
