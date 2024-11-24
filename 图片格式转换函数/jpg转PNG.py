from PIL import Image
import os

def convert_jpg_to_png(folder_path):
    # Check if the folder exists
    if not os.path.exists(folder_path):
        print(f"Folder '{folder_path}' does not exist.")
        return

    # Get a list of all files in the folder
    file_list = os.listdir(folder_path)

    # Iterate through the files and convert JPG to PNG
    for filename in file_list:
        if filename.lower().endswith('.jpg'):
            # Load the image
            image_path = os.path.join(folder_path, filename)
            image = Image.open(image_path)

            # Remove the .jpg extension and add .png
            new_filename = os.path.splitext(filename)[0] + '.png'
            new_image_path = os.path.join(folder_path, new_filename)

            # Save the image in PNG format
            image.save(new_image_path, 'PNG')
            print(f"Converted '{filename}' to '{new_filename}'.")

    print("Conversion completed.")

if __name__ == "__main__":
    folder_path = r"C:\Users\zg\Desktop\PV\PVP Dataset\labels2"  # Replace with the path to your folder containing JPG images
    convert_jpg_to_png(folder_path)

