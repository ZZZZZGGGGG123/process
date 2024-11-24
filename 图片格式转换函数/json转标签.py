import os
import json
import numpy as np
from PIL import Image, ImageDraw

# 定义类别映射，将类别名映射到标签值
class_mapping = {
    "blackground": 0,
    "PV": 1,
    # 添加更多类别映射
}

# 指定包含JSON文件的文件夹路径
json_folder = r"E:\code\Pycode\PythonApplication5_json转标签\PythonApplication5_json转标签\json"

# 指定保存标签图的文件夹路径
output_folder = r'E:\code\Pycode\PythonApplication5_json转标签\PythonApplication5_json转标签\res'

# 创建保存标签图的文件夹（如果不存在）
os.makedirs(output_folder, exist_ok=True)

# 遍历文件夹中的JSON文件
for json_filename in os.listdir(json_folder):
    if json_filename.endswith('.json'):
        # 从JSON文件加载标注数据
        with open(os.path.join(json_folder, json_filename), 'r', encoding='utf-8') as json_file:annotation_data = json.load(json_file)

        # 获取图像尺寸
        image_width = annotation_data["image_width"]
        image_height = annotation_data["image_height"]

        # 创建空的标签图
        label_map = np.zeros((image_height, image_width), dtype=np.uint8)

        # 遍历标注数据
        for annotation in annotation_data["annotations"]:
            class_name = annotation["class_name"]
            class_id = class_mapping.get(class_name, 0)  # 默认为0，表示背景类别
            polygon = annotation["polygon"]  # 标注的多边形坐标

            # 使用PIL库来在标签图上填充多边形区域
            polygon_points = [(x, y) for x, y in polygon]
            img = Image.new('L', (image_width, image_height), 0)
            ImageDraw.Draw(img).polygon(polygon_points, outline=class_id, fill=class_id)
            label_map += np.array(img)

        # 保存标签图为图像文件
        label_map_image = Image.fromarray(label_map)
        label_map_image.save(os.path.join(output_folder, f'{json_filename[:-5]}.png'))

