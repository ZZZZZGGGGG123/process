input_txt_path = r"D:\简化\裁剪后\ann_dir\classfly.txt"
output_txt_path = r"D:\简化\裁剪后\ann_dir\classfly2.txt"
'''
此函数可以把txt文件标签列的后缀去掉，例如：图片1.tiff >>> 图片1
'''
with open(input_txt_path, "r") as input_file, open(output_txt_path, "w") as output_file:
    for line in input_file:
        line = line.strip()
        if line.endswith(".tiff"):
            line = line[:-5]  # 去掉后缀
        output_file.write(line + "\n")

print("Processed txt file saved.")

