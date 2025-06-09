import cv2
import numpy as np
import os
from tqdm import tqdm
from osgeo import gdal

# 设置面积阈值，去除小区域
MIN_AREA = 5000  # 这个阈值可以根据你的图像情况进行调整


def remove_noise(image_path, output_path):
    # 使用 GDAL 读取 TIFF 图像
    dataset = gdal.Open(image_path)
    img = dataset.ReadAsArray()  # 读取栅格数据（这里读取的是第一个波段）

    # 获取仿射变换和投影信息
    transform = dataset.GetGeoTransform()
    projection = dataset.GetProjection()

    # 连通组件分析
    num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(img)

    # 创建一个空白图像来保存筛选后的结果
    output_image = np.zeros_like(img)

    # 遍历每个连通区域
    for i in range(1, num_labels):
        area = stats[i, cv2.CC_STAT_AREA]

        # 如果连通区域的面积大于设定的阈值，则保留该区域
        if area > MIN_AREA:
            output_image[labels == i] = 255  # 保留区域

    # 使用 GDAL 保存处理后的图像
    driver = gdal.GetDriverByName('GTiff')  # 获取 GeoTIFF 驱动
    out_dataset = driver.Create(output_path, dataset.RasterXSize, dataset.RasterYSize, 1, gdal.GDT_Byte)

    # 设置投影和仿射变换
    out_dataset.SetGeoTransform(transform)
    out_dataset.SetProjection(projection)

    # 写入处理后的图像数据
    out_dataset.GetRasterBand(1).WriteArray(output_image)

    # 关闭数据集
    out_dataset = None  # 关闭文件，保存数据


def process_folder(input_folder, output_folder):
    # 获取文件夹中的所有图片
    files = [f for f in os.listdir(input_folder) if f.endswith(".tif") or f.endswith(".jpg")]  # 支持其他格式

    # 使用 tqdm 来显示进度条
    for filename in tqdm(files, desc="Processing images", unit="image"):
        input_path = os.path.join(input_folder, filename)
        output_path = os.path.join(output_folder, filename)
        remove_noise(input_path, output_path)


# 调用函数处理文件夹中的所有图片
input_folder = r"I:\APV\7out_2\浙江"
output_folder = r"I:\APV\7.2矢量化结果\浙江去噪"

process_folder(input_folder, output_folder)
