
#此代码是在QGIS控制台中运行的，这里并不适用

import processing
import geopandas as gpd
import numpy as np
import os
from shapely.geometry import Polygon

# 选择目标shp文件，注意投影坐标系要和底图一致
data = gpd.read_file('G:\桌面\新建文件夹 (2)\ceshi.shp')
image_paved_out_dir = 'I:\PV\Test'


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
        
        # 测试：打印每个多边形的地理范围
        print(f"多边形 {i}: 范围 = {extent}")
        
        out_path = os.path.join(image_paved_out_dir, f"{i}.tif")

        # 下载影像
        processing.run("native:rasterize", {
            'EXTENT': extent,
            'EXTENT_BUFFER': 0,
            'TILE_SIZE': 512,
            'MAP_UNITS_PER_PIXEL': 0.5,
            'MAKE_BACKGROUND_TRANSPARENT': False,
            'MAP_THEME': None,
            'LAYERS': ['type=xyz&zmin=0&zmax=20&url=https://mt1.google.com/vt/lyrs%3Ds%26x%3D{x}%26y%3D{y}%26z%3D{z}'],
            'OUTPUT': out_path
        })
