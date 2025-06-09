import pandas as pd

# 配置参数
input_file = r"D:\4制图数据\第四章\土地利用\merged_max_values.csv"  # 输入CSV文件路径
output_file = r"D:\4制图数据\第四章\土地利用\province_landuse_summary.csv"  # 输出文件路径

# 1. 读取数据
print(f"正在读取数据: {input_file}")
df = pd.read_csv(input_file)

# 2. 验证所需列存在
required_columns = ['layer'] + [f'HISTO_{i}' for i in [1, 2, 4, 5, 7, 8, 11]] + ['HISTO_NODATA']
for col in required_columns:
    if col not in df.columns:
        print(f"警告: 列 '{col}' 缺失，将创建并填充0")
        df[col] = 0

# 3. 分省统计
print("\n按省分组统计中...")
province_groups = df.groupby('layer')

# 4. 计算每个省的总面积
print("计算各省总面积...")
province_area = province_groups['Area'].sum().reset_index()
province_area.columns = ['Province', 'Total_Area_km2']

# 5. 计算各省用地类型统计
print("计算各省用地类型统计...")
landuse_cols = [f'HISTO_{i}' for i in [1, 2, 4, 5, 7, 8, 11]] + ['HISTO_NODATA']
landuse_sum = province_groups[landuse_cols].sum().reset_index()

# 6. 计算各类用地百分比
print("计算各类用地占比...")
for col in landuse_cols:
    # 计算该类型占总面积比例
    percentage_col = col.replace('HISTO', 'PCT')
    landuse_sum[percentage_col] = landuse_sum[col] / landuse_sum[landuse_cols].sum(axis=1) * 100
    landuse_sum[percentage_col] = landuse_sum[percentage_col].round(2)  # 保留两位小数

# 7. 合并结果
result = pd.merge(province_area, landuse_sum, left_on='Province', right_on='layer')
result = result.drop('layer', axis=1)

# 8. 添加土地类型中文名称映射
landuse_names = {
    'HISTO_1': '水体',
    'HISTO_2': '林地',
    'HISTO_4': '湿地',
    'HISTO_5': '耕地',
    'HISTO_7': '建设用地',
    'HISTO_8': '裸地',
    'HISTO_11': '未分类',
    'HISTO_NODATA': '无数据'
}

# 9. 重命名列
new_column_names = {'Total_Area_km2': '总面积(km²)'}
for col in landuse_cols:
    # 数量和占比列
    count_name = f"{landuse_names[col]}面积"
    pct_name = f"{landuse_names[col]}占比(%)"
    new_column_names[col] = count_name
    new_column_names[col.replace('HISTO', 'PCT')] = pct_name

result = result.rename(columns=new_column_names)

# 10. 保存结果
result.to_csv(output_file, index=False, encoding='utf_8_sig')  # 使用UTF-8 with BOM编码支持中文

print(f"\n统计完成! 结果已保存至: {output_file}")
print(f"处理了 {len(df)} 条记录, 共 {len(province_groups)} 个省份")
print("\n前5行结果预览:")
#print(result.head())