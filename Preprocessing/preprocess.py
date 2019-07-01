import os
import sys

import SimpleITK as sitk
from Preprocessing.createHeadMask import createHeadMask
from Preprocessing.create3DCT import create3DCT
from Registration.register import register

import math

import tkinter as tk
from tkinter import filedialog

def main():
    #Directory with images CT, MRT1, MRT2, FLAIR
    if len(sys.argv)==1:
        root = tk.Tk()
        root.withdraw()
        path = filedialog.askdirectory(initialdir = '/mnt/D8D413E4D413C422/I3M/Imagenes/')
    else:
        path = sys.argv[1]

#    my_images = images()
#    images.getModalities()
#    images.getPatients()
#    images.createSplits()

    ct_cor_files = [f for f in os.listdir(path) if f.endswith('_ct_cor.nii')]
    ct_cor_files.sort()
    ct_sag_files = [f for f in os.listdir(path) if f.endswith('_ct_sag.nii')]
    ct_sag_files.sort()
    ct_tra_files = [f for f in os.listdir(path) if f.endswith('_ct_tra.nii')]
    ct_tra_files.sort()

    #create headMasks on 2D CT stacks
    for n,file in enumerate(ct_cor_files):
        ct_cor_mask = createHeadMask(sitk.ReadImage(os.path.join(path,ct_cor_files[n])),direction="cor")
        ct_sag_mask = createHeadMask(sitk.ReadImage(os.path.join(path,ct_sag_files[n])),direction="sag")
        ct_tra_mask = createHeadMask(sitk.ReadImage(os.path.join(path,ct_tra_files[n])),direction="tra")

        sitk.WriteImage(ct_cor_mask, os.path.join(path, ct_cor_files[n].split('.')[0] + '_mask.nii'))
        sitk.WriteImage(ct_sag_mask, os.path.join(path, ct_sag_files[n].split('.')[0] + '_mask.nii'))
        sitk.WriteImage(ct_tra_mask, os.path.join(path, ct_tra_files[n].split('.')[0] + '_mask.nii'))

    #create 3D CT from 2D stacks using NiftyMic
    ct_cor_masks = [f for f in os.listdir(path) if f.endswith('_ct_cor_mask.nii')]
    ct_cor_masks.sort()
    ct_sag_masks = [f for f in os.listdir(path) if f.endswith('_ct_sag_mask.nii')]
    ct_sag_masks.sort()
    ct_tra_masks = [f for f in os.listdir(path) if f.endswith('_ct_tra_mask.nii')]
    ct_tra_masks.sort()

    create3DCT([[os.path.join(path,file) for file in ct_cor_files],
                [os.path.join(path, file) for file in ct_sag_files],
                [os.path.join(path, file) for file in ct_tra_files]],
               [[os.path.join(path,file) for file in ct_cor_masks],
                [os.path.join(path, file) for file in ct_sag_masks],
                [os.path.join(path, file) for file in ct_tra_masks]])


    #create headMasks on 3D CT volumes
    ct_files = [f for f in os.listdir(path) if f.endswith('_ct.nii')]
    ct_files.sort()
    for n,file in enumerate(ct_files):
        ct_mask = createHeadMask(sitk.ReadImage(os.path.join(path,ct_files[n])))
        sitk.WriteImage(ct_mask, os.path.join(path, ct_files[n].split('.')[0] + '_mask.nii'))

    #Register volumes mrT1,mrT2,Flair (moving) to 3DCT(fixed)
    ct_files = sorted([os.path.join(path,'{}'.format(i)) for i in os.listdir(path) if i.endswith('_ct.nii')])
    ct_masks = sorted([os.path.join(path,'{}'.format(i)) for i in os.listdir(path) if i.endswith('_ct_mask.nii')])
    mrT1_files = sorted([os.path.join(path,'{}'.format(i)) for i in os.listdir(path) if i.endswith('_mrT1.nii')])
    mrT2_files = sorted([os.path.join(path,'{}'.format(i)) for i in os.listdir(path) if i.endswith('_mrT2.nii')])
    flair_files = sorted([os.path.join(path,'{}'.format(i)) for i in os.listdir(path) if i.endswith('_flair.nii')])

    for i,_ in enumerate(ct_files):
        _, file = os.path.split(ct_files[i])
        patientID = file.split('_')[0]

        ct = sitk.ReadImage(ct_files[i])
        ct_mask = sitk.ReadImage(ct_masks[i])
        mrT1 = sitk.ReadImage(mrT1_files[i])
        mrT2 = sitk.ReadImage(mrT2_files[i])
        flair = sitk.ReadImage(flair_files[i])

        sitk.WriteImage(sitk.Mask(ct,ct_mask,-1000),os.path.join(path,patientID+'_ct_reg.nii'))

        result = register(ct, mrT1, ct_mask) #We save the masked, Bias corrected volume
        sitk.WriteImage(sitk.Mask(sitk.N4BiasFieldCorrection(result,ct_mask),ct_mask,0), os.path.join(path,patientID+'_mrT1_reg.nii'))

        result = register(ct, mrT2, ct_mask)
        sitk.WriteImage(sitk.Mask(sitk.N4BiasFieldCorrection(result,ct_mask),ct_mask,0), os.path.join(path,patientID+'_mrT2_reg.nii'))

        result = register(ct, flair, ct_mask)
        sitk.WriteImage(sitk.Mask(sitk.N4BiasFieldCorrection(result,ct_mask),ct_mask,0), os.path.join(path,patientID+'_flair_reg.nii'))


    #Create masks above nasal cavities, we will use these masks for evaluation of the results.
    for file in ct_masks:
        ct_mask = sitk.ReadImage(os.path.join(path,file))
        half_position = math.floor(ct_mask.GetSize()[1]*0.7)
        blank_slice = sitk.Image([ct_mask.GetSize()[0],half_position,ct_mask.GetSize()[2]],sitk.sitkUInt8)
        half_mask = sitk.Paste(ct_mask, blank_slice, blank_slice.GetSize(), destinationIndex=[0, half_position, 0])
        sitk.WriteImage(half_mask, os.path.join(path, file.split('.')[0] + 'Half.nii'))

    """Create air, bone and tissue masks"""
    for file in ct_files:
        ct = sitk.ReadImage(os.path.join(path,file))
        filter = sitk.StatisticsImageFilter()
        filter.Execute(ct)

        air = sitk.BinaryThreshold(ct,filter.GetMinimum(),-500) #background
        sitk.WriteImage(air, os.path.join(path, file.split('.')[0] + '_air.nii'))

        bone = sitk.BinaryThreshold(ct, 300, filter.GetMaximum()) #bone
        sitk.WriteImage(bone, os.path.join(path, file.split('.')[0] + '_bone.nii'))

        tissue = sitk.BinaryThreshold(ct, -500, 300) #tissue
        sitk.WriteImage(tissue, os.path.join(path, file.split('.')[0] + '_tissue.nii'))


if __name__ == '__main__':
    main()