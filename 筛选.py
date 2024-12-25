import os
import shutil


def filter_images_by_labels(image_folder, label_folder, output_image_folder):
    """
    根据标签文件夹中的文件，从图像文件夹中筛选出有对应标签的图片文件。

    Args:
        image_folder (str): 图像文件夹路径。
        label_folder (str): 标签文件夹路径。
        output_image_folder (str): 筛选后的图像文件夹路径。

    Returns:
        None
    """
    # 确保输出文件夹存在
    os.makedirs(output_image_folder, exist_ok=True)

    # 获取标签文件的基文件名（不含扩展名）
    label_filenames = {os.path.splitext(file)[0] for file in os.listdir(label_folder) if
                       os.path.isfile(os.path.join(label_folder, file))}

    # 遍历图像文件夹，筛选出有对应标签的图像文件
    for image_file in os.listdir(image_folder):
        image_name, image_ext = os.path.splitext(image_file)
        if image_name in label_filenames:
            # 复制匹配的图像文件到输出文件夹
            shutil.copy(os.path.join(image_folder, image_file), os.path.join(output_image_folder, image_file))

    print(f"筛选完成，输出文件夹：{output_image_folder}")


if __name__ == "__main__":
    # 示例：指定图像文件夹、标签文件夹和输出文件夹
    image_folder = "D:\简化\训练图像"  # 替换为你的图像文件夹路径
    label_folder = "D:\简化\训练图像_标签"  # 替换为你的标签文件夹路径
    output_image_folder = "D:\简化\新建文件夹"  # 替换为你希望保存图像的文件夹路径

    # 调用函数
    filter_images_by_labels(image_folder, label_folder, output_image_folder)
