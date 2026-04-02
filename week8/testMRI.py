import nibabel as nib
import matplotlib.pyplot as plt

# Load the NIfTI file
dataMRI = nib.load("someones_epi.nii")
data = dataMRI.get_fdata()

# Compute middle indices
mid_x = data.shape[0] // 2
mid_y = data.shape[1] // 2
mid_z = data.shape[2] // 2

# Extract middle slices
axial = data[:, :, mid_z]      # top-down view
coronal = data[:, mid_y, :]    # front view
sagittal = data[mid_x, :, :]   # side view

# Create subplots
fig, axes = plt.subplots(1, 3, figsize=(15, 5))

# Axial
axes[0].imshow(axial.T, cmap='gray', origin='lower')
axes[0].set_title("Axial (Z={})".format(mid_z))
axes[0].axis('off')

# Coronal
axes[1].imshow(coronal.T, cmap='gray', origin='lower')
axes[1].set_title("Coronal (Y={})".format(mid_y))
axes[1].axis('off')

# Sagittal
axes[2].imshow(sagittal.T, cmap='gray', origin='lower')
axes[2].set_title("Sagittal (X={})".format(mid_x))
axes[2].axis('off')

plt.tight_layout()
plt.show()