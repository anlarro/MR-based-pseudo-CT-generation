import os
import sys

import SimpleITK as sitk
import numpy as np

import tkinter as tk
from tkinter import filedialog

import csv

import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable

if len(sys.argv)==1:
    root = tk.Tk()
    root.withdraw()
    inference_dir1 = filedialog.askdirectory(initialdir = "/mnt/D8D413E4D413C422/I3M/Proyectos/NiftyNet_skull_segmentation/NiftyNet_projects/proyectos/pseudoCT_regression/modelsRIRE_EMBC",title = "Inference directory 1")
    inference_dir2 = filedialog.askdirectory(initialdir = "/mnt/D8D413E4D413C422/I3M/Proyectos/NiftyNet_skull_segmentation/NiftyNet_projects/proyectos/pseudoCT_regression/modelsRIRE_EMBC",title = "Inference directory 2")
else:
    inference_dir1 = sys.argv[1]
    inference_dir2 = sys.argv[2]

avg_dir = os.path.join(os.path.dirname(inference_dir1),'avg')

inference_files1 = [f for f in os.listdir(inference_dir1) if f.endswith('_niftynet_out.nii.gz')]
inference_files2 = [f for f in os.listdir(inference_dir2) if f.endswith('_niftynet_out.nii.gz')]

for i in inference_files1:
    for r in inference_files2:
        pos = i.find("_niftynet_out")
        if i[:pos] == r[:pos]:
            inferenceVol1 = sitk.ReadImage(os.path.join(inference_dir1, r),sitk.sitkFloat32)

            inferenceVol2 = sitk.ReadImage(os.path.join(inference_dir2, i),sitk.sitkFloat32)

            # Generate error map
            avg = np.mean([sitk.GetArrayFromImage(inferenceVol1),sitk.GetArrayFromImage(inferenceVol2)],axis=0)
            avgVol = sitk.GetImageFromArray(avg)
            for k in inferenceVol1.GetMetaDataKeys():
                avgVol.SetMetaData(k,inferenceVol1.GetMetaData(k))

            if not os.path.exists(avg_dir):
                avg_dir,os.mkdir(avg_dir)
            sitk.WriteImage(avgVol, os.path.join(avg_dir, i[:pos] + '_avg.nii.gz'))
            break

            #Hacer el average con sitk porque o sino sale mal.