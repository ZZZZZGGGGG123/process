import os
import random
import shutil


def sample_images_with_rename(input_folder, output_folder, start_num, end_num, sample_count, rename_start):
    """
    从输入文件夹中随机采样图片，并复制到输出文件夹，且重新命名。

    参数:
    - input_folder: 输入文件夹路径
    - output_folder: 输出文件夹路径
    - start_num: 采样编号起始值
    - end_num: 采样编号结束值
    - sample_count: 采样的图片数量
    - rename_start: 重命名起始编号
    """
    # 获取输入文件夹中的所有图片文件
    image_files = [f for f in os.listdir(input_folder)
                   if f.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp', '.tif', '.tiff'))]

    # 过滤编号范围内的文件
    valid_files = [f for f in image_files
                   if start_num <= int(os.path.splitext(f)[0]) <= end_num]

    # 检查是否有足够的文件供采样
    if len(valid_files) < sample_count:
        raise ValueError(f"可用图片数量不足，找到 {len(valid_files)} 张图片，但需要 {sample_count} 张。")

    # 随机采样
    sampled_files = random.sample(valid_files, sample_count)

    # 确保输出文件夹存在
    os.makedirs(output_folder, exist_ok=True)

    # 复制采样的图片到输出文件夹，并重新命名
    current_name = rename_start
    for file in sampled_files:
        ext = os.path.splitext(file)[1]  # 获取文件扩展名
        new_name = f"{current_name}{ext}"  # 生成新文件名
        shutil.copy(os.path.join(input_folder, file), os.path.join(output_folder, new_name))
        current_name += 1  # 递增编号

    print(f"已成功将 {sample_count} 张图片复制到 {output_folder}，起始编号为 {rename_start}。")


# 示例用法
if __name__ == "__main__":
    input_folder = r"I:\APV\6各省遥感影像\安徽"  # 输入文件夹路径
    output_folder = r"D:\数据集2\裁剪后\纯负例"  # 输出文件夹路径
    start_num = 1  # 起始编号
    end_num = 80000  # 结束编号
    sample_count = 1500  # 需要采样的数量
    rename_start = 5751  # 重命名的起始编号

    sample_images_with_rename(input_folder, output_folder, start_num, end_num, sample_count, rename_start)
