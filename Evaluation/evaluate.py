"""
Script to evaluate the regression results by computing different measures
"""

import os
import sys

import SimpleITK as sitk
import numpy as np

import tkinter as tk
from tkinter import filedialog

import csv

import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable

reference_dir = "/mnt/D8D413E4D413C422/I3M/Proyectos/NiftyNet_skull_segmentation/Images/Training/RIRE" #modify accordingly

if len(sys.argv)==1:
    root = tk.Tk()
    root.withdraw()
    inference_dir = filedialog.askdirectory(initialdir = "/mnt/D8D413E4D413C422/I3M/Proyectos/NiftyNet_skull_segmentation/NiftyNet_projects/proyectos/pseudoCT_regression/models_onlyRIRE/best_models",title = "Inference directory")
else:
    inference_dir = sys.argv[1]


reference_files = [f for f in os.listdir(reference_dir) if f.endswith('_ct_tra_reg masked.nii')]
mask_files = [f for f in os.listdir(reference_dir) if f.endswith('_headMask.nii')]
inference_files = [f for f in os.listdir(inference_dir) if f.endswith('_niftynet_out.nii.gz')]

with open(os.path.join(inference_dir, 'results.csv'), 'w') as csvfile:
    filewriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    filewriter.writerow(['id', 'mae', 'rmse'])

for i in inference_files:
    cnt = 0
    for r in reference_files:
        pos = i.find("_niftynet_out")
        if i[:pos] == r[:pos]:
            referenceVol = sitk.ReadImage(os.path.join(reference_dir, r),sitk.sitkFloat32)
            maskVol = sitk.ReadImage(os.path.join(reference_dir, mask_files[cnt]), sitk.sitkFloat32)
            inferenceVol = sitk.ReadImage(os.path.join(inference_dir, i),sitk.sitkFloat32)

            # Calculate measures
            ct=sitk.GetArrayFromImage(referenceVol)
            mri=sitk.GetArrayFromImage(inferenceVol)
            msk = sitk.GetArrayFromImage(maskVol)

            mae = np.mean(np.abs(ct - mri))
            rmse = np.sqrt(np.mean(np.square(ct-mri)))


          #  sum(abs(ct_masked(:)-mri_masked(:))) / sum(mask(:));
          #  mse = sum((ct_masked(:) - mri_masked(:)).^ 2) / sum(mask(:));

            with open(os.path.join(inference_dir,'results.csv'), 'a') as csvfile:
                filewriter = csv.writer(csvfile, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)
                filewriter.writerow([i[:pos],mae,rmse])
            #write results
            break
        cnt+=1

