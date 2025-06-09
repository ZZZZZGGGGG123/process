import os
import shutil


def copy_and_rename_images(input_folder, output_folder, start_number, prefix=""):
    """
    复制并重命名图片文件，从输入文件夹复制到输出文件夹。

    参数：
    - input_folder: 输入文件夹路径。
    - output_folder: 输出文件夹路径。
    - start_number: 起始编号。
    - prefix: 新文件名前缀（默认 'image'）。
    """
    # 检查输入文件夹是否存在
    if not os.path.exists(input_folder):
        print(f"输入文件夹不存在: {input_folder}")
        return

    # 如果输出文件夹不存在，则创建
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print(f"输出文件夹已创建: {output_folder}")

    # 获取输入文件夹中的所有文件
    files = os.listdir(input_folder)
    # 过滤出图片文件（支持常见格式）
    image_files = [f for f in files if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tif'))]

    if not image_files:
        print("输入文件夹中没有找到图片文件。")
        return

    # 按文件名排序
    image_files.sort()

    # 开始复制并重命名
    current_number = start_number
    for file_name in image_files:
        # 获取原文件的完整路径
        old_path = os.path.join(input_folder, file_name)
        # 获取文件扩展名
        file_extension = os.path.splitext(file_name)[1]
        # 生成新文件名
        new_name = f"{prefix}{current_number:04d}{file_extension}"  # 用4位编号，格式如 image_0001.jpg
        new_path = os.path.join(output_folder, new_name)

        # 复制并重命名文件
        shutil.copy(old_path, new_path)
        print(f"复制并重命名: {file_name} -> {new_name}")
        current_number += 1

    print("图片文件复制并重命名完成！")


# 示例用法
input_folder = r"D:\数据集2\裁剪后_最终数据集\label_负"  # 输入文件夹路径
output_folder = r"D:\数据集2\裁剪后_最终数据集\label_负"  # 输出文件夹路径
start_number = 7816  # 起始编号
copy_and_rename_images(input_folder, output_folder, start_number)
