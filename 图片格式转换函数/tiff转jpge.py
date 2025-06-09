from PIL import Image
import os

def convert_tiff_to_jpeg(input_folder, output_folder):
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Loop through all files in the input folder
    for filename in os.listdir(input_folder):
        input_path = os.path.join(input_folder, filename)

        # Check if the file is a TIFF image
        if filename.lower().endswith(".tiff") or filename.lower().endswith(".tif"):
            try:
                # Open the TIFF image
                with Image.open(input_path) as img:
                    # Generate the output JPEG filename by replacing the extension
                    output_filename = os.path.splitext(filename)[0] + ".jpg"
                    output_path = os.path.join(output_folder, output_filename)

                    # Convert and save as JPEG
                    img.save(output_path, "JPEG")

                print(f"Converted {filename} to {output_filename}")
            except Exception as e:
                print(f"Error converting {filename}: {e}")
        else:
            print(f"Skipping {filename}: Not a TIFF image")

if __name__ == "__main__":
    input_folder = r"D:\数据集2\裁剪后_最终数据集\负"  # Replace with the path to the folder containing TIFF images
    output_folder = r"D:\数据集2\裁剪后_最终数据集\负_jpg"  # Replace with the path to the folder where you want to save JPEG images

    convert_tiff_to_jpeg(input_folder, output_folder)

