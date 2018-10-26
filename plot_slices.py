import matplotlib.pyplot as plt

def plot_slices(mr,ct,labels,idx,title='',slice='middle',figsize=(15,3)):
    if slice=='middle':
        slice=mr.shape[2]//2

    f, axes = plt.subplots(1, 3, figsize=figsize)
    mr = mr.reshape(mr.shape[:3])
    axes[0].imshow(mr[:,:,slice].transpose(), cmap='gray')
    axes[0].set_title('MR-T1',fontsize=16)

    ct = ct.reshape(ct.shape[:3])
    axes[1].imshow(ct[:,:,slice].transpose(), cmap='gray')
    axes[1].set_title('CT',fontsize=16)

    labels = labels.reshape(labels.shape[:3])
    axes[2].imshow(labels[:,:,slice].transpose())
    axes[2].set_title('Labels',fontsize=16)
    for ax in axes:
        ax.set_axis_off()
    f.tight_layout()

    f.suptitle(title + ' (idx %s)' %idx,fontsize=20)  # or plt.suptitle('Main title')
    plt.show()