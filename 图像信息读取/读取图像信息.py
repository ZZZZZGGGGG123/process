import cv2
import numpy as np

# 输入标签图像路径（请修改为你自己的路径）
label_path = "10538.tif"

# 读取标签图像
label = cv2.imread(label_path)

# 输出标签图像信息
if label is not None:
    # 输出标签图像的形状
    print(f"Label shape: {label.shape}")  # (height, width) 或 (height, width, channels)

    # 输出标签图像的数据类型
    print(f"Label dtype: {label.dtype}")  # 输出数据类型，如 uint8

    # 输出标签图像的位深度（例如，uint8 代表 8 位深度）
    bit_depth = np.iinfo(label.dtype).bits  # 获取数据类型的位深度
    print(f"Bit depth: {bit_depth}-bit")

    # 输出标签图像的通道数
    if len(label.shape) == 2:
        print("Channels: 1 (grayscale)")  # 单通道图像
    else:
        print(f"Channels: {label.shape[2]} (color)")  # 多通道图像

    # 输出标签图像的像素值范围
    print(f"Label pixel value range: {label.min()} to {label.max()}")

    # 输出标签图像的 NumPy 数组
    print("Label image as NumPy array:")
    np.set_printoptions(threshold=np.inf)  # 设置打印数组的阈值为无限大
    print(label)  # 这样就可以打印完整的 NumPy 数组

else:
    print("Error reading label.")
