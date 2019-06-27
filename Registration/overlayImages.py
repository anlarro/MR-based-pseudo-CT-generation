import numpy as np
import matplotlib.pyplot as plt
import SimpleITK as sitk


def overlay(img1, img2, title=None, interpolation=None, sizeThreshold=128):
    """
    Description
    -----------
    Displays an overlay of two 2D images using matplotlib.pyplot.imshow().

    Args
    ----
    img1 : np.array or sitk.Image
        image to be displayed
    img2 : np.array or sitk.Image
        image to be displayed

    Optional
    --------
    title : string
        string used as image title
        (default None)
    interpolation : string
        desired option for interpolation among matplotlib.pyplot.imshow options
        (default nearest)
    sizeThreshold : integer
        size under which interpolation is automatically set to 'nearest' if all
        dimensions of img1 and img2 are below
        (default 128)
    """
    # Check for type of images and convert to np.array
    if isinstance(img1, sitk.Image):
        img1 = sitk.GetArrayFromImage(img1)
    if isinstance(img2, sitk.Image):
        img2 = sitk.GetArrayFromImage(img2)
    if type(img1) is not type(img2) is not np.ndarray:
        raise NotImplementedError('Please provide images as np.array or '
                                  'sitk.Image.')
    # Check for size of images
    if not img1.ndim == img2.ndim == 2:
        raise NotImplementedError('Only supports 2D images.')

    if interpolation:
        plt.imshow(img1, cmap='summer', interpolation=interpolation)
        plt.imshow(img2, cmap='autumn', alpha=0.5, interpolation=interpolation)
    elif max(max(img1.shape), max(img2.shape)) > sizeThreshold:
        plt.imshow(img1, cmap='summer')
        plt.imshow(img2, cmap='autumn', alpha=0.5)
    else:
        plt.imshow(img1, cmap='summer', interpolation='nearest')
        plt.imshow(img2, cmap='autumn', alpha=0.5, interpolation='nearest')
    plt.title(title)
    plt.axis('off')
    plt.show()