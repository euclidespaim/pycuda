import dicom
import matplotlib
import pylab

ds=dicom.read_file("C:\\Users\Kid\\Desktop\\up\\Archive.dcm")
pylab.imshow(ds.pixel_array, cmap=pylab.cm.bone)

pylab.show()
