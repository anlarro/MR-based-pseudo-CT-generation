import SimpleITK as sitk
import numpy as np

def createHeadMask(volume,direction=None):
    otsuFilter = sitk.OtsuThresholdImageFilter()
    otsuFilter.SetInsideValue(0)
    otsuFilter.SetOutsideValue(1)
    seg = otsuFilter.Execute(volume)

    ccFilter = sitk.ConnectedComponentImageFilter()
    ccFilter.FullyConnectedOn()
    labels = ccFilter.Execute(seg)

    relabelFilter = sitk.RelabelComponentImageFilter() #Relabels and sort by order (largest cc with label1, next with label2 etc)
    labels = relabelFilter.Execute(labels)

    binaryFilter = sitk.BinaryThresholdImageFilter() #Now we get only the largest ConnectedComponent(label)
    binaryFilter.SetLowerThreshold(1)
    binaryFilter.SetUpperThreshold(1)
    mask = binaryFilter.Execute(labels)

    #Fill holes slice by slice in the axial direction
    if direction=="tra":
        # headMask = sitk.JoinSeries()
        mask_slices = [sitk.BinaryFillhole(mask[:, :, z], fullyConnected=True) for z in range(mask.GetSize()[2])]
        headMask = sitk.GetImageFromArray(np.dstack([sitk.GetArrayFromImage(i).transpose(1, 0) for i in mask_slices]).transpose(2, 1, 0))
    else:
        # headMask = sitk.JoinSeries() #JoinSeries doesn't work here, that'swhy we use numpy arrays
        mask_slices = [sitk.BinaryFillhole(mask[:, y, :], fullyConnected=True) for y in range(mask.GetSize()[1])]
        headMask = sitk.GetImageFromArray(np.dstack([sitk.GetArrayFromImage(i).transpose(1, 0) for i in mask_slices]).transpose(1, 2, 0))
    #sitk Image is in (z,y,x) and numpy array in (x,y,z), that's why we transpose every transforming operation
    headMask.CopyInformation(mask) #copy the metadata to the headMask

    dilated_headMask = sitk.BinaryDilate(headMask,1)

    return dilated_headMask