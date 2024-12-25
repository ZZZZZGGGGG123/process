import os
import random
import shutil  # 用于文件复制

# 定义原始图像路径和标签路径
image_dir = r"G:\桌面\训练数据\PV\PVP Dataset\images2"  # 图像文件夹路径
annotation_dir = r"G:\桌面\训练数据\PV\PVP Dataset\labels2"  # 标签文件夹路径

# 用户定义的train和val文件夹路径（你自己指定）
train_image_dir = r"E:\code\BiSeNet-master\datasets\PVP\images\trainning"  # 训练集图像文件夹路径
val_image_dir = r"E:\code\BiSeNet-master\datasets\PVP\images\validation"  # 验证集图像文件夹路径
train_annotation_dir = r"E:\code\BiSeNet-master\datasets\PVP\annotations\trainning"  # 训练集标签文件夹路径
val_annotation_dir = r"E:\code\BiSeNet-master\datasets\PVP\annotations\validation"  # 验证集标签文件夹路径

# 定义保存序号的txt文件路径
train_txt_path = r"E:\code\BiSeNet-master\datasets\PVP\train.txt"
val_txt_path = r"E:\code\BiSeNet-master\datasets\PVP\val.txt"

# 获取所有图像文件名
image_files = os.listdir(image_dir)
image_files = [file for file in image_files if file.endswith('.jpg')]  # 仅选择jpg文件
image_files.sort()  # 确保文件名顺序一致

# 去掉扩展名
image_files = [os.path.splitext(file)[0] for file in image_files]

# 打乱图像文件顺序
random.shuffle(image_files)

# 定义训练集、验证集的比例
train_ratio = 0.9

# 精确计算各个集合的图像数量
total_images = len(image_files)
train_count = round(total_images * train_ratio)
val_count = total_images - train_count

# 分割图像文件为训练集和验证集
train_images = image_files[:train_count]
val_images = image_files[train_count:]

# 复制训练集和验证集的图像文件到对应文件夹
for image in train_images:
    src_image_path = os.path.join(image_dir, image + '.jpg')  # 源图像路径
    dest_image_path = os.path.join(train_image_dir, image + '.jpg')  # 目标训练集路径
    if os.path.exists(src_image_path):
        shutil.copy(src_image_path, dest_image_path)

for image in val_images:
    src_image_path = os.path.join(image_dir, image + '.jpg')  # 源图像路径
    dest_image_path = os.path.join(val_image_dir, image + '.jpg')  # 目标验证集路径
    if os.path.exists(src_image_path):
        shutil.copy(src_image_path, dest_image_path)

# 复制训练集和验证集的标签文件到对应文件夹
for image in train_images:
    src_annotation_path = os.path.join(annotation_dir, image + '.png')  # 源标签路径
    dest_annotation_path = os.path.join(train_annotation_dir, image + '.png')  # 目标标签路径
    if os.path.exists(src_annotation_path):
        shutil.copy(src_annotation_path, dest_annotation_path)

for image in val_images:
    src_annotation_path = os.path.join(annotation_dir, image + '.png')  # 源标签路径
    dest_annotation_path = os.path.join(val_annotation_dir, image + '.png')  # 目标标签路径
    if os.path.exists(src_annotation_path):
        shutil.copy(src_annotation_path, dest_annotation_path)

# 将图像序号分别保存到 train.txt 和 val.txt 文件中
with open(train_txt_path, "w") as train_txt:
    train_txt.write("\n".join(train_images))

with open(val_txt_path, "w") as val_txt:
    val_txt.write("\n".join(val_images))

print(f"Total images: {total_images}")
print(f"Train images: {len(train_images)}")
print(f"Validation images: {len(val_images)}")
print("Image filenames saved to train.txt and val.txt.")
print("Images and annotations copied to train and val directories.")
