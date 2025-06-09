import os
from PIL import Image
import numpy as np


def add_salt_noise(input_folder, output_folder, salt_prob=0.05):
    os.makedirs(output_folder, exist_ok=True)

    for filename in os.listdir(input_folder):
        if filename.endswith(".tif") or filename.endswith(".tiff"):
            image = Image.open(os.path.join(input_folder, filename))
            # 强制转换为 uint8 类型
            pixels = np.array(image, dtype=np.uint8)

            noisy_pixels = pixels.copy()
            background_mask = (pixels == 0)

            # 生成盐粒噪声并确保类型为 uint8
            random_salt = np.random.choice([0, 255],
                                           size=background_mask.sum(),
                                           p=[1 - salt_prob, salt_prob],
                                           dtype=np.uint8)

            np.putmask(noisy_pixels, background_mask, random_salt)

            # 显式转换为 uint8（可选，但保险起见）
            processed_image = Image.fromarray(noisy_pixels, mode='L')
            processed_image.save(os.path.join(output_folder, filename))


if __name__ == "__main__":
    input_folder = r"E:\tiff数据\安徽res"  # 替换为实际输入路径
    output_folder = r"E:\tiff数据\安徽res_noise"  # 替换为实际输出路径
    add_salt_noise(input_folder, output_folder, salt_prob=0.05)




