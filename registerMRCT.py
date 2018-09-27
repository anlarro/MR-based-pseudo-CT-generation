import os
import SimpleITK as sitk
from myshow import myshow,myshow3d
import matplotlib.pyplot as plt
import numpy as np

vol_dir = "D:/I3M/Proyectos/NiftyNet_skull_segmentation/Images/Training"


def load_volumes(vol_dir):
    for f_name in [f for f in os.listdir(vol_dir) if f.endswith('_mr_T1.mhd')]:
        itkvol = sitk.ReadImage(os.path.join(vol_dir,f_name))