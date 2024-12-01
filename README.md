
# Industrial Project Part 1: Processing and Analyzing Spectral Data 

> **_⚠️ Note:_**  
> **_This code has been tested on Python versions 3.10.5 and 3.12.4._**  

This project is designed for processing and analyzing multispectral image data. Using Python, it implements interactive visualization, data binning, preprocessing, and spectral transformations to enhance understanding of spectral properties and derivatives. 

## Features

- **Spectral Image Preprocessing**: Converts raw spectral data to reflectance images and allows for cropping and binning.
- **Data Binning**: Includes spatial and spectral binning to reduce data dimensions while preserving essential spectral features.
- **Interactive Visualization**: Provides an RGB visualization and an interactive spectral plot for a selected region, with options to view normalized spectra and its first and second derivatives.
- **Configurable Pipeline**: Leverages a `config.yaml` file for flexible input paths, parameters, and settings, enabling easy customization for different datasets.

## Installation

### Requirements

- Python 3.8 or higher
- The following Python libraries:
    - `numpy`
    - `matplotlib`
    - `PyYAML`
    - `opencv-python`
    - `scikit-learn`

### Setup Instructions

1. Clone the repository to your local machine:
   ```bash
   git clone https://github.com/sonainjameel/Industrial_Project_2024.git
   cd Industrial_Project_2024
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Ensure you have the correct input data and configurations as specified in the `config.yaml` file.

## Configuration

The project relies on a `config.yaml` file for setting input paths and processing parameters. Here’s an example of what this file might look like:

```yaml
paths:
  header_file: "/path/to/header/file.hdr"
  dark_reference: "/path/to/dark_reference.hdr"
  white_reference: "/path/to/white_reference.hdr"
  output_dir: "/path/to/output/directory"
  spectral_binned_file: "/path/to/spectral_binned_image.hdr"

parameters:
  spatial_bin_size: 2
  spectral_bin_size: 2
  target_wavelengths: [1496.9, 1301.1, 1104.8]
  reflectance_factor: "1"# for reference image; "0.448 * 0.95" for charred wood samples

crop_params:
  x1: 20
  y1: 950
  x2: 300
  y2: 1220
```

## Usage

To run the main script and execute the pipeline:

```bash
python3 main.py config.yaml
```

This command will process the specified hyperspectral image, perform data binning, and launch an interactive visualization window.

## Project Structure

```
Industrial_Project_2024/
├── config.yaml                      # Configuration file for paths and parameters
├── main.py                          # Main script to run the pipeline
├── requirements.txt                 # Required libraries
└── my_project/                      # Core project folder
    ├── __init__.py                  # Initialize package
    ├── io_utils.py                  # I/O functions for loading and saving data
    ├── preprocessing.py             # Functions for preprocessing images
    ├── binning.py                   # Functions for spatial and spectral binning
    └── interactive_visualization.py # Interactive visualization functions
```

### Key Modules

- **`io_utils.py`**: Handles loading and saving of spectral image data.
- **`preprocessing.py`**: Contains image preprocessing functions, including normalization and reflectance conversion.
- **`binning.py`**: Implements spatial and spectral binning to reduce data dimensions.
- **`interactive_visualization.py`**: Provides an interactive visualization interface, allowing users to view an RGB image and explore spectral data across selected regions.

## Interactive Visualization

When the interactive visualization window opens:
1. Click on any region of the RGB image to display spectral data for a 100x100 pixel region centered at that point.
2. The interactive plots include:
    - **Mean Spectrum**: Displays the average reflectance.
    - **Standard Normal Spectrum**: Displays a normalized version of the spectrum.
    - **First Derivative**: Displays the first derivative of the spectrum, highlighting changes across wavelengths.
    - **Second Derivative**: Displays the second derivative of the spectrum, indicating areas of rapid spectral change.


## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Commit your changes with clear descriptions.
4. Submit a pull request for review.

## License

This project is licensed under the MIT License.

## Acknowledgements

Group A (Sonain, Kasem, and Turab) especially thanks Joni Hyttinen and Prof. Markku Keinänen for their support in developing this project.
