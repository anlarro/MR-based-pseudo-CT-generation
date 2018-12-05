"""
Script to generate error maps from inferenced images.
"""

import os
import sys

import SimpleITK as sitk

import tkinter as tk
from tkinter import filedialog

import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable

def myshow(ct,inference,diff,title='',slice='middle',figsize=(15,5)):
    if slice=='middle':
        slice=ct.shape[2]//2

    f, axes = plt.subplots(1, 3, figsize=figsize)

    ct = ct.reshape(ct.shape[:3])
    axes[0].imshow(ct[:,:,slice].transpose(), cmap='gray')
    axes[0].set_title('Ground-truth CT',fontsize=16)

    inference = inference.reshape(inference.shape[:3])
    axes[1].imshow(inference[:,:,slice].transpose(), cmap='gray')
    axes[1].set_title('Inference',fontsize=16)

    diff = diff.reshape(diff.shape[:3])
    im=axes[2].imshow(diff[:,:,slice].transpose(), cmap='gist_heat')
    axes[2].set_title('Absolute error (HU)',fontsize=16)

    divider = make_axes_locatable(axes[2])
    cax = divider.append_axes("right", size="5%", pad=0.05)
    im.set_clim(0, 1000)
    f.colorbar(im,cax=cax,ax=axes[2])


    for ax in axes:
        ax.set_axis_off()
    f.tight_layout()

    f.suptitle(title,fontsize=20)  # or plt.suptitle('Main title')
    plt.show()


reference_dir = "/media/andres/Datos/I3M/Proyectos/NiftyNet_skull_segmentation/Images/Training" #modify accordingly

if len(sys.argv)==1:
    root = tk.Tk()
    root.withdraw()
    inference_dir = filedialog.askdirectory(initialdir = "/media/andres/Datos/I3M/Proyectos/NiftyNet_skull_segmentation/NiftyNet_projects/models",title = "Inference directory")
else:
    inference_dir = sys.argv[1]

error_dir = os.path.join(os.path.dirname(inference_dir),'error_maps')

reference_files = [f for f in os.listdir(reference_dir) if f.endswith('_ct masked.mhd')]
inference_files = [f for f in os.listdir(inference_dir) if f.endswith('_niftynet_out.nii.gz')]

for i in inference_files:
    for r in reference_files:
        pos = i.find("_niftynet_out")
        if i[:pos] == r[:pos]:
            referenceVol = sitk.ReadImage(os.path.join(reference_dir, r),sitk.sitkFloat32)

            inferenceVol = sitk.ReadImage(os.path.join(inference_dir, i),sitk.sitkFloat32)

            # Generate error map
            error_map = sitk.AbsoluteValueDifference(inferenceVol,referenceVol)
            if not os.path.exists(error_dir):
                error_dir,os.mkdir(error_dir)
            sitk.WriteImage(error_map, os.path.join(error_dir, i[:pos] + '_error.nii.gz'))
           # myshow(sitk.GetArrayFromImage(referenceVol).transpose(), sitk.GetArrayFromImage(inferenceVol).transpose(), sitk.GetArrayFromImage(error_map).transpose())
            break





