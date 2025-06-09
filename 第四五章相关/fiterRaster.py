import rasterio
import numpy as np
import os
from tqdm import tqdm
import glob


def set_nodata_in_range(input_tif, output_tif, min_value, max_value):
    # 打开输入的栅格文件
    with rasterio.open(input_tif) as src:
        # 获取栅格的元数据
        meta = src.meta

        # 读取栅格数据
        data = src.read(1)  # 读取第一个波段

        # 设置无数据值
        nodata_value = src.nodata

        # 使用 numpy 来替换数据范围内的值为无数据
        data = np.where((data >= min_value) & (data <= max_value), nodata_value, data)

        # 更新栅格的无数据值
        meta.update(nodata=nodata_value)

        # 通过 tqdm 显示处理进度
        with rasterio.open(output_tif, 'w', **meta) as dst:
            # 写入更新后的数据
            for i in tqdm(range(1, 2), desc=f"Processing {os.path.basename(input_tif)}", unit="band"):
                dst.write(data, i)

    print(f"处理完成，输出文件保存为: {output_tif}")


def process_directory(input_dir, output_dir, min_value, max_value):
    # 确保输出目录存在
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 获取所有 .tif 文件的路径
    tif_files = glob.glob(os.path.join(input_dir, '*.tif'))

    # 遍历所有 tif 文件
    for tif_file in tqdm(tif_files, desc="Processing files", unit="file"):
        # 输出文件路径
        output_file = os.path.join(output_dir, os.path.basename(tif_file))

        # 调用处理函数
        set_nodata_in_range(tif_file, output_file, min_value, max_value)


# 输入和输出文件夹路径
input_dir = r'I:\APV\10辅助数据\or'  # 输入文件夹路径
output_dir = r'I:\APV\10辅助数据\res2'  # 输出文件夹路径
min_value = 0  # 设置最小值
max_value = 5  # 设置最大值

# 调用处理函数
process_directory(input_dir, output_dir, min_value, max_value)
