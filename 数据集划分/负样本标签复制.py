import os
import shutil


def generate_copied_labels(input_folder, output_folder, start_num, n):
    """
    从输入文件夹中复制标签文件，并重命名为指定的编号范围。

    参数:
    - input_folder: 输入文件夹路径，包含原始标签文件。
    - output_folder: 输出文件夹路径，复制后的标签文件会存放在这里。
    - start_num: 重命名时的起始编号。
    - n: 需要复制的标签文件数量。
    """
    # 获取输入文件夹中的所有标签文件（假设标签文件是图像文件，如 .png, .jpg 等）
    label_files = [f for f in os.listdir(input_folder)
                   if f.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp', '.tif', '.tiff'))]

    if len(label_files) == 0:
        print(f"输入文件夹 {input_folder} 中没有标签文件。")
        return

    # 确保输出文件夹存在
    os.makedirs(output_folder, exist_ok=True)

    # 复制标签文件 n 次，并按指定编号重命名
    current_num = start_num
    for i in range(n):
        label_file = label_files[i % len(label_files)]  # 循环使用标签文件
        file_ext = os.path.splitext(label_file)[1]  # 获取文件扩展名
        new_label_name = f"{current_num}{file_ext}"  # 生成新的标签文件名
        # 复制文件到输出文件夹
        shutil.copy(os.path.join(input_folder, label_file), os.path.join(output_folder, new_label_name))
        current_num += 1  # 更新编号

    print(f"已成功复制 {n} 个标签文件到 {output_folder}，起始编号为 {start_num}。")


# 示例用法
if __name__ == "__main__":
    input_folder = r"D:\数据集2\裁剪后\or"  # 输入文件夹路径，包含原始标签文件
    output_folder = r"D:\数据集2\裁剪后\纯负例标签"  # 输出文件夹路径，存放复制后的标签文件
    start_num = 5751  # 重命名时的起始编号
    n = 1500  # 需要复制的标签文件数量

    generate_copied_labels(input_folder, output_folder, start_num, n)
