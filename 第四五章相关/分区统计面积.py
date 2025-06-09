import rasterio
from rasterio.mask import mask
import geopandas as gpd
import numpy as np
import pandas as pd
from tqdm import tqdm


def count_suitability_by_province(tif_path, shp_path, output_excel, pixel_area=0.654746):
    """
    按省级行政区统计适宜性面积 (单位：km²)
    :param tif_path: 分类后的适宜性TIFF路径
    :param shp_path: 省级行政区Shapefile路径
    :param output_excel: 输出Excel路径
    :param pixel_area: 单个像元面积 (默认0.654746 km²)
    """
    # 加载省级矢量数据
    provinces = gpd.read_file(shp_path)

    # 打开栅格文件
    with rasterio.open(tif_path) as src:
        # 检查坐标系一致性
        if provinces.crs != src.crs:
            provinces = provinces.to_crs(src.crs)

        # 初始化结果表
        results = []

        # 遍历各省份
        for idx, row in tqdm(provinces.iterrows(), total=len(provinces), desc="处理进度"):
            try:
                geom = row.geometry
                if geom.is_empty:
                    print(f"警告: {row['name']} 几何为空，跳过处理")
                    continue

                # 检查几何与栅格是否有交集
                if rasterio.coords.disjoint_bounds(geom.bounds, src.bounds):
                    area_counts = [0.0] * 5  # 无交集则面积为0
                else:
                    # 裁剪栅格到省份范围
                    clipped, _ = mask(
                        src,
                        [geom],
                        crop=True,
                        all_touched=True,
                        nodata=src.nodata
                    )

                    # 提取有效像元值 (排除NoData)
                    valid_values = clipped[0][clipped[0] != src.nodata]

                    # 统计各等级像元数量并转换为面积
                    counts = np.bincount(valid_values.astype(int), minlength=6)[1:6]
                    area_counts = (counts * pixel_area).round(2).tolist()  # 保留两位小数

                # 记录结果
                results.append({
                    "FID": row["FID"],
                    "name": row["name"],
                    "1": area_counts[0],
                    "2": area_counts[1],
                    "3": area_counts[2],
                    "4": area_counts[3],
                    "5": area_counts[4]
                })

            except Exception as e:
                print(f"处理 {row['name']} 错误: {str(e)}")
                results.append({
                    "FID": row["FID"],
                    "name": row["name"],
                    "1": 0.0,
                    "2": 0.0,
                    "3": 0.0,
                    "4": 0.0,
                    "5": 0.0
                })

    # 输出到Excel
    df = pd.DataFrame(results)
    df.to_excel(output_excel, index=False, float_format="%.2f")  # 确保小数精度
    print(f"结果已保存至: {output_excel}")


# 调用示例 (需替换实际路径)
if __name__ == "__main__":
    count_suitability_by_province(
        tif_path=r"D:\5Arcgis\最终分类统计\最终分类统计适宜性.tif",
        shp_path=r"D:\5Arcgis\最终分类统计\中国_省_Areas.shp",
        output_excel=r"D:\5Arcgis\最终分类统计\province_suitability_areas2.xlsx",
        pixel_area=0.654746  # 根据实际像元面积修改
    )