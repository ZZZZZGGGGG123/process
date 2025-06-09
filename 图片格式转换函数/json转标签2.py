# -*- coding: utf-8 -*-
import base64  # 导入用于Base64编码和解码的模块
import json  # 导入用于处理JSON数据的模块
import os  # 导入操作文件和文件夹的模块
import os.path as osp  # 导入路径操作的模块
import numpy as np  # 导入用于数值处理的模块
import PIL.Image  # 导入Pillow库中的Image模块，用于图像处理
from labelme import utils  # 导入标签工具的模块

# 定义将JSON标注文件转换为图像的函数
def Jsontopng(Yuan_path, num):
    jpgs_path = r"D:\数据集2\ew"  # JPG图像保存路径
    pngs_path = r"D:\数据集2\补充数据集标签2"  # PNG标签图像保存路径
    classes = ["_background_", "PV"]  # 定义标签类别
    count = os.listdir(Yuan_path)  # 列出指定文件夹中的所有文件和子文件夹
    print(count)
    
    # 遍历文件夹中的每个文件
    for i in range(0, len(count)):
        path = os.path.join(Yuan_path, count[i])  # 构建当前文件的完整路径
        print(path)
 
        # 检查文件是否存在且以 '.json' 结尾
        if os.path.isfile(path) and path.endswith('json'):
            # 加载JSON数据
            data = json.load(open(path))
 
            # 检查是否存在图像数据，如果存在则解码为Base64编码字符串
            if data['imageData']:
                imageData = data['imageData']
            else:
                imagePath = os.path.join(os.path.dirname(path), data['imagePath'])
                with open(imagePath, 'rb') as f:
                    imageData = f.read()
                    imageData = base64.b64encode(imageData).decode('utf-8')
 
            # 将Base64编码的图像数据转换为NumPy数组
            img = utils.img_b64_to_arr(imageData)
 
            # 定义标签名到类别值的映射
            label_name_to_value = {'_background_': 0, 'PV': 1}
            
            # 遍历JSON数据中的标注形状，将标签名映射到类别值
            for shape in data['shapes']:
                label_name = shape['label']
                if label_name in label_name_to_value:
                    label_value = label_name_to_value[label_name]
                else:
                    label_value = len(label_name_to_value)
                    label_name_to_value[label_name] = label_value
 
            # 创建用于排序的标签值和标签名的列表
            label_values, label_names = [], []
            for ln, lv in sorted(label_name_to_value.items(), key=lambda x: x[1]):
                label_values.append(lv)
                label_names.append(ln)
            assert label_values == list(range(len(label_values)))
 
            # 使用标签工具中的函数将标注形状转换为标签图像的NumPy数组
            lbl = utils.shapes_to_label(img.shape, data['shapes'], label_name_to_value)
 
            # 转换 RGBA 图像为 RGB 格式，去除 alpha 通道
            img_rgb = img[:, :, :3]
 
            # 保存图像为JPEG格式
            PIL.Image.fromarray(img_rgb).save(osp.join(jpgs_path, str(num) + '.jpg'))
 
            # 创建一个全零数组，并根据标签名填充相应的类别值
            new = np.zeros([np.shape(img)[0], np.shape(img)[1]])
            for name in label_names:
                index_json = label_names.index(name)
                index_all = classes.index(name)
                new = new + index_all * (np.array(lbl) == index_json)
 
            # 保存标签图像为PNG格式
            #utils.lblsave(osp.join(pngs_path, str(num) + '.png'), new)
            #print('Saved ' + count[i].split(".")[0] + '.jpg and ' + count[i].split(".")[0] + '.png')
            #num = num + 1

            # 保存标签图像为PNG格式，使用原始文件名
            label_image_filename = os.path.splitext(os.path.basename(path))[0] + '.png'
            utils.lblsave(osp.join(pngs_path, label_image_filename), new)
            print('Saved ' + count[i].split(".")[0] + '.jpg and ' + label_image_filename)

 
if __name__ == '__main__':
    num = 0  # 文件编号
    Yuan_path = r"D:\数据集2\补充数据集2"  # JSON文件所在路径
    Jsontopng(Yuan_path, num)  # 调用函数开始转换
