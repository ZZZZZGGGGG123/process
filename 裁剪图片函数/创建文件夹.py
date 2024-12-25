import os
import shutil


def create_folders(input_dir, output_dir):
    # 确保目标文件夹存在，如果不存在则创建
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 遍历原始文件夹中的子文件夹
    for folder_name in os.listdir(input_dir):
        folder_path = os.path.join(input_dir, folder_name)

        # 仅处理文件夹（排除文件）
        if os.path.isdir(folder_path):
            # 在输出目录中创建相同名称的文件夹
            new_folder_path = os.path.join(output_dir, folder_name)
            if not os.path.exists(new_folder_path):
                os.makedirs(new_folder_path)
                print(f"Created folder: {new_folder_path}")
            else:
                print(f"Folder already exists: {new_folder_path}")
        else:
            print(f"Skipping non-directory: {folder_name}")


# 示例调用
input_directory = r'I:\APV\7out'  # 替换为源文件夹路径
output_directory = r'I:\APV\7out_2'  # 替换为目标文件夹路径

create_folders(input_directory, output_directory)
