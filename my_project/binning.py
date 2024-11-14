import numpy as np

def spatial_binning(image, bin_size):
    h, w, bands = image.shape
    new_h, new_w = (h // bin_size) * bin_size, (w // bin_size) * bin_size
    cropped_image = image[:new_h, :new_w, :]
    binned_image = cropped_image.reshape(new_h // bin_size, bin_size, new_w // bin_size, bin_size, bands).sum(axis=(1, 3))
    return binned_image

def spectral_binning(image, bin_size, wavelengths):
    h, w, bands = image.shape
    new_bands = (bands // bin_size) * bin_size
    cropped_image = image[:, :, :new_bands]
    binned_image = cropped_image.reshape(h, w, new_bands // bin_size, bin_size).sum(axis=-1)
    
    # Bin wavelengths to match the spectral reduction
    binned_wavelengths = wavelengths[:new_bands].reshape(-1, bin_size).mean(axis=1)
    
    return binned_image, binned_wavelengths

def find_closest_wavelengths(target_wavelengths, wavelength_array):
    indices = []
    for tw in target_wavelengths:
        idx = (np.abs(wavelength_array - tw)).argmin()
        indices.append(idx)
    return indices

def create_rgb_image(binned_image, wavelengths, target_wavelengths):
    closest_indices = find_closest_wavelengths(target_wavelengths, wavelengths)
    R_channel = binned_image[:, :, closest_indices[0]]
    G_channel = binned_image[:, :, closest_indices[1]]
    B_channel = binned_image[:, :, closest_indices[2]]
    
    RGB_image = np.stack([R_channel, G_channel, B_channel], axis=2)
    RGB_image = (RGB_image - np.min(RGB_image)) / (np.max(RGB_image) - np.min(RGB_image))
    
    return RGB_image
