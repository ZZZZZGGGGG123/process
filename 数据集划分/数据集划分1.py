import os
import random

# 定义原始图像路径和保存序号的txt文件路径
image_dir = r"D:\简化\裁剪后\image"
train_dir = r"D:\简化\裁剪后\ann_dir\train"
val_dir = r"D:\简化\裁剪后\ann_dir\val"
txt_file_path = r"D:\简化\裁剪后\ann_dir\classfly.txt"

# 获取所有图像文件名
image_files = os.listdir(image_dir)
image_files.sort()  # 确保文件名顺序一致

# 打乱图像文件顺序
random.shuffle(image_files)

# 定义训练集、测试集和验证集的比例
train_ratio = 0.9

# 精确计算各个集合的图像数量
total_images = len(image_files)
train_count = round(total_images * train_ratio)  # 使用 round 代替 int 进行四舍五入
val_count = total_images - train_count  # 剩余的分配给验证集

# 分割图像文件为训练集和验证集
train_images = image_files[:train_count]
val_images = image_files[train_count:]

# 创建保存图像的文件夹
os.makedirs(train_dir, exist_ok=True)
os.makedirs(val_dir, exist_ok=True)

# 将图像序号保存到 txt 文件中
with open(txt_file_path, "w") as txt_file:
    txt_file.write("Train:\n")
    txt_file.write("\n".join(train_images))
    txt_file.write("\n\nValidation:\n")
    txt_file.write("\n".join(val_images))

print(f"Total images: {total_images}")
print(f"Train images: {len(train_images)}")
print(f"Validation images: {len(val_images)}")
print("Images split, saved to folders, and image indexes saved to txt file.")
