"""
Script to evaluate the regression results by computing different measures
"""
import sys
niftynet_path = '/mnt/D8D413E4D413C422/I3M/Proyectos/NiftyNet_skull_segmentation/NiftyNet_projects' #modify accordingly
sys.path.insert(0,niftynet_path)
from niftynet.io.image_reader import ImageReader

import os

import SimpleITK as sitk
import numpy as np

import tkinter as tk
from tkinter import filedialog

import csv

import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable

#Modify data_param according to the available image data
#For this example, read only one volume
# if len(sys.argv)==1:
#     root = tk.Tk()
#     root.withdraw()
#     inference_dir = filedialog.askdirectory(initialdir = "/mnt/D8D413E4D413C422/I3M/Proyectos/NiftyNet_skull_segmentation/NiftyNet_projects/proyectos/pseudoCT_regression/modelsRIRE_EMBC",title = "Inference directory")
# else:
#     inference_dir = sys.argv[1]

inference_dir = "/mnt/D8D413E4D413C422/I3M/Proyectos/NiftyNet_skull_segmentation/NiftyNet_projects/proyectos/pseudoCT_regression/modelsRIRE_EMBC/M7_context_allFolds/inference"
reference_dir = "/mnt/D8D413E4D413C422/I3M/Proyectos/NiftyNet_skull_segmentation/NiftyNet_projects/Images/Training/ALL" #modify accordingly

data_param = {'CT': {'path_to_search': reference_dir,'spatial_window_size': (48,48,48),
            'filename_contains': '_ct_tra_reg masked', 'pixdim': (1.5,1.5,1.5), 'axcodes': ['L','P','S'],'interp_order': 3},
            'INF': {'path_to_search': inference_dir, 'spatial_window_size': (48,48,48),
            'filename_contains': '_niftynet_out','pixdim': (1.5,1.5,1.5), 'axcodes': ['L','P','S'],'interp_order': 3},
            'MASK': {'path_to_search': reference_dir,'spatial_window_size': (48,48,48),
            'filename_contains': '_headMask', 'pixdim': (1.5,1.5,1.5), 'axcodes': ['L','P','S'],'interp_order': 0},
            'BONE': {'path_to_search': reference_dir,'spatial_window_size': (48,48,48),
            'filename_contains': '_bone', 'pixdim': (1.5,1.5,1.5), 'axcodes': ['L','P','S'],'interp_order': 0},
            'TISSUE': {'path_to_search': reference_dir,'spatial_window_size': (48,48,48),
            'filename_contains': '_tissue', 'pixdim': (1.5,1.5,1.5), 'axcodes': ['L','P','S'],'interp_order': 0},
            'AIR': {'path_to_search': reference_dir,'spatial_window_size': (48,48,48),
            'filename_contains': '_air', 'pixdim': (1.5,1.5,1.5), 'axcodes': ['L','P','S'],'interp_order': 0},
             }

reader = ImageReader().initialise(data_param)

# reference_files = [f for f in os.listdir(reference_dir) if f.endswith('_ct_tra_reg masked.nii')]
# reference_files.sort()
# mask_files = [f for f in os.listdir(reference_dir) if f.endswith('_headMask.nii')]
# mask_files.sort()
inference_files = [f for f in os.listdir(inference_dir) if f.endswith('_niftynet_out.nii.gz')]
inference_files.sort()

with open(os.path.join(inference_dir, 'results.csv'), 'w') as csvfile:
    filewriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    filewriter.writerow(['id', 'msk_mae','bone_mae','tissue_mae','air_mae','msk_rmse','bone_rmse','tissue_rmse','air_rmse'])

for i,f in enumerate(inference_files):
#     cnt = 0
#     for r in reference_files:
        pos = f.find("_niftynet_out")
#         if i[:pos] == r[:pos]:
#             # referenceVol = sitk.ReadImage(os.path.join(reference_dir, r),sitk.sitkFloat32)
            # maskVol = sitk.ReadImage(os.path.join(reference_dir, mask_files[cnt]), sitk.sitkFloat32)
            # inferenceVol = sitk.ReadImage(os.path.join(inference_dir, i),sitk.sitkFloat32)

        _, vols, _ = reader(idx=i)
        ct = vols['CT']
        msk = vols['MASK']
        inf = vols['INF']
        bone = vols['BONE']
        tissue = vols['TISSUE']
        air = np.logical_and(vols['AIR'], msk).astype(int)

            # Calculate measures
            # ct=sitk.GetArrayFromImage(referenceVol)
            # inf=sitk.GetArrayFromImage(inferenceVol)
            # msk = sitk.GetArrayFromImage(maskVol)

        msk_mae = np.mean(np.abs(ct[msk > 0] - inf[msk > 0]))
        msk_rmse = np.sqrt(np.mean(np.square(ct[msk > 0] - inf[msk > 0])))

        bone_mae = np.mean(np.abs(ct[bone > 0] - inf[bone > 0]))
        bone_rmse = np.sqrt(np.mean(np.square(ct[bone > 0] - inf[bone > 0])))

        tissue_mae = np.mean(np.abs(ct[tissue > 0] - inf[tissue > 0]))
        tissue_rmse = np.sqrt(np.mean(np.square(ct[tissue > 0] - inf[tissue > 0])))

        air_mae = np.mean(np.abs(ct[air > 0] - inf[air > 0]))
        air_rmse = np.sqrt(np.mean(np.square(ct[air > 0] - inf[air > 0])))

        # mae = np.mean(np.abs(ct - inf))
        # rmse = np.sqrt(np.mean(np.square(ct - inf)))

        with open(os.path.join(inference_dir,'results.csv'), 'a') as csvfile:
            filewriter = csv.writer(csvfile, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)
            filewriter.writerow([f[:pos],msk_mae,bone_mae,tissue_mae,air_mae,msk_rmse,bone_rmse,tissue_rmse,air_rmse])
            #write results
            # break
        # cnt+=1

