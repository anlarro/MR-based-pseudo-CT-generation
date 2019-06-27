"""
Script to generate error maps from inferenced images.
"""

import sys
niftynet_path = '/mnt/D8D413E4D413C422/I3M/Proyectos/NiftyNet_skull_segmentation/NiftyNet_projects' #modify accordingly
sys.path.insert(0,niftynet_path)
from niftynet.io.image_reader import ImageReader

import os
import numpy as np
import SimpleITK as sitk

import tkinter as tk
from tkinter import filedialog

import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable



def myshow(ct,inference,diff,title='',slice='middle',figsize=(15,5)):
    if slice=='middle':
        slice=ct.shape[2]//2


    f, axes = plt.subplots(1, 3, figsize=figsize)
    plt.subplots_adjust(wspace=0)

    ct = ct.reshape(ct.shape[:3])
    axes[0].imshow(ct[:,:,slice].transpose(), cmap='gray')
    axes[0].set_title('Ground-truth CT',fontsize=32)

    inference = inference.reshape(inference.shape[:3])
    axes[1].imshow(inference[:,:,slice].transpose(), cmap='gray')
    axes[1].set_title('Synthetic CT',fontsize=32)

    diff = diff.reshape(diff.shape[:3])
    im=axes[2].imshow(diff[:,:,slice].transpose(), cmap='gist_heat')
    axes[2].set_title('Absolute error (HU)',fontsize=32)

    divider = make_axes_locatable(axes[2])
    cax = divider.append_axes("right", size="5%", pad=0.05)
    im.set_clim(0, 600)
    cax.tick_params(labelsize=16)
    f.colorbar(im,cax=cax,ax=axes[2])


    for ax in axes:
        ax.set_axis_off()
    f.tight_layout()

    f.suptitle(title,fontsize=20)  # or plt.suptitle('Main title')
    plt.subplots_adjust(top=1, bottom=0, right=1, left=0,hspace=0, wspace=0)
    plt.margins(0, 0)
    plt.show()
    plt.savefig('error_map1.tiff', format='tiff', dpi=300, bbox_inches='tight')


if len(sys.argv)==1:
    root = tk.Tk()
    root.withdraw()
    inference_dir = filedialog.askdirectory(initialdir = "/mnt/D8D413E4D413C422/I3M/Proyectos/NiftyNet_skull_segmentation/NiftyNet_projects/proyectos/pseudoCT_regression/modelsRIRE_EMBC",title = "Inference directory")
else:
    inference_dir = sys.argv[1]

reference_dir = "/mnt/D8D413E4D413C422/I3M/Proyectos/NiftyNet_skull_segmentation/NiftyNet_projects/Images/Training/ALL" #modify accordingly
error_dir = os.path.join(os.path.dirname(inference_dir),'error_maps')

data_param = {'CT': {'path_to_search': reference_dir,'spatial_window_size': (48,48,48),
            'filename_contains': '_ct_tra_reg masked', 'pixdim': (1.5,1.5,1.5), 'axcodes': ['L','P','S'],'interp_order': 3},
            'INF': {'path_to_search': inference_dir, 'spatial_window_size': (48,48,48),
            'filename_contains': '_niftynet_out','pixdim': (1.5,1.5,1.5), 'axcodes': ['L','P','S'],'interp_order': 3},
            'MRT1SE': {'path_to_search': reference_dir,'spatial_window_size': (48,48,48),
            'filename_contains': '_mrT1SE_reg masked', 'pixdim': (1.5,1.5,1.5), 'axcodes': ['L','P','S'],'interp_order': 3},
            'MRT2': {'path_to_search': reference_dir,'spatial_window_size': (48,48,48),
            'filename_contains': '_mrT2_reg masked', 'pixdim': (1.5,1.5,1.5), 'axcodes': ['L','P','S'],'interp_order': 3},
             }

reader = ImageReader().initialise(data_param)

inference_files = [f for f in os.listdir(inference_dir) if f.endswith('_niftynet_out.nii.gz')]
inference_files.sort()

for i,f in enumerate(inference_files):
    pos = f.find("_niftynet_out")
    _, vols, _ = reader(idx=i)

    referenceVol = vols['CT']
    inferenceVol = vols['INF']

    #Generate error map
    error_map = np.abs(inferenceVol-referenceVol)
    # if not os.path.exists(error_dir):
    #     error_dir,os.mkdir(error_dir)    # sitk.WriteImage(error_map, os.path.join(error_dir, i[:pos] + '_error.nii.gz'))
    myshow(referenceVol[25:150, 5:130, 5:165], inferenceVol[25:150, 5:130, 5:165], error_map[25:150, 5:130, 5:165])
    myshow(referenceVol[25:150,5:130,5:165], inferenceVol[25:150,5:130,5:165], error_map[25:150,5:130,5:165],slice=60)

# for i in inference_files:
#     for r in reference_files:
#         pos = i.find("_niftynet_out")
#         if i[:pos] == r[:pos]:
#             referenceVol = sitk.ReadImage(os.path.join(reference_dir, r),sitk.sitkFloat32)
#
#             inferenceVol = sitk.ReadImage(os.path.join(inference_dir, i),sitk.sitkFloat32)
#
#             # Generate error map
#             error_map = sitk.AbsoluteValueDifference(inferenceVol,referenceVol)
#             if not os.path.exists(error_dir):
#                 error_dir,os.mkdir(error_dir)
#             sitk.WriteImage(error_map, os.path.join(error_dir, i[:pos] + '_error.nii.gz'))
#             myshow(sitk.GetArrayFromImage(referenceVol).transpose(), sitk.GetArrayFromImage(inferenceVol).transpose(), sitk.GetArrayFromImage(error_map).transpose())
#             break
#
#



