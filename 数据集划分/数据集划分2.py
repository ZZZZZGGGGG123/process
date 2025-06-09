import os
import random

# 定义原始图像路径和保存序号的txt文件路径
image_dir = r"D:\数据集2\裁剪后_最终数据集\image_jpg"
train_dir = r"D:\数据集2\裁剪后_最终数据集\ann_dir\train"
val_dir = r"D:\数据集2\裁剪后_最终数据集\ann_dir\val"
train_txt_path = r"D:\数据集2\裁剪后_最终数据集\ann_dir\train.txt"
val_txt_path = r"D:\数据集2\裁剪后_最终数据集\ann_dir\val.txt"

# 获取所有图像文件名
image_files = os.listdir(image_dir)
image_files.sort()  # 确保文件名顺序一致

# 去掉扩展名
image_files = [os.path.splitext(file)[0] for file in image_files]

# 打乱图像文件顺序
random.shuffle(image_files)

# 定义训练集、测试集和验证集的比例
train_ratio = 0.9

# 精确计算各个集合的图像数量
total_images = len(image_files)
train_count = round(total_images * train_ratio)
val_count = total_images - train_count

# 分割图像文件为训练集和验证集
train_images = image_files[:train_count]
val_images = image_files[train_count:]

# 创建保存图像的文件夹
os.makedirs(train_dir, exist_ok=True)
os.makedirs(val_dir, exist_ok=True)

# 将图像序号分别保存到 train.txt 和 val.txt 文件中
with open(train_txt_path, "w") as train_txt:
    train_txt.write("\n".join(train_images))

with open(val_txt_path, "w") as val_txt:
    val_txt.write("\n".join(val_images))

print(f"Total images: {total_images}")
print(f"Train images: {len(train_images)}")
print(f"Validation images: {len(val_images)}")
print("Image filenames saved to train.txt and val.txt.")
