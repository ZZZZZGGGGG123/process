import os
from PIL import Image
import numpy as np

# 读取TIFF图像
def readTIFF(fileName):
    img = Image.open(fileName)
    if img is None:
        print(fileName + "文件无法打开")
    return img

# 保存TIFF文件函数
def writeTIFF(im_data, path):
    img = Image.fromarray(im_data)
    img.save(path)

# 读取PNG图像
def readPNG(fileName):
    img = Image.open(fileName)
    if img is None:
        print(fileName + "文件无法打开")
    return img

# 保存PNG文件函数
def writePNG(im_data, path):
    img = Image.fromarray(im_data)
    img.save(path)

'''
滑动窗口裁剪函数
InputPath 输入文件夹路径，包含原图像和标签图像
SaveTiffPath 裁剪后保存原图像的目录
SavePngPath 裁剪后保存标签图像的目录
CropSize 裁剪尺寸
RepetitionRate 重复率
'''
def DualCrop(InputPath, SaveTiffPath, SavePngPath, CropSize, RepetitionRate):
    tiff_files = [f for f in os.listdir(InputPath) if f.endswith(".tiff")]
    png_files = [f for f in os.listdir(InputPath) if f.endswith(".png")]
    tiff_files.sort()  # 确保文件名的顺序一致
    png_files.sort()

    for i, (tiff_file, png_file) in enumerate(zip(tiff_files, png_files), start=1):
        tiff_path = os.path.join(InputPath, tiff_file)
        png_path = os.path.join(InputPath, png_file)
        
        tiff_img = readTIFF(tiff_path)
        png_img = readPNG(png_path)
        
        width, height = tiff_img.size

        # 获取当前文件夹的文件个数 len，并以 len+1 命名即将裁剪得到的图像
        new_name = len(os.listdir(SaveTiffPath)) + 1

        for i in range(int((height - CropSize * RepetitionRate) / (CropSize * (1 - RepetitionRate)))):
            for j in range(int((width - CropSize * RepetitionRate) / (CropSize * (1 - RepetitionRate)))):
                left = int(j * CropSize * (1 - RepetitionRate))
                upper = int(i * CropSize * (1 - RepetitionRate))
                right = left + CropSize
                lower = upper + CropSize

                # 裁剪原图像
                cropped_tiff = tiff_img.crop((left, upper, right, lower))
                cropped_tiff.save(os.path.join(SaveTiffPath, f'{new_name}.tif'))

                # 裁剪标签图像
                cropped_png = png_img.crop((left, upper, right, lower))
                cropped_png.save(os.path.join(SavePngPath, f'{new_name}.png'))

                new_name += 1

        # 向前裁剪最后一列
        for i in range(int((height - CropSize * RepetitionRate) / (CropSize * (1 - RepetitionRate)))):
            left = width - CropSize
            upper = int(i * CropSize * (1 - RepetitionRate))
            right = width
            lower = upper + CropSize

            # 裁剪原图像
            cropped_tiff = tiff_img.crop((left, upper, right, lower))
            cropped_tiff.save(os.path.join(SaveTiffPath, f'{new_name}.tif'))

            # 裁剪标签图像
            cropped_png = png_img.crop((left, upper, right, lower))
            cropped_png.save(os.path.join(SavePngPath, f'{new_name}.png'))

            new_name += 1

        # 向前裁剪最后一行
        for j in range(int((width - CropSize * RepetitionRate) / (CropSize * (1 - RepetitionRate)))):
            left = int(j * CropSize * (1 - RepetitionRate))
            upper = height - CropSize
            right = left + CropSize
            lower = height

            # 裁剪原图像
            cropped_tiff = tiff_img.crop((left, upper, right, lower))
            cropped_tiff.save(os.path.join(SaveTiffPath, f'{new_name}.tif'))

            # 裁剪标签图像
            cropped_png = png_img.crop((left, upper, right, lower))
            cropped_png.save(os.path.join(SavePngPath, f'{new_name}.png'))

            new_name += 1

        # 裁剪右下角
        left = width - CropSize
        upper = height - CropSize
        right = width
        lower = height

        # 裁剪原图像
        cropped_tiff = tiff_img.crop((left, upper, right, lower))
        cropped_tiff.save(os.path.join(SaveTiffPath, f'{new_name}.tif'))

        # 裁剪标签图像
        cropped_png = png_img.crop((left, upper, right, lower))
        cropped_png.save(os.path.join(SavePngPath, f'{new_name}.png'))

        new_name += 1

# 示例用法
DualCrop("E:\code\Pycode\PythonApplication3_裁剪图像4_标签+原图\PythonApplication3_裁剪图像4\in",
         "E:\code\Pycode\PythonApplication3_裁剪图像4_标签+原图\PythonApplication3_裁剪图像4\out_png",
         "E:\code\Pycode\PythonApplication3_裁剪图像4_标签+原图\PythonApplication3_裁剪图像4\out_tiff",
         768, 0)
