from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from my_project.io_utils import load_envi_data  # To load the binned file

def find_closest_wavelengths(target_wavelengths, wavelength_array):
    indices = []
    for tw in target_wavelengths:
        idx = (np.abs(wavelength_array - tw)).argmin()
        indices.append(idx)
    return indices

def display_interactive_spectral_plot(spectral_binned_path, target_wavelengths, binned_wavelengths):
    # Load the spectrally binned image cube
    sample_cube, _, _ = load_envi_data(spectral_binned_path)
    
    # Find the closest wavelengths for the RGB channels using the binned wavelengths
    closest_indices = find_closest_wavelengths(target_wavelengths, binned_wavelengths)

    # Extract R, G, B channels and create the RGB image
    R_channel = sample_cube[:, :, closest_indices[0]]
    G_channel = sample_cube[:, :, closest_indices[1]]
    B_channel = sample_cube[:, :, closest_indices[2]]
    RGB_image = np.stack([R_channel, G_channel, B_channel], axis=2)
    RGB_image = (RGB_image - np.min(RGB_image)) / (np.max(RGB_image) - np.min(RGB_image))

    # Set up the figure with a 2x3 grid for the plots
    fig, axes = plt.subplots(2, 3, figsize=(18, 8))
    image_ax, spectral_ax = axes[0, 0], axes[0, 1]
    normalized_ax, first_deriv_ax, second_deriv_ax = axes[0, 2], axes[1, 1], axes[1, 2]
    
    # Clear any unnecessary axes initially
    axes[1, 0].axis('off')  # Clear the empty plot if not used

    # Display the RGB image initially
    image_ax.imshow(RGB_image)
    image_ax.set_title('RGB Image')
    image_ax.axis('off')

    # Variable to store the selection rectangle
    rect = None

    # Function to standardize, compute first derivative, and second derivative of the spectrum
    def process_spectrum(reflectance_spectrum):
        # Standard Normal version (mean=0, std=1)
        normalized_spectrum = (reflectance_spectrum - np.mean(reflectance_spectrum)) / np.std(reflectance_spectrum)
        
        # First derivative of the spectrum
        first_derivative = np.gradient(reflectance_spectrum, binned_wavelengths)
        
        # Second derivative of the spectrum
        second_derivative = np.gradient(first_derivative, binned_wavelengths)
        
        return normalized_spectrum, first_derivative, second_derivative

    # Function to update the spectral plots for a 100x100 region
    def update_spectral_plot(x, y):
        nonlocal rect  # Use nonlocal to access the rect variable
        
        # Remove previous rectangle if it exists
        if rect is not None:
            rect.remove()
        
        # Ensure the rectangle remains within bounds
        x_start = max(0, min(x - 50, sample_cube.shape[1] - 100))
        y_start = max(0, min(y - 50, sample_cube.shape[0] - 100))
        
        # Draw a new rectangle for the selected region
        rect = Rectangle((x_start, y_start), 100, 100, linewidth=2, edgecolor='red', facecolor='none')
        image_ax.add_patch(rect)
        
        # Calculate the average spectral reflectance for the selected region
        reflectance_spectrum = np.mean(sample_cube[y_start:y_start+100, x_start:x_start+100, :], axis=(0, 1))
        
        # Compute processed spectra
        normalized_spectrum, first_derivative, second_derivative = process_spectrum(reflectance_spectrum)
        
        # Update the original spectral plot
        spectral_ax.clear()
        spectral_ax.plot(binned_wavelengths, reflectance_spectrum)
        # Add vertical lines at wavelengths 1700 and 2300
        spectral_ax.axvline(x=1700, color='blue', linestyle='--', linewidth=1.5)#, label="1700 nm")
        spectral_ax.axvline(x=1750, color='blue', linestyle='--', linewidth=1.5)#, label="1750 nm")
        spectral_ax.axvline(x=2300, color='black', linestyle='--', linewidth=1.5)#, label="2300 nm")
        spectral_ax.axvline(x=2350, color='black', linestyle='--', linewidth=1.5)#, label="2350 nm")
        # Fill regions between 1700-1750 and 2300-2350 with light colors
        spectral_ax.axvspan(1700, 1750, color='lightblue', alpha=0.3)#, label="1700-1750 nm Region")
        spectral_ax.axvspan(2300, 2350, color='lightgray', alpha=0.3)#, label="2300-2350 nm Region")
        spectral_ax.set_title('Mean Spectrum')
        spectral_ax.set_xlabel('Wavelength (nm)')
        spectral_ax.set_ylabel('Reflectance')
        spectral_ax.grid(True)
        
        # Update the normalized spectrum plot
        normalized_ax.clear()
        normalized_ax.plot(binned_wavelengths, normalized_spectrum)
        # Add vertical lines at wavelengths 1700 and 2300
        normalized_ax.axvline(x=1700, color='blue', linestyle='--', linewidth=1.5)#, label="1700 nm")
        normalized_ax.axvline(x=1750, color='blue', linestyle='--', linewidth=1.5)#, label="1750 nm")
        normalized_ax.axvline(x=2300, color='black', linestyle='--', linewidth=1.5)#, label="2300 nm")
        normalized_ax.axvline(x=2350, color='black', linestyle='--', linewidth=1.5)#, label="2350 nm")
        # Fill regions between 1700-1750 and 2300-2350 with light colors
        normalized_ax.axvspan(1700, 1750, color='lightblue', alpha=0.3)#, label="1700-1750 nm Region")
        normalized_ax.axvspan(2300, 2350, color='lightgray', alpha=0.3)#, label="2300-2350 nm Region")
        normalized_ax.set_title('Standard Normal Spectrum')
        normalized_ax.set_xlabel('Wavelength (nm)')
        normalized_ax.set_ylabel('Normalized Value')
        normalized_ax.grid(True)

        # Update the first derivative plot
        first_deriv_ax.clear()
        first_deriv_ax.plot(binned_wavelengths, first_derivative)
        # Add vertical lines at wavelengths 1700 and 2300
        first_deriv_ax.axvline(x=1700, color='blue', linestyle='--', linewidth=1.5)#, label="1700 nm")
        first_deriv_ax.axvline(x=1750, color='blue', linestyle='--', linewidth=1.5)#, label="1750 nm")
        first_deriv_ax.axvline(x=2300, color='black', linestyle='--', linewidth=1.5)#, label="2300 nm")
        first_deriv_ax.axvline(x=2350, color='black', linestyle='--', linewidth=1.5)#, label="2350 nm")
        # Fill regions between 1700-1750 and 2300-2350 with light colors
        first_deriv_ax.axvspan(1700, 1750, color='lightblue', alpha=0.3)#, label="1700-1750 nm Region")
        first_deriv_ax.axvspan(2300, 2350, color='lightgray', alpha=0.3)#, label="2300-2350 nm Region")
        first_deriv_ax.set_title('First Derivative')
        first_deriv_ax.set_xlabel('Wavelength (nm)')
        first_deriv_ax.set_ylabel('Derivative Value')
        first_deriv_ax.grid(True)
        
        # Update the second derivative plot
        second_deriv_ax.clear()
        second_deriv_ax.plot(binned_wavelengths, second_derivative)
        # Add vertical lines at wavelengths 1700 and 2300
        second_deriv_ax.axvline(x=1700, color='blue', linestyle='--', linewidth=1.5)#, label="1700 nm")
        second_deriv_ax.axvline(x=1750, color='blue', linestyle='--', linewidth=1.5)#, label="1750 nm")
        second_deriv_ax.axvline(x=2300, color='black', linestyle='--', linewidth=1.5)#, label="2300 nm")
        second_deriv_ax.axvline(x=2350, color='black', linestyle='--', linewidth=1.5)#, label="2350 nm")
        # Fill regions between 1700-1750 and 2300-2350 with light colors
        second_deriv_ax.axvspan(1700, 1750, color='lightblue', alpha=0.3)#, label="1700-1750 nm Region")
        second_deriv_ax.axvspan(2300, 2350, color='lightgray', alpha=0.3)#, label="2300-2350 nm Region")
        second_deriv_ax.set_title('Second Derivative')
        second_deriv_ax.set_xlabel('Wavelength (nm)')
        second_deriv_ax.set_ylabel('Second Derivative Value')
        second_deriv_ax.grid(True)

        # Redraw the figure canvas
        fig.canvas.draw_idle()

    # Adjust layout to avoid text overlap
    plt.tight_layout()
    fig.subplots_adjust(hspace=0.4, wspace=0.3)  # Increase spacing between plots

    # Event handler for mouse clicks
    def on_click(event):
        if event.inaxes == image_ax:
            x, y = int(event.xdata), int(event.ydata)
            if 0 <= x < sample_cube.shape[1] and 0 <= y < sample_cube.shape[0]:
                update_spectral_plot(x, y)

    # Connect the click event to the on_click function
    fig.canvas.mpl_connect('button_press_event', on_click)
    
    plt.show()
