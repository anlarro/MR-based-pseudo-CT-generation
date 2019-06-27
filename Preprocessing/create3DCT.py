##
#Reconstruct a 3D CT volume from low resolution 2D stacks (axial, sagital and coronal).
#The reconstruction is performed with NiftyMIC (https://github.com/gift-surg/NiftyMIC)
import os
import sys
from niftymic.application import reconstruct_volume_from_slices

def create3DCT(stacks, masks, res=1.5):
    path=os.path.split(stacks[0][0])[0]
    for n in range(len(stacks[0])):
        imageID = os.path.split(stacks[0][n])[1].split('_')[0]
        sys.argv = ['', '--filenames',
                    stacks[0][n],
                    stacks[1][n],
                    stacks[2][n],
                    '--filenames-masks',
                    masks[0][n],
                    masks[1][n],
                    masks[2][n],
                    '--isotropic-resolution', str(res),
                    '--output', os.path.join(path, imageID + '_ct.nii'),
                    '--extra-frame-target','0']
        reconstruct_volume_from_slices.main()