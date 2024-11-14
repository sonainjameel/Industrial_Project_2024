from pathlib import Path
from my_project.envi2 import read_envi as envi2_read_envi, write_envi as envi2_write_envi

def load_envi_data(header_file):
    # Ensure header_file is a Path object
    header_file = Path(header_file)
    sample_cube, wavelengths, header = envi2_read_envi(header_file=header_file)
    return sample_cube, wavelengths, header

def save_envi_data(output_file, header, image_data, wavelengths):
    output_file = Path(output_file)
    header['bands'] = image_data.shape[2]
    header['wavelengths'] = wavelengths.tolist()
    envi2_write_envi(output_file, header, image_data, wavelengths)  # Added wavelengths here
