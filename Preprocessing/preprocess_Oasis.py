import os
import sys

import SimpleITK as sitk
from Registration.register import register
from Preprocessing.resampleVolume import resampleVolume
from Preprocessing.createHeadMask import createHeadMask

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
    files = [[] for _ in range(len(modalities))]
    mask = [[] for _ in range(len(modalities))]
    results = [[] for _ in range(len(modalities))]

    for m in range(len(modalities)):
        files[m] = sorted(os.listdir(os.path.join(path,modalities[m])))

    for i,_ in enumerate(files[0]):
        patientID = files[0][i].split('_')[0]

        results[0].append(resampleVolume(sitk.ReadImage(os.path.join(path, modalities[0], files[0][i]),sitk.sitkFloat32), [1.5, 1.5, 1.5]))
        mask[0].append(createHeadMask(results[0][i],direction="tra",lowerThreshold=30))
        headMask = mask[0][i]

        for m in range(1,len(modalities)): #register the rest of modalities to modality 0
            results[m].append(register(results[0][i],sitk.ReadImage(os.path.join(path,modalities[m],files[m][i]), sitk.sitkFloat32))) #We save the bias corrected volume
            mask[m].append(createHeadMask(results[m][i],direction="tra",lowerThreshold=30))
            headMask &= mask[m][i]  #create common headMask

        #Save results
        for m,_ in enumerate(modalities):
            sitk.WriteImage(sitk.Mask(sitk.N4BiasFieldCorrection(results[m][i], headMask), headMask, 0),
                        os.path.join(path, modalities[m], patientID + '_' + modalities[m] + '_reg.nii.gz'))


if __name__ == '__main__':
    main()

