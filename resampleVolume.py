import SimpleITK as sitk
import numpy as np

def resampleVolume(volume, new_spacing,default_pixel_value=0):
    resample = sitk.ResampleImageFilter()
    resample.SetInterpolator(sitk.sitkBSpline)
    resample.SetOutputDirection(volume.GetDirection())
    resample.SetOutputOrigin(volume.GetOrigin())
    resample.SetOutputSpacing(new_spacing)
    resample.SetDefaultPixelValue(default_pixel_value)

    orig_size = np.array(volume.GetSize(), dtype=np.int)
    orig_spacing = np.array(volume.GetSpacing())
    new_size = orig_size * (orig_spacing / new_spacing)
    new_size = np.ceil(new_size).astype(np.int)  # Image dimensions are in integers
    new_size = [int(s) for s in new_size]
    resample.SetSize(new_size)
    newVolume = resample.Execute(volume)
    return newVolume