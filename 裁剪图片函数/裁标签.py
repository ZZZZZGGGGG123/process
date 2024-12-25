import os
from PIL import Image

# 滑动窗口裁剪函数
def PNGCrop(PNGPath, SavePath, CropSize, RepetitionRate):
    # 获取当前文件夹的文件个数len，并以len+1命名即将裁剪得到的图像
    new_name = len(os.listdir(SavePath)) + 1

    for filename in os.listdir(PNGPath):
        if filename.endswith(".png"):
            img = Image.open(os.path.join(PNGPath, filename))
            width, height = img.size

            for i in range(int((height - CropSize * RepetitionRate) / (CropSize * (1 - RepetitionRate)))):
                for j in range(int((width - CropSize * RepetitionRate) / (CropSize * (1 - RepetitionRate)))):
                    cropped_img = img.crop((int(j * CropSize * (1 - RepetitionRate)), int(i * CropSize * (1 - RepetitionRate)),
                                           int(j * CropSize * (1 - RepetitionRate)) + CropSize, int(i * CropSize * (1 - RepetitionRate)) + CropSize))
                    cropped_img.save(os.path.join(SavePath, f'{new_name}.png'))

                    new_name += 1

            # 向前裁剪最后一列
            for i in range(int((height - CropSize * RepetitionRate) / (CropSize * (1 - RepetitionRate)))):
                cropped_img = img.crop((width - CropSize, int(i * CropSize * (1 - RepetitionRate)), width, int(i * CropSize * (1 - RepetitionRate)) + CropSize))
                cropped_img.save(os.path.join(SavePath, f'{new_name}.png'))

                new_name += 1

            # 向前裁剪最后一行
            for j in range(int((width - CropSize * RepetitionRate) / (CropSize * (1 - RepetitionRate)))):
                cropped_img = img.crop((int(j * CropSize * (1 - RepetitionRate)), height - CropSize,
                                       int(j * CropSize * (1 - RepetitionRate)) + CropSize, height))
                cropped_img.save(os.path.join(SavePath, f'{new_name}.png'))

                new_name += 1

            # 裁剪右下角
            cropped_img = img.crop((width - CropSize, height - CropSize, width, height))
            cropped_img.save(os.path.join(SavePath, f'{new_name}.png'))

            new_name += 1

# 示例用法
PNGCrop(
    r"E:\code\Pycode\PythonApplication3_裁剪原图+标签2\PythonApplication3_裁剪原图+标签2\in_png4",
    r"E:\code\Pycode\PythonApplication3_裁剪原图+标签2\PythonApplication3_裁剪原图+标签2\out_png3",
    768, 0)
#768这个参数代表裁剪的子图片尺寸是768*768
#0代表重复率，相邻两张图片的相交的比率为0
