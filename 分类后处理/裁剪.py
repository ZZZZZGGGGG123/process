import os
import numpy as np
from osgeo import gdal


def crop_tif_image(input_file, output_folder, crop_size=512):
    dataset = gdal.Open(input_file)
    if dataset is None:
        print(f"文件 {input_file} 无法打开")
        return

    # 获取影像宽度、高度和波段数
    width = dataset.RasterXSize
    height = dataset.RasterYSize
    bands = dataset.RasterCount

    # 获取地理坐标和投影信息
    geotrans = dataset.GetGeoTransform()
    proj = dataset.GetProjection()

    # 计算行列数，处理边缘部分
    rows = height // crop_size + (1 if height % crop_size > 0 else 0)
    cols = width // crop_size + (1 if width % crop_size > 0 else 0)

    for i in range(rows):
        for j in range(cols):
            # 计算裁剪区域的偏移量
            x_off = j * crop_size
            y_off = i * crop_size

            # 计算裁剪区域的实际宽高
            actual_width = min(crop_size, width - x_off)
            actual_height = min(crop_size, height - y_off)

            # 读取裁剪区域的数据
            data = dataset.ReadAsArray(x_off, y_off, actual_width, actual_height)

            # 更新裁剪区域的地理信息
            new_geotrans = list(geotrans)
            new_geotrans[0] = geotrans[0] + x_off * geotrans[1]
            new_geotrans[3] = geotrans[3] + y_off * geotrans[5]

            # 构造输出文件路径
            output_file = os.path.join(
                output_folder,
                f"{os.path.splitext(os.path.basename(input_file))[0]}_{i}_{j}.tif",
            )

            # 保存裁剪后的影像
            write_tif_image(data, output_file, new_geotrans, proj)


def batch_crop_tif_images(input_folder, output_folder, crop_size=512):
    # 确保输出文件夹存在
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 遍历输入文件夹中的所有 .tif 文件
    for filename in os.listdir(input_folder):
        if filename.endswith(".tif"):
            input_file = os.path.join(input_folder, filename)
            print(f"正在处理文件：{input_file}")
            crop_tif_image(input_file, output_folder, crop_size)


def write_tif_image(im_data, output_file, geotrans, proj):
    # 根据 im_data 的数据类型选择 GDAL 数据类型
    if "int8" in im_data.dtype.name:
        datatype = gdal.GDT_Byte
    elif "int16" in im_data.dtype.name:
        datatype = gdal.GDT_UInt16
    else:
        datatype = gdal.GDT_Float32

    # 确定波段数量
    if len(im_data.shape) == 3:
        im_bands, im_height, im_width = im_data.shape
    elif len(im_data.shape) == 2:
        im_data = np.array([im_data])
        im_bands, im_height, im_width = im_data.shape

    # 创建输出文件
    driver = gdal.GetDriverByName("GTiff")
    dataset = driver.Create(output_file, im_width, im_height, im_bands, datatype)

    # 设置地理信息
    dataset.SetGeoTransform(geotrans)
    dataset.SetProjection(proj)

    # 写入影像数据
    for i in range(im_bands):
        dataset.GetRasterBand(i + 1).WriteArray(im_data[i])
    del dataset  # 关闭文件


# 示例用法
input_folder = r"I:\APV\天"  # 输入文件夹路径
output_folder = r"I:\APV\天out"  # 输出文件夹路径
batch_crop_tif_images(input_folder, output_folder, crop_size=512)
