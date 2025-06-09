import pandas as pd
import os
import numpy as np

# 配置参数
input_folder = r"D:\4制图数据\第四章\土地利用"  # 替换为包含1-13.csv的文件夹路径
output_folder =r"D:\4制图数据\第四章\土地利用"  # 替换为输出文件夹路径

output_file = os.path.join(output_folder, "merged_max_values.csv")

# 确保输出文件夹存在
os.makedirs(output_folder, exist_ok=True)

# 1. 定义所有必需的列
REQUIRED_COLUMNS = [
    'ID', 'Area', 'layer', 'path',
    'HISTO_NODATA', 'HISTO_1', 'HISTO_2', 'HISTO_4',
    'HISTO_5', 'HISTO_7', 'HISTO_8', 'HISTO_11'
]

# 2. 读取所有CSV文件并按数字顺序排序
csv_files = [f for f in os.listdir(input_folder) if f.endswith('.csv') and f[:-4].isdigit()]
csv_files = sorted(csv_files, key=lambda x: int(x.split('.')[0]))

# 验证文件数量
if len(csv_files) != 13:
    print(f"警告: 找到 {len(csv_files)} 个CSV文件，但预期13个!")
    print("找到的文件:", csv_files)

# 3. 读取并标准化所有DataFrame
dfs = []
for file in csv_files:
    file_path = os.path.join(input_folder, file)
    df = pd.read_csv(file_path)

    # 标准化列结构
    for col in REQUIRED_COLUMNS:
        if col not in df.columns:
            print(f"警告: 文件 {file} 缺少列 '{col}'，将填充0")
            df[col] = 0  # 填充0

    # 只保留需要的列
    df = df[REQUIRED_COLUMNS]
    dfs.append(df)
    print(f"已加载: {file} ({len(df)} 行)")

# 4. 创建合并框架 - 使用第一个文件的标识列
merged_df = dfs[0][['ID', 'Area', 'layer', 'path']].copy()

# 5. 对每个统计列计算最大值
print("\n开始计算最大值...")
stat_columns = [col for col in REQUIRED_COLUMNS if col.startswith('HISTO_')]

for col in stat_columns:
    print(f"处理列: {col}")

    # 创建空数组存储所有值
    all_values = np.zeros((len(merged_df), len(dfs)))

    # 填充数组
    for i, df in enumerate(dfs):
        all_values[:, i] = df[col].values

    # 计算每行的最大值
    merged_df[col] = np.max(all_values, axis=1)

# 6. 保存结果
merged_df.to_csv(output_file, index=False)
print(f"\n合并完成! 结果已保存至: {output_file}")
print(f"处理统计: {len(dfs)} 个文件, {len(merged_df)} 行数据, {len(stat_columns)} 个统计列")

# 7. 添加验证信息
print("\n前5行结果预览:")
print(merged_df.head())
print("\n列结构验证:")
print(merged_df.columns.tolist())