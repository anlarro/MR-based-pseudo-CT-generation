#Script to visualize the MR, CT and labels slices contained in a folder
import os
import SimpleITK as sitk

from plot_slices import plot_slices

idx=0
vol_dir = "D:/I3M/Proyectos/NiftyNet_skull_segmentation/Images/Training" #modify accordingly

mr_files = [f for f in os.listdir(vol_dir) if f.endswith('_mr_T1.mhd')]
ct_files = [f for f in os.listdir(vol_dir) if f.endswith('_ct masked.mhd')]
label_files = [f for f in os.listdir(vol_dir) if f.endswith('_labels.mhd')]

mrVol = sitk.ReadImage(os.path.join(vol_dir, mr_files[idx]))
mr = sitk.GetArrayFromImage(mrVol).transpose()

ctVol = sitk.ReadImage(os.path.join(vol_dir, ct_files[idx]))
ct = sitk.GetArrayFromImage(ctVol).transpose()

labelsVol = sitk.ReadImage(os.path.join(vol_dir, label_files[idx]))
labels = sitk.GetArrayFromImage(labelsVol).transpose()

plot_slices(mr,ct,labels,idx,title='Original images')