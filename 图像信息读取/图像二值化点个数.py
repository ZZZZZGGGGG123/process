import numpy as np
from osgeo import gdal


def count_targets_in_tiff(tiff_path):
    """
    Count the number of target points (pixels with value 1) in a binary TIFF image.

    Args:
        tiff_path (str): Path to the binary TIFF image.

    Returns:
        int: Number of target points in the image.
    """
    # Step 1: Open the TIFF image using GDAL
    ds = gdal.Open(tiff_path)
    if ds is None:
        raise FileNotFoundError(f"Failed to open image at {tiff_path}")

    # Step 2: Read the raster band (assuming the image is a single band)
    band = ds.GetRasterBand(1)  # Get the first (and likely the only) band
    img_array = band.ReadAsArray()  # Read the image into a NumPy array

    # Step 3: Count the number of target points (pixels with value 1)
    target_count = np.sum(img_array == 255)

    return target_count


# Example usage
tiff_path = r"E:\code\process\图像信息读取\67687.tif"
target_count = count_targets_in_tiff(tiff_path)
print(f"Number of target points: {target_count}")
