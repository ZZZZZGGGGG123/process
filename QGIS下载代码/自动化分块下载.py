import os
import geopandas as gpd
import numpy as np
import processing
from shapely.geometry import Polygon


def download_raster_for_polygons(data, output_dir):
    for i, geom in enumerate(data['geometry']):
        # 检查是否为多边形或多边形集合
        if isinstance(geom, Polygon):
            polygons = [geom]
        elif geom.is_empty:
            continue  # 如果几何对象为空，则跳过
        else:
            polygons = list(geom.geoms)  # 从MultiPolygon获取所有Polygon

        for poly in polygons:
            xx, yy = poly.exterior.coords.xy
            extent_0 = np.min(xx)
            extent_1 = np.max(xx)
            extent_2 = np.min(yy)
            extent_3 = np.max(yy)
            extent = f"{extent_0},{extent_1},{extent_2},{extent_3} [EPSG:4326]"

            # 打印每个多边形的地理范围
            print(f"多边形 {i}: 范围 = {extent}")

            out_path = os.path.join(output_dir, f"{i}.tif")

            # 下载影像
            processing.run("native:rasterize", {
                'EXTENT': extent,
                'EXTENT_BUFFER': 0,
                'TILE_SIZE': 256,
                'MAP_UNITS_PER_PIXEL': 1,
                'MAKE_BACKGROUND_TRANSPARENT': False,
                'MAP_THEME': None,
                'LAYERS': [
                    'type=xyz&zmin=0&zmax=20&url=https://mt1.google.com/vt/lyrs%3Ds%26x%3D{x}%26y%3D{y}%26z%3D{z}'],
                'OUTPUT': out_path
            })
            print(f"Downloaded raster for polygon {i}: {out_path}")


def process_shapefiles(input_folder, output_folder):
    for root, dirs, files in os.walk(input_folder):
        for file in files:
            if file.endswith('.shp'):
                province_name = os.path.basename(root)
                shp_path = os.path.join(root, file)

                # 读取 shapefile 数据
                gdf = gpd.read_file(shp_path)

                # 创建省份输出文件夹路径
                province_output_folder = os.path.join(output_folder, province_name)
                os.makedirs(province_output_folder, exist_ok=True)

                # 下载影像
                download_raster_for_polygons(gdf, province_output_folder)


# 示例调用
input_folder = r'I:\APV\or1'  # 输入文件夹路径
output_folder = r'I:\APV\result1'  # 输出文件夹路径

process_shapefiles(input_folder, output_folder)
