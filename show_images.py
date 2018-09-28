#Function to visualize the MR, CT and labels slices contained in a folder
import os
import SimpleITK as sitk
import matplotlib.pyplot as plt
import numpy as np

vol_dir = "D:/I3M/Proyectos/NiftyNet_skull_segmentation/Images/Training" #modify accordingly

def plot_slices(vol_dir=vol_dir,id=0,slice='middle',figsize=(10,5)):
    mr_files = [f for f in os.listdir(vol_dir) if f.endswith('_mr_T1.mhd')]
    ct_files = [f for f in os.listdir(vol_dir) if f.endswith('_ct.mhd')]
    label_files = [f for f in os.listdir(vol_dir) if f.endswith('_labels.mhd')]

    mrVol = sitk.ReadImage(os.path.join(vol_dir, mr_files[id]))
    ctVol = sitk.ReadImage(os.path.join(vol_dir, ct_files[id]))
    labelsVol = sitk.ReadImage(os.path.join(vol_dir, label_files[id]))

    f, axes = plt.subplots(1, 3, figsize=figsize)
    nda = sitk.GetArrayFromImage(mrVol)
    if slice=='middle':
        slice=nda.shape[0]//2
    axes[0].imshow(nda[slice], cmap='gray')
    axes[0].set_title('MR-T1 %s' % id)
    nda = sitk.GetArrayFromImage(ctVol)
    if slice=='middle':
        slice=nda.shape[0]//2
    axes[1].imshow(nda[slice], cmap='gray')
    axes[1].set_title('CT %s' % id)
    nda = sitk.GetArrayFromImage(labelsVol)
    if slice=='middle':
        slice=nda.shape[0]//2
    axes[2].imshow(nda[slice], cmap='gray')
    axes[2].set_title('Labels %s' % id)
    for ax in axes:
        ax.set_axis_off()
    f.tight_layout()
    plt.show()