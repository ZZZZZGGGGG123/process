import os
import shutil


def sample_matching_images(folder1, folder2, output_folder):
    """
    根据文件夹1中的文件名，从文件夹2中找出对应的文件，并复制到输出文件夹。

    参数：
    - folder1: 参考图片文件夹路径。
    - folder2: 目标图片文件夹路径。
    - output_folder: 输出文件夹路径。
    """
    # 检查输入文件夹是否存在
    if not os.path.exists(folder1):
        print(f"参考文件夹不存在: {folder1}")
        return
    if not os.path.exists(folder2):
        print(f"目标文件夹不存在: {folder2}")
        return

    # 创建输出文件夹
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print(f"输出文件夹已创建: {output_folder}")

    # 获取文件夹1中的文件名（无扩展名）
    ref_files = [os.path.splitext(f)[0] for f in os.listdir(folder1)]
    ref_files = set(ref_files)  # 使用集合加快查找速度

    # 获取文件夹2中的所有文件
    target_files = os.listdir(folder2)

    # 遍历目标文件夹中的文件，找出匹配的文件
    matched_count = 0
    for target_file in target_files:
        # 分离文件名和扩展名
        target_name, target_ext = os.path.splitext(target_file)

        # 如果文件名匹配，复制到输出文件夹
        if target_name in ref_files:
            old_path = os.path.join(folder2, target_file)
            new_path = os.path.join(output_folder, target_file)
            shutil.copy(old_path, new_path)
            print(f"匹配并复制: {target_file}")
            matched_count += 1

    print(f"操作完成，共复制了 {matched_count} 个文件到 {output_folder}")


# 示例用法
folder1 = r"I:\APV\7去噪结果\山东"  # 参考文件夹路径
folder2 = r"I:\APV\6各省遥感影像\山东"  # 目标文件夹路径
output_folder = r"I:\APV\7去噪结果\山东源"  # 输出文件夹路径
sample_matching_images(folder1, folder2, output_folder)
