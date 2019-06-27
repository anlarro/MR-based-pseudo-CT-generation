#Function to register two volumes

import SimpleITK as sitk

from Registration.getParameterMap import getParameterMap

def register(fixed, moving, fixed_mask=None, moving_mask=None):
    parameterMapVector = getParameterMap()
    elastixImageFilter = sitk.ElastixImageFilter()
    elastixImageFilter.SetParameterMap(parameterMapVector)

    elastixImageFilter.SetFixedImage(fixed)
    elastixImageFilter.SetMovingImage(moving)

    if fixed_mask is not None:
        elastixImageFilter.SetFixedMask(fixed_mask)

    if moving_mask is not None:
        elastixImageFilter.SetFixedMask(moving_mask)


    elastixImageFilter.Execute()
    result = elastixImageFilter.GetResultImage()

    return result