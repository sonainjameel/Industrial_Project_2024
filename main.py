import argparse
import yaml
from pathlib import Path
from my_project.io_utils import load_envi_data, save_envi_data
from my_project.preprocessing import preprocess_image
from my_project.binning import spatial_binning, spectral_binning, create_rgb_image
from my_project.interactive_visualization import display_interactive_spectral_plot  # Import the new function
import matplotlib.pyplot as plt

def main(config_path):
    # Load configuration
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)

    # Load and preprocess data
    header_file_path = Path(config['paths']['header_file'])
    sample_cube, wavelengths, header = load_envi_data(header_file_path)
    
    # Preprocess
    reflectance_factor = eval(config['parameters']['reflectance_factor'])  
    x1, y1, x2, y2 = config['crop_params']['x1'], config['crop_params']['y1'], config['crop_params']['x2'], config['crop_params']['y2']
    reflectance_image_cropped = preprocess_image(
        sample_cube, 
        config['paths']['dark_reference'], 
        config['paths']['white_reference'], 
        reflectance_factor, 
        x1, y1, x2, y2
    )
    
    # Spatial and Spectral Binning
    spatial_binned_image = spatial_binning(reflectance_image_cropped, config['parameters']['spatial_bin_size'])
    spectral_binned_image, binned_wavelengths = spectral_binning(reflectance_image_cropped, config['parameters']['spectral_bin_size'], wavelengths)


    # Save the binned data
    output_dir = Path(config['paths']['output_dir'])
    output_dir.mkdir(parents=True, exist_ok=True)
    spatial_output_file = output_dir / "spatial_binned_image.hdr"
    spectral_output_file = output_dir / "spectral_binned_image.hdr"
    save_envi_data(spatial_output_file, header, spatial_binned_image, wavelengths)
    save_envi_data(spectral_output_file, header, spectral_binned_image, wavelengths)

    # Display the interactive plot for the spectrally binned image
    spectral_binned_path = Path(config['paths']['spectral_binned_file'])  # Load from config
    target_wavelengths = config['parameters']['target_wavelengths']
    display_interactive_spectral_plot(spectral_binned_path, target_wavelengths, binned_wavelengths)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the industrial-level project.")
    parser.add_argument("config_path", type=str, help="Path to the configuration file")
    args = parser.parse_args()
    
    main(args.config_path)
