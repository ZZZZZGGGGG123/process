import processing
import geopandas as gpd
import numpy as np
import os
from shapely.geometry import Polygon
'''
�˴�����QGIS�����У����ض���ε���Ӿ�������Ӧ��ң��Ӱ��
'''
# ѡ��Ŀ��shp�ļ���ע��ͶӰ����ϵҪ�͵�ͼһ��
data = gpd.read_file('G:/����/data append/China_PV_training_polygon_2020.shp')
image_paved_out_dir = 'G:/����/�½��ļ��� (4)/'

for i, geom in enumerate(data['geometry']):
    # ����Ƿ�Ϊ����λ����μ���
    if isinstance(geom, Polygon):
        polygons = [geom]
    elif geom.is_empty:
        continue  # ������ζ���Ϊ�գ�������
    else:
        polygons = list(geom.geoms)  # ��MultiPolygon��ȡ����Polygon

    for poly in polygons:
        xx, yy = poly.exterior.coords.xy
        extent_0 = np.min(xx)
        extent_1 = np.max(xx)
        extent_2 = np.min(yy)
        extent_3 = np.max(yy)
        extent = f"{extent_0},{extent_1},{extent_2},{extent_3} [EPSG:4326]"

        # ���ԣ���ӡÿ������εĵ���Χ
        print(f"����� {i}: ��Χ = {extent}")

        out_path = os.path.join(image_paved_out_dir, f"{i}.tif")

        # ����Ӱ��
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
