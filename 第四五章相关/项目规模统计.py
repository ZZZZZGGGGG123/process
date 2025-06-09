import pandas as pd
import numpy as np


def process_data(file_path):
    # 读取CSV文件（逗号分隔）
    df = pd.read_csv(file_path, sep=',')

    # 确保Area是数值类型

    # 按CLUSTER_ID进行合并，对每个簇面积求和
    grouped_cluster = df.groupby('CLUSTER_ID').agg({
        'Area': 'sum',
        'layer': 'first',  # 取第一个layer值
        'path': 'first',  # 取第一个path值
        'CLUSTER_SIZE': 'first'  # 取第一个CLUSTER_SIZE值
    }).reset_index()

    # 按正确区间定义面积分类函数
    def classify_area(area):
        if area < 0.5:
            return '0-0.5 km²'
        elif area < 1.5:
            return '0.5-1.5 km²'
        elif area < 5:
            return '1.5-5 km²'
        elif area < 20:
            return '5-20 km²'
        else:
            return '>20 km²'

    # 添加面积区间分类列
    grouped_cluster['area_category'] = grouped_cluster['Area'].apply(classify_area)

    # 按省份分组统计
    province_stats = grouped_cluster.groupby('layer').agg(
        average_area=('Area', 'mean'),
        cluster_count=('CLUSTER_ID', 'count')
    ).reset_index()

    # 统计各区间数量
    area_counts = grouped_cluster.groupby(['layer', 'area_category']).size().unstack(fill_value=0)

    # 确保所有类别都存在
    all_categories = ['0-0.5 km²', '0.5-1.5 km²', '1.5-5 km²', '5-20 km²', '>20 km²']
    for cat in all_categories:
        if cat not in area_counts.columns:
            area_counts[cat] = 0

    # 合并统计数据
    result = pd.merge(province_stats, area_counts, on='layer')

    # 重命名列
    result.rename(columns={
        'average_area': '平均面积(km²)',
        'cluster_count': '数量'
    }, inplace=True)

    # 1. 添加总面积列 - 平均面积 * 数量
    result['总面积(km²)'] = result['平均面积(km²)'] * result['数量']

    # 2. 按总面积从大到小排序
    result = result.sort_values(by='总面积(km²)', ascending=False)

    # 调整列顺序（将总面积放在平均面积后面）
    result = result[['layer', '平均面积(km²)', '总面积(km²)', '数量',
                     '0-0.5 km²', '0.5-1.5 km²',
                     '1.5-5 km²', '5-20 km²', '>20 km²']]

    return result


# 使用示例
input_file = r'D:\4制图数据\第四章\项目大小\水光伏项目大小.csv'  # 替换为您的文件路径
result = process_data(input_file)

if result is not None:
    # 保存结果到CSV（使用UTF-8编码）
    result.to_csv('province_statistics.csv', index=False, encoding='utf-8')
    print("结果已成功保存到 province_statistics.csv")

    # 显示排序后的数据摘要
    try:
        print("\n各省份总面积排名:")
        print(result[['layer', '总面积(km²)']].to_string(index=False))

        total_area = result['总面积(km²)'].sum()
        print(f"\n全国光伏总面积: {total_area:.2f} km²")

        province_max = result.loc[result['总面积(km²)'].idxmax(), 'layer']
        province_min = result.loc[result['总面积(km²)'].idxmin(), 'layer']
        print(f"光伏面积最大的省份: {province_max}")
        print(f"光伏面积最小的省份: {province_min}")
    except Exception as e:
        print(f"显示摘要时出错: {e}, 请查看CSV文件")
else:
    print("未能处理文件，请检查输入文件格式")