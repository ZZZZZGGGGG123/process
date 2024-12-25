import os
import numpy as np
from PIL import Image
from tqdm import tqdm
from multiprocessing import Pool, Manager

def check_single_image(img_path):
    """
    检查单个图像文件是否损坏或无法加载。
    """
    try:
        # 尝试打开图像
        img = Image.open(img_path)
        # 尝试转换为NumPy数组
        img_array = np.array(img)
        # 检查是否为合法的数值数组
        if not isinstance(img_array, np.ndarray) or img_array.dtype == np.object_:
            return img_path  # 无效图像
        return None  # 有效图像返回None
    except Exception:
        return img_path  # 异常图像

def process_images_in_folder(folder_path, valid_extensions=None, num_workers=4):
    """
    使用多进程检查文件夹中的图像文件。

    参数：
        folder_path (str): 要检查的文件夹路径。
        valid_extensions (list): 支持的图像文件扩展名。
        num_workers (int): 并行处理的进程数。

    返回：
        invalid_images (list): 包含有问题图像文件名称的列表。
    """
    if valid_extensions is None:
        valid_extensions = ['.bmp', '.dib', '.png', '.jpg', '.jpeg', '.pbm', '.pgm', '.ppm', '.tif', '.tiff']

    # 获取所有图像文件路径
    image_paths = []
    for root, _, files in os.walk(folder_path):
        for file in files:
            if any(file.lower().endswith(ext) for ext in valid_extensions):
                image_paths.append(os.path.join(root, file))

    print(f"Total images found: {len(image_paths)}")

    # 使用多进程处理
    with Pool(processes=num_workers) as pool, Manager() as manager:
        invalid_images = manager.list()
        for result in tqdm(pool.imap_unordered(check_single_image, image_paths), total=len(image_paths), desc="Checking images"):
            if result:
                invalid_images.append(result)

    return list(invalid_images)

def save_invalid_images(invalid_images, output_file):
    """
    将有问题的图像路径保存到文件中。
    """
    with open(output_file, 'w') as f:
        for img_path in invalid_images:
            f.write(img_path + '\n')

if __name__ == "__main__":
    folder_path = r"I:\APV\6各省遥感影像\福建"  # 替换为您的图像文件夹路径
    output_file = "E:\code\process\数据检查\invalid.txt"  # 检查结果保存路径

    # 检查图像文件
    invalid_images = process_images_in_folder(folder_path, num_workers=8)

    # 打印和保存结果
    if invalid_images:
        print(f"Invalid images found: {len(invalid_images)}")
        save_invalid_images(invalid_images, output_file)
        print(f"Invalid image list saved to {output_file}")
    else:
        print("All images are valid!")
