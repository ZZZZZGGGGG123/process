import cv2
import numpy as np


def is_rgb_or_bgr(image):
    """
    判断图像是RGB还是BGR。

    Args:
        image (numpy.ndarray): 输入的图像数据。

    Returns:
        str: 'RGB' 或 'BGR'，如果无法判断则返回 'Unknown'。
    """
    if image is None:
        return 'Invalid image'

    if len(image.shape) == 3 and image.shape[2] == 3:  # 确保是彩色图像
        # 创建一个测试像素，交换第一个和最后一个通道
        test_pixel = image[0, 0].copy()
        swapped_pixel = test_pixel[[2, 1, 0]]  # 交换R和B

        # 判断原图像中交换前和交换后是否一致
        if np.array_equal(image[0, 0], swapped_pixel):
            return 'RGB'
        else:
            return 'BGR'
    else:
        return 'Unknown'


# 示例
# 加载图像
image_bgr = cv2.imread('ADE_train_00000001.png')  # OpenCV读取图像默认是BGR
result = is_rgb_or_bgr(image_bgr)
print(f'The image format is: {result}')
