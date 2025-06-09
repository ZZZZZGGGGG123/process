import os
from osgeo import gdal
from PIL import Image
import numpy as np

# 读取Tiff数据集
def readTiff(fileName):
    dataset = gdal.Open(fileName)
    if dataset is None:
        print(fileName + "文件无法打开")
    return dataset

# 读取PNG图像
def readPNG(fileName):
    img = Image.open(fileName)
    if img is None:
        print(fileName + "文件无法打开")
    return img

# 保存Tiff文件函数
def writeTiff(im_data, im_geotrans, im_proj, path):
    if 'int8' in im_data.dtype.name:
        datatype = gdal.GDT_Byte
    elif 'int16' in im_data.dtype.name:
        datatype = gdal.GDT_UInt16
    else:
        datatype = gdal.GDT_Float32
    if len(im_data.shape) == 3:
        im_bands, im_height, im_width = im_data.shape
    elif len(im_data.shape) == 2:
        im_data = np.array([im_data])
        im_bands, im_height, im_width = im_data.shape
    driver = gdal.GetDriverByName("GTiff")
    dataset = driver.Create(path, int(im_width), int(im_height), int(im_bands), datatype)
    if dataset is not None:
        dataset.SetGeoTransform(im_geotrans)
        dataset.SetProjection(im_proj)
    for i in range(im_bands):
        dataset.GetRasterBand(i + 1).WriteArray(im_data[i])
    del dataset

# 保存PNG文件函数
def writePNG(im_data, path):
    img = Image.fromarray(im_data)
    img.save(path)

# 滑动窗口裁剪函数
def DualCrop(inputTiffFolder, inputPngFolder, outputTiffFolder, outputPngFolder, cropSize, repetitionRate):
    # 获取所有的Tiff文件
    tiff_files = [f for f in os.listdir(inputTiffFolder) if f.endswith(".tif") or f.endswith(".tiff")]

    for tiff_file in tiff_files:
        tiff_path = os.path.join(inputTiffFolder, tiff_file)
        png_file = os.path.join(inputPngFolder, tiff_file.replace(".tif", ".png"))  # 假设PNG文件名与Tiff文件名对应

        dataset_img = readTiff(tiff_path)
        width = dataset_img.RasterXSize
        height = dataset_img.RasterYSize
        proj = dataset_img.GetProjection()
        geotrans = dataset_img.GetGeoTransform()
        img = dataset_img.ReadAsArray(0, 0, width, height)  # 获取数据

        # 获取当前文件夹的文件个数 len，并以 len+1 命名即将裁剪得到的图像
        new_name = len(os.listdir(outputTiffFolder)) + 1

        for i in range(int((height - cropSize * repetitionRate) / (cropSize * (1 - repetitionRate)))):
            for j in range(int((width - cropSize * repetitionRate) / (cropSize * (1 - repetitionRate)))):
                cropped_img = img[:,
                                  int(i * cropSize * (1 - repetitionRate)): int(i * cropSize * (1 - repetitionRate)) + cropSize,
                                  int(j * cropSize * (1 - repetitionRate)): int(j * cropSize * (1 - repetitionRate)) + cropSize]
                writeTiff(cropped_img, geotrans, proj, os.path.join(outputTiffFolder, f'{new_name}.tiff'))

                if os.path.exists(png_file):
                    png_img = readPNG(png_file)
                    cropped_png = png_img.crop((0, 0, cropSize, cropSize))
                    cropped_png.save(os.path.join(outputPngFolder, f'{new_name}.png'))

                new_name += 1

        # 向前裁剪最后一列
        for i in range(int((height - cropSize * repetitionRate) / (cropSize * (1 - repetitionRate)))):
            cropped_img = img[:,
                              int(i * cropSize * (1 - repetitionRate)): int(i * cropSize * (1 - repetitionRate)) + cropSize,
                              width - cropSize: width]
            writeTiff(cropped_img, geotrans, proj, os.path.join(outputTiffFolder, f'{new_name}.tiff'))

            if os.path.exists(png_file):
                png_img = readPNG(png_file)
                cropped_png = png_img.crop((png_img.width - cropSize, 0, png_img.width, cropSize))
                cropped_png.save(os.path.join(outputPngFolder, f'{new_name}.png'))

            new_name += 1

        # 向前裁剪最后一行
        for j in range(int((width - cropSize * repetitionRate) / (cropSize * (1 - repetitionRate)))):
            cropped_img = img[:,
                              height - cropSize: height,
                              int(j * cropSize * (1 - repetitionRate)): int(j * cropSize * (1 - repetitionRate)) + cropSize]
            writeTiff(cropped_img, geotrans, proj, os.path.join(outputTiffFolder, f'{new_name}.tiff'))

            if os.path.exists(png_file):
                png_img = readPNG(png_file)
                cropped_png = png_img.crop((0, png_img.height - cropSize, cropSize, png_img.height))
                cropped_png.save(os.path.join(outputPngFolder, f'{new_name}.png'))

            new_name += 1

        # 裁剪右下角
        cropped_img = img[:,
                          height - cropSize: height,
                          width - cropSize: width]
        writeTiff(cropped_img, geotrans, proj, os.path.join(outputTiffFolder, f'{new_name}.tiff'))

        if os.path.exists(png_file):
            png_img = readPNG(png_file)
            cropped_png = png_img.crop((png_img.width - cropSize, png_img.height - cropSize, png_img.width, png_img.height))
            cropped_png.save(os.path.join(outputPngFolder, f'{new_name}.png'))

        new_name += 1

# 示例用法
DualCrop(
    r"D:\数据集2\补充数据集2",  # 输入Tiff文件夹
    r"D:\数据集2\补充数据集标签2",  # 输入PNG标签文件夹
    r"D:\数据集2\1",  # 输出Tiff文件夹
    r"D:\数据集2\2",  # 输出PNG标签文件夹
    768, 0  # 裁剪尺寸和重复率
)
