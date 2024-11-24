from PIL import Image
import os

def tiff_to_png(input_folder, output_folder):
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Loop through files in the input folder
    for filename in os.listdir(input_folder):
        input_path = os.path.join(input_folder, filename)
        output_path = os.path.join(output_folder, os.path.splitext(filename)[0] + ".png")

        # Check if the file is a TIFF image
        if filename.lower().endswith(".tiff") or filename.lower().endswith(".tif"):
            try:
                # Open the TIFF image and save it as PNG
                with Image.open(input_path) as img:
                    img.save(output_path, format="PNG")
                print(f"Converted {filename} to PNG successfully.")
            except Exception as e:
                print(f"Error converting {filename}: {e}")

if __name__ == "__main__":
    input_folder = r"C:\Users\zg\Desktop\res\r7"
    output_folder = r"C:\Users\zg\Desktop\res\r9"
    tiff_to_png(input_folder, output_folder)

