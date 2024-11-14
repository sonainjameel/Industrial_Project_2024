import numpy as np
from my_project.io_utils import load_envi_data

def preprocess_image(sample_cube, dark_reference_path, white_reference_path, reflectance_factor, x1, y1, x2, y2):
    # Load dark and white reference images
    darkref_cube, _, _ = load_envi_data(dark_reference_path)
    whiteref_cube, _, _ = load_envi_data(white_reference_path)
    
    mean_darkref = np.mean(darkref_cube, axis=0)
    mean_whiteref = np.mean(whiteref_cube, axis=0)
    
    replicated_darkref = np.tile(mean_darkref, (sample_cube.shape[0], 1, 1))
    replicated_whiteref = np.tile(mean_whiteref, (sample_cube.shape[0], 1, 1))
    
    # Add a small epsilon to the denominator to avoid division by zero
    epsilon = 1e-10
    reflectance_image = reflectance_factor * (sample_cube - replicated_darkref) / (replicated_whiteref - replicated_darkref + epsilon)
    reflectance_image = np.nan_to_num(reflectance_image, nan=0.0, posinf=0.0, neginf=0.0)
    
    # Crop the reflectance image
    reflectance_image_cropped = reflectance_image[y1:y2, x1:x2, :]
    
    return reflectance_image_cropped
