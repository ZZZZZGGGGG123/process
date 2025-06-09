import rasterio
from rasterio.mask import mask
import geopandas as gpd
import numpy as np
import pandas as pd
from tqdm import tqdm  # 进度条工具（可选）

import rasterio
from rasterio.mask import mask
import geopandas as gpd
import numpy as np
import pandas as pd
from tqdm import tqdm


def count_suitability_by_province(tif_path, shp_path, output_excel):
    provinces = gpd.read_file(shp_path)

    with rasterio.open(tif_path) as src:
        print(f"栅格范围: {src.bounds}")

        if provinces.crs != src.crs:
            provinces = provinces.to_crs(src.crs)

        results = []
        for idx, row in tqdm(provinces.iterrows(), total=len(provinces)):
            try:
                geom = row.geometry
                if geom.is_empty:
                    print(f"省份 {row['name']} 几何为空")
                    continue

                # 检查几何与栅格是否有交集
                if rasterio.coords.disjoint_bounds(geom.bounds, src.bounds):
                    print(f"省份 {row['name']} 与栅格无交集")
                    counts = [0] * 5
                else:
                    clipped, _ = mask(src, [geom], crop=True, all_touched=True, nodata=src.nodata)
                    valid_values = clipped[0][clipped[0] != src.nodata]

                    # 统计1-5级像元
                    counts = np.bincount(valid_values.astype(int), minlength=6)[1:6]
                    counts = [int(c) for c in counts]

                results.append({
                    "FID": row["FID"],
                    "name": row["name"],
                    "1": counts[0],
                    "2": counts[1],
                    "3": counts[2],
                    "4": counts[3],
                    "5": counts[4]
                })

            except Exception as e:
                print(f"处理省份 {row['name']} 错误: {str(e)}")
                results.append({
                    "FID": row["FID"],
                    "name": row["name"],
                    "1": 0,
                    "2": 0,
                    "3": 0,
                    "4": 0,
                    "5": 0
                })

    pd.DataFrame(results).to_excel(output_excel, index=False)
    print(f"结果已保存至: {output_excel}")




# 调用示例
if __name__ == "__main__":
    count_suitability_by_province(
        tif_path=r"D:\5Arcgis\最终分类统计\最终分类统计适宜性.tif",
        shp_path=r"D:\5Arcgis\最终分类统计\中国_省_Areas.shp",
        output_excel=r"D:\5Arcgis\最终分类统计\province_suitability_counts.xlsx"
    )