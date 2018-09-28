import matplotlib.pyplot as plt

def plot_slices(mr,ct,labels,idx,slice='middle',figsize=(15,5)):
    if slice=='middle':
        slice=mr.shape[2]//2

    f, axes = plt.subplots(1, 3, figsize=figsize)
    mr = mr.reshape(mr.shape[:3])
    axes[0].imshow(mr[:,:,slice].transpose(), cmap='gray')
    axes[0].set_title('MR-T1 (idx %s)' % idx)

    ct = ct.reshape(ct.shape[:3])
    axes[1].imshow(ct[:,:,slice].transpose(), cmap='gray')
    axes[1].set_title('CT (idx %s)' % idx)

    labels = labels.reshape(labels.shape[:3])
    axes[2].imshow(labels[:,:,slice].transpose())
    axes[2].set_title('Labels (idx %s)' % idx)
    for ax in axes:
        ax.set_axis_off()
    f.tight_layout()
    plt.show()