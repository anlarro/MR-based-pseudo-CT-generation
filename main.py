import sys
niftynet_path = 'D:/I3M/Proyectos/Software_libraries/NiftyNet_source'
sys.path.insert(0,niftynet_path)


from niftynet.io.image_reader import ImageReader
from niftynet.layer.pad import PadLayer
from niftynet.layer.rand_rotation import RandomRotationLayer as Rotate
from niftynet.layer.rand_elastic_deform import RandomElasticDeformationLayer

import SimpleITK as sitk
import matplotlib.pyplot as plt


def plot_slices(vol,idx,slice='middle',figsize=(15,5)):
    f, axes = plt.subplots(1, 3, figsize=figsize)
    if slice=='middle':
        slice=vol['MR'].shape[2]//2
    axes[0].imshow(vol['MR'][:,:,slice,0,0].transpose(), cmap='gray')
    axes[0].set_title('MR-T1 %s' % idx)
    if slice=='middle':
        slice=vol['CT'].shape[2]//2
    axes[1].imshow(vol['CT'][:,:,slice,0,0].transpose(), cmap='gray')
    axes[1].set_title('CT %s' % idx)
    if slice=='middle':
        slice=vol['LABELS'].shape[2]//2
    axes[2].imshow(vol['LABELS'][:,:,slice,0,0].transpose(), cmap='gray')
    axes[2].set_title('Labels %s' % idx)
    for ax in axes:
        ax.set_axis_off()
    f.tight_layout()
    plt.show()

data_param = {'MR': {'path_to_search': 'D:/I3M/Proyectos/NiftyNet_skull_segmentation/Images/Training','spatial_window_size': (48,48,48),
            'filename_contains': ['_mr_T1','mhd'], 'pixdim': (1,1,1), 'axcodes': ['L','P','S'],'interp_order': 3},
            'CT': {'path_to_search': 'D:/I3M/Proyectos/NiftyNet_skull_segmentation/Images/Training', 'spatial_window_size': (48,48,48),
            'filename_contains': ['_ct masked','mhd'],'pixdim': (1,1,1), 'axcodes': ['L','P','S'],'interp_order': 3},
            'LABELS': {'path_to_search': 'D:/I3M/Proyectos/NiftyNet_skull_segmentation/Images/Training', 'spatial_window_size': (48,48,48),
            'filename_contains': ['_labels','mhd'],'pixdim': (1,1,1), 'axcodes': ['L','P','S'],'interp_order': 0}
              }

idx=0 #patient to show
reader = ImageReader().initialise(data_param)
#_, vol, _ = reader(idx=idx)
#plot_slices(vol,idx)


reader.add_preprocessing_layers(PadLayer(image_name=['MR','CT','LABELS'],border=(20,20,20),mode='constant'))
_, vol, _ = reader(idx=idx)
plot_slices(vol,idx,100)

rotation_layer = Rotate()
rotation_layer.init_uniform_angle([-10.0, 10.0])
reader.add_preprocessing_layers([rotation_layer])
_, vol, _ = reader(idx=idx)
plot_slices(vol,idx)

reader.add_preprocessing_layers(RandomElasticDeformationLayer(
    num_controlpoints=2,
    std_deformation_sigma=15,
    proportion_to_augment=1,
    spatial_rank=2))
_, vol, _ = reader(idx=idx)
plot_slices(vol,idx)