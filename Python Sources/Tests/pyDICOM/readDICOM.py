import dicom

ds = dicom.read_file("C:\\Users\Kid\\Desktop\\up\\Archive.dcm")

print(ds.PixelData)
print(ds.pixel_array)
print(ds.pixel_array.shape)

"""for n,val in enumerate(ds.pixel_array.flat): # example: zero anything < 300
   if val < 300:
        ds.pixel_array.flat[n]=0
ds.PixelData = ds.pixel_array.tostring()
ds.save_as("C:\\Users\Kid\\Desktop\\up\\newfilename.dcm")"""
