#Script to demonstrate the different sampling options in Niftynet
#Uniform, balanced and weighted sampler

import sys
niftynet_path = 'D:/I3M/Proyectos/Software_libraries/NiftyNet_source' #modify accordingly
sys.path.insert(0,niftynet_path)

from niftynet.io.image_reader import ImageReader
from niftynet.layer.pad import PadLayer
from niftynet.engine.sampler_uniform_v2 import UniformSampler
from niftynet.engine.sampler_balanced_v2 import BalancedSampler
from niftynet.engine.sampler_weighted_v2 import WeightedSampler

# Modify data_param according to the available image data
# For this example, read only one volume
images_dir = './Sampler/sample_images' #modify accordingly
data_param = {'MR': {'path_to_search': images_dir,'spatial_window_size': (48,48,48),
            'filename_contains': ['109_mr_T1','mhd'], 'pixdim': (1,1,1), 'axcodes': ['L','P','S'],'interp_order': 3},
            'sampler': {'path_to_search': images_dir, 'spatial_window_size': (48,48,48),
            'filename_contains': ['109_labels','mhd'],'pixdim': (1,1,1), 'axcodes': ['L','P','S'],'interp_order': 0},
              }
#This option is to read 2D slices
# data_param = {'MR': {'path_to_search': './sample_images','spatial_window_size': (48,48,41),
#             'filename_contains': ['middleSlice','mhd'], 'pixdim': (1,1), 'axcodes': ['L','P','S'],'interp_order': 3},
#             'sampler': {'path_to_search': './sample_images', 'spatial_window_size': (48,48,1),
#             'filename_contains': ['middleLabels','mhd'],'pixdim': (1,1), 'axcodes': ['L','P','S'],'interp_order': 0},
#               }

#Create image reader and add padding layer with 'constant' value 0
#This will ensure that samples are taken even at the beginning and ending slice
reader = ImageReader().initialise(data_param)
reader.add_preprocessing_layers(PadLayer(image_name=['MR','sampler'],border=(20,20,20),mode='constant'))
_, img, _ = reader(idx=0)

#Create samplers with window_size
weighted_sampler = WeightedSampler(
    reader, window_sizes=(48, 48, 48))

balanced_sampler = BalancedSampler(
    reader, window_sizes=(48, 48, 48))

uniform_sampler = UniformSampler(
    reader, window_sizes=(48, 48, 48))


#Generate N samples for each type
N=50
import tensorflow as tf
# adding the tensorflow tensors
next_window = weighted_sampler.pop_batch_op()
# run the tensors
with tf.Session() as sess:
    weighted_sampler.run_threads(sess) #initialise the iterator
    w_coords = []
    for _ in range(N):
        windows = sess.run(next_window)
        #print(windows.keys(), windows['MR_location'], windows['MR'].shape)
        w_coords.append(windows['MR_location'])


next_window = balanced_sampler.pop_batch_op()
# run the tensors
with tf.Session() as sess:
    balanced_sampler.run_threads(sess) #initialise the iterator
    b_coords = []
    for _ in range(N):
        windows = sess.run(next_window)
        #print(windows.keys(), windows['CT_location'], windows['CT'].shape)
        b_coords.append(windows['MR_location'])


next_window = uniform_sampler.pop_batch_op()
# run the tensors
with tf.Session() as sess:
    uniform_sampler.run_threads(sess) #initialise the iterator
    u_coords = []
    for _ in range(N):
        windows = sess.run(next_window)
        # print(windows.keys(), windows['CT_location'], windows['CT'].shape)
        u_coords.append(windows['MR_location'])

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.collections import PatchCollection

#Function to plot the results
def myshow(slice=0,figsize=(15,3)):
    f,ax = plt.subplots(1,4,figsize=figsize)
    #print(img['MR'].shape)
    #plt.subplot(1,2,1)
    ax[0].imshow(img['MR'][:,:,slice,0,0].transpose(),cmap='gray')
    #plt.subplot(1,2,2)
    ax[1].imshow(img['sampler'][:,:,slice,0,0].transpose())

    # show uniform sampled windows
    all_patch = []
    for win in np.concatenate(u_coords, axis=0):
        if slice>=win[3] and slice<=win[6]:
            patch = patches.Rectangle(
                (win[1], win[2]),
                win[4]-win[1], win[5]-win[2], linewidth=1)
            all_patch.append(patch)
    all_pc = PatchCollection(
        all_patch, alpha=0.5, edgecolor='r', facecolor='r')
    ax[1].add_collection(all_pc)
    ax[1].set_title('Uniform',fontsize=16)
    #plt.show()

    #plt.subplot(1,2,2)
    ax[2].imshow(img['sampler'][:,:,slice,0,0].transpose())

    # show balanced sampled windows
    all_patch = []
    for win in np.concatenate(b_coords, axis=0):
        if slice>=win[3] and slice<=win[6]:
            patch = patches.Rectangle(
                (win[1], win[2]),
                win[4]-win[1], win[5]-win[2], linewidth=1)
            all_patch.append(patch)
    all_pc = PatchCollection(
        all_patch, alpha=0.5, edgecolor='r', facecolor='r')
    ax[2].add_collection(all_pc)
    ax[2].set_title('Balanced',fontsize=16)
    #plt.show()

    #plt.subplot(1,2,2)
    ax[3].imshow(img['sampler'][:,:,slice,0,0].transpose())

    # show weighted sampled windows
    all_patch = []
    for win in np.concatenate(w_coords, axis=0):
        if slice>=win[3] and slice<=win[6]:
            patch = patches.Rectangle(
                (win[1], win[2]),
                win[4]-win[1], win[5]-win[2], linewidth=1)
            all_patch.append(patch)
    all_pc = PatchCollection(
        all_patch, alpha=0.5, edgecolor='r', facecolor='r')
    ax[3].add_collection(all_pc)
    ax[3].set_title('Weighted',fontsize=16)
    plt.show()

#save 3D mask with patches
import os
import SimpleITK as sitk

maskVolume=np.zeros(img['MR'].shape[:3])
for win in np.concatenate(w_coords, axis=0):
    maskVolume[win[1]:win[4],win[2]:win[5],win[3]:win[6]]=1

sitk.WriteImage(sitk.GetImageFromArray(img['sampler'][:,:,:,0,0]),os.path.join(images_dir,'patient_109_patchImage.mhd'))
sitk.WriteImage(sitk.GetImageFromArray(maskVolume),os.path.join(images_dir,'patient_109_patchMask.mhd'))

myshow(slice=20) #bottom slice
myshow(slice=img['MR'].shape[2]//2) #middle slice
myshow(slice=img['MR'].shape[2]-21) #top slice