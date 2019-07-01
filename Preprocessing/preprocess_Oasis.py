import os
import sys

import SimpleITK as sitk
from Registration.register import register
from Preprocessing.resampleVolume import resampleVolume

import tkinter as tk
from tkinter import filedialog

def main():
    #Directory with
    if len(sys.argv)==1:
        root = tk.Tk()
        root.withdraw()
        path = filedialog.askdirectory(initialdir = '/mnt/D8D413E4D413C422/I3M/Imagenes/')
    else:
        path = sys.argv[1]

    modalities = sorted(os.listdir(path))

    #Register volumes (moving) to input_modalities[0] (fixed)
    files = {}
    for m in range(len(modalities)):
        files[m] = sorted(os.listdir(os.path.join(path,modalities[m])))

    for i,_ in enumerate(files[0]):
        patientID = files[0][i].split('_')[0]

        fixed_volume = resampleVolume(sitk.ReadImage(os.path.join(path, modalities[0], files[0][i]),sitk.sitkFloat32), [1.5, 1.5, 1.5])
        sitk.WriteImage(sitk.N4BiasFieldCorrection(fixed_volume), os.path.join(path, modalities[0], patientID+'_'+modalities[0]+'_reg.nii.gz'))

        for m,_ in enumerate(modalities):
            result = register(fixed_volume,sitk.ReadImage(os.path.join(path,modalities[m],files[m][i]), sitk.sitkFloat32)) #We save the bias corrected volume
            sitk.WriteImage(sitk.N4BiasFieldCorrection(result), os.path.join(path,modalities[m],patientID+'_'+modalities[m]+'_reg.nii.gz'))

if __name__ == '__main__':
    main()