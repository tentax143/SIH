import rasterio
import matplotlib.pyplot as plt
import numpy as np

# Open the TIFF file
with rasterio.open('path_to_your_file.tif') as dataset:
    # Read the dataset information
    width, height = dataset.width, dataset.height
    num_bands = dataset.count
    dtype = dataset.dtypes[0]
    crs = dataset.crs
    bounds = dataset.bounds

    # Display dataset metadata
    print("Dataset Metadata:")
    print(f" - Width: {width}")
    print(f" - Height: {height}")
    print(f" - Number of Bands: {num_bands}")
    print(f" - Data Type: {dtype}")
    print(f" - Coordinate Reference System: {crs}")
    print(f" - Bounds: {bounds}")

    # Initialize a plot to show each band individually if multiple bands exist
    fig, axs = plt.subplots(1, num_bands, figsize=(15, 5))
    for band_num in range(1, num_bands + 1):
        # Read each band
        band = dataset.read(band_num)
        print(f"\nAnalyzing Band {band_num}:")

        # Calculate statistics
        band_min, band_max = np.min(band), np.max(band)
        band_mean, band_std = np.mean(band), np.std(band)
        print(f" - Min: {band_min}")
        print(f" - Max: {band_max}")
        print(f" - Mean: {band_mean:.2f}")
        print(f" - Standard Deviation: {band_std:.2f}")

        # Plot histogram for each band
        axs[band_num - 1].hist(band.ravel(), bins=50, color='blue', alpha=0.7)
        axs[band_num - 1].set_title(f'Histogram of Band {band_num}')
        axs[band_num - 1].set_xlabel('Pixel Values')
        axs[band_num - 1].set_ylabel('Frequency')

    plt.tight_layout()
    plt.show()

    # Read the first band for further analysis
    band1 = dataset.read(1)

    # Calculate non-zero pixels statistics for Band 1
    non_zero_mask = band1 > 0
    filtered_band1 = band1[non_zero_mask]
    print("\nNon-zero pixel analysis for Band 1:")
    print(f" - Total non-zero pixels: {filtered_band1.size}")
    print(f" - Sample non-zero values: {filtered_band1[:10]}")
    print(f" - Mean of non-zero pixels: {filtered_band1.mean():.2f}")
    print(f" - Standard deviation of non-zero pixels: {filtered_band1.std():.2f}")

    # Generate and display spatial plot for Band 1
    plt.figure(figsize=(10, 8))
    plt.imshow(band1, cmap='viridis')
    plt.colorbar(label='Pixel Values')
    plt.title('Spatial Distribution of Band 1')
    plt.xlabel('Width (pixels)')
    plt.ylabel('Height (pixels)')
    plt.show()

    # If RGB imagery is available, plot RGB composite image (assuming bands 1, 2, 3 are RGB)
    if num_bands >= 3:
        print("\nDisplaying RGB composite from bands 1, 2, and 3 (if applicable)")
        rgb = np.dstack((dataset.read(1), dataset.read(2), dataset.read(3)))
        plt.figure(figsize=(10, 8))
        plt.imshow(rgb)
        plt.title('RGB Composite Image')
        plt.axis('off')
        plt.show()
    
    # Calculate pixel area statistics if spatial resolution is available
    pixel_size_x, pixel_size_y = dataset.res[0], dataset.res[1]
    pixel_area = abs(pixel_size_x * pixel_size_y)
    print(f"\nPixel Area: {pixel_area:.2f} square units")

    # Display dataset bounds as the geographic extent
    print("Geographic Extent of the Dataset:")
    print(f" - West: {bounds.left}")
    print(f" - East: {bounds.right}")
    print(f" - South: {bounds.bottom}")
    print(f" - North: {bounds.top}")
    
    # Create basic map of band 1 to observe the extent and spatial distribution
    fig, ax = plt.subplots(figsize=(10, 8))
    ax.imshow(band1, cmap='gray', extent=(bounds.left, bounds.right, bounds.bottom, bounds.top))
    ax.set_title('Spatial Extent and Distribution of Band 1')
    ax.set_xlabel('Longitude')
    ax.set_ylabel('Latitude')
    plt.colorbar(ax.imshow(band1, cmap='gray'), ax=ax, label='Pixel Value')
    plt.show()
