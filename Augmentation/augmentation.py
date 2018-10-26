"""
Script to show preprocessing and augmentation options of Niftynet
Normalization, padding and augmentation is performed
"""

import sys
niftynet_path = '/media/andres/Datos/I3M/Proyectos/NiftyNet_skull_segmentation/NiftyNet_projects'
sys.path.insert(0,niftynet_path)

import SimpleITK as sitk

from niftynet.io.image_reader import ImageReader

from niftynet.layer.mean_variance_normalisation import MeanVarNormalisationLayer
from niftynet.layer.pad import PadLayer

from niftynet.layer.rand_rotation import RandomRotationLayer as Rotate
from niftynet.layer.rand_spatial_scaling import RandomSpatialScalingLayer as Scale
from niftynet.layer.rand_elastic_deform import RandomElasticDeformationLayer as Deform
from niftynet.layer.rand_bias_field import RandomBiasFieldLayer as Bias
from niftynet.layer.binary_masking import BinaryMaskingLayer as Mask

from plot_slices import plot_slices

data_param = {'MR': {'path_to_search': '/media/andres/Datos/I3M/Proyectos/NiftyNet_skull_segmentation/Images/Training','spatial_window_size': (48,48,48),
            'filename_contains': ['_mr_T1','mhd'], 'pixdim': (1,1,1), 'axcodes': ['L','P','S'],'interp_order': 1},
            'CT': {'path_to_search': '/media/andres/Datos/I3M/Proyectos/NiftyNet_skull_segmentation/Images/Training', 'spatial_window_size': (48,48,48),
            'filename_contains': ['_ct masked','mhd'],'pixdim': (1,1,1), 'axcodes': ['L','P','S'],'interp_order': 1},
            'LABELS': {'path_to_search': '/media/andres/Datos/I3M/Proyectos/NiftyNet_skull_segmentation/Images/Training', 'spatial_window_size': (48,48,48),
            'filename_contains': ['_labels','mhd'],'pixdim': (1,1,1), 'axcodes': ['L','P','S'],'interp_order': 0}
              }

#Read images and plot
#Original images are already interpolated (order 1) to 1mm pixel size.
idx=0
reader = ImageReader().initialise(data_param)
_, vol, _ = reader(idx=idx)
plot_slices(vol['MR'],vol['CT'],vol['LABELS'],idx,title='Original images')
#sitk.WriteImage(sitk.GetImageFromArray(vol['MR'][:,:,:,0,0]),'./original.mhd') #save to disk
print(vol['MR'].shape)


##Normalization
binary_masking_func=Mask(type_str='mean_plus')
#mask=binary_masking_func(vol['MR'])
reader.add_preprocessing_layers(MeanVarNormalisationLayer(image_name = 'MR',binary_masking_func=binary_masking_func))
_, vol, _ = reader(idx=idx)
plot_slices(vol['MR'],vol['CT'],vol['LABELS'],idx,title='Normalized MR image')
#sitk.WriteImage(sitk.GetImageFromArray(vol['MR'][:,:,:,0,0]),'./whitenned.mhd')


# Use border as half of spatial_window_size, so the NN can learn more from the borders
#Use constant mode padding, I have modified niftynet.layers.pad to use constant_values=np.amin(image)
reader.add_preprocessing_layers(PadLayer(image_name=['MR','CT','LABELS'],border=(24,24,48),mode='constant'))
_, vol, _ = reader(idx=idx)
plot_slices(vol['MR'],vol['CT'],vol['LABELS'],idx,title='Padded images')
#sitk.WriteImage(sitk.GetImageFromArray(vol['CT'][:,:,:,0,0]),'./padded.mhd')
print(vol['MR'].shape)

#Add rotation layer
rotation_layer = Rotate()
rotation_layer.init_uniform_angle([-10.0, 10.0]) #randomly rotate between -10 and 10 degrees
reader.add_preprocessing_layers([rotation_layer])
_, vol, _ = reader(idx=idx)
plot_slices(vol['MR'],vol['CT'],vol['LABELS'],idx,title='Rotated images')
#sitk.WriteImage(sitk.GetImageFromArray(vol['CT'][:,:,:,0,0]),'./rotated.mhd')

#Add scaling layer
del(reader.preprocessors[2]) #Remove the previous preprocessing layer, layer 0 is the padding
reader.add_preprocessing_layers(Scale(min_percentage=-10,max_percentage=10))
_, vol, _ = reader(idx=idx)
plot_slices(vol['MR'],vol['CT'],vol['LABELS'],idx,title='Scaled images')
#sitk.WriteImage(sitk.GetImageFromArray(vol['CT'][:,:,:,0,0]),'./scaled.mhd')

#Add elastic layer
del(reader.preprocessors[2]) #Remove the previous preprocessing layer, layer 0 is the padding
reader.add_preprocessing_layers(Deform(
    num_controlpoints=4,
    std_deformation_sigma=10,
    proportion_to_augment=1,
    spatial_rank=3))
_, vol, _ = reader(idx=idx)
plot_slices(vol['MR'],vol['CT'],vol['LABELS'],idx,title='Deformed images')
#sitk.WriteImage(sitk.GetImageFromArray(vol['CT'][:,:,:,0,0]),'./deformed.mhd')

#Add bias layer
del(reader.preprocessors[2]) #Remove the previous preprocessing layer, layer 0 is the padding
bias_layer = Bias()
bias_layer.init_uniform_coeff([-50, 50])
reader.add_preprocessing_layers([bias_layer])
_, vol, _ = reader(idx=idx)
plot_slices(vol['MR'],vol['CT'],vol['LABELS'],idx,title='Images with random bias field')
#sitk.WriteImage(sitk.GetImageFromArray(vol['MR'][:,:,:,0,0]),'./bias.mhd')