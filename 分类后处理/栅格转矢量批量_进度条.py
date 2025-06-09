from osgeo import gdal, ogr, osr
import os
from tqdm import tqdm  # 导入tqdm进度条库

def raster_to_vector(raster_input, layer):
    # 打开栅格数据集
    raster_ds = gdal.Open(raster_input, gdal.GA_ReadOnly)
    if not raster_ds:
        print(f"无法打开文件 {raster_input}")
        return

    # 获取栅格的第一波段
    band = raster_ds.GetRasterBand(1)

    # 创建内存中栅格图层，作为掩膜
    mask_band = gdal.GetDriverByName('MEM').Create('', raster_ds.RasterXSize, raster_ds.RasterYSize, 1, gdal.GDT_Byte)
    mask_band_array = band.ReadAsArray()

    # 设置掩膜：值为255的像素设为1，其他设为0
    mask_band_array[mask_band_array == 255] = 1
    mask_band_array[mask_band_array != 1] = 0

    # 写入掩膜波段
    mask_band.GetRasterBand(1).WriteArray(mask_band_array)
    
    # 使用Polygonize函数将栅格转为矢量
    gdal.Polygonize(band, mask_band.GetRasterBand(1), layer, 0)

def batch_raster_to_vector(input_folder, output_shapefile):
    # 创建输出的Shapefile
    driver = ogr.GetDriverByName('ESRI Shapefile')
    if os.path.exists(output_shapefile):
        driver.DeleteDataSource(output_shapefile)
    
    vector_ds = driver.CreateDataSource(output_shapefile)
    
    # 定义空间参考，这里使用EPSG:3857（Web墨卡托投影）
    srs = osr.SpatialReference()
    srs.ImportFromEPSG(3857)
    
    # 创建矢量图层
    layer = vector_ds.CreateLayer('raster_vector', srs=srs)
    
    # 添加ID字段
    id_field = ogr.FieldDefn("ID", ogr.OFTInteger)
    layer.CreateField(id_field)

    # 获取输入文件夹中的所有.tif文件
    raster_files = [f for f in os.listdir(input_folder) if f.endswith(".tif")]

    # 使用tqdm来显示进度条
    for i, filename in tqdm(enumerate(raster_files), total=len(raster_files), desc="Processing rasters"):
        raster_input = os.path.join(input_folder, filename)
        print(f"正在处理 {raster_input}")
        raster_to_vector(raster_input, layer)

    vector_ds = None  # 保存并关闭Shapefile

# 示例用法

input_folder = r"I:\APV\7去噪结果\辽宁"
output_shapefile =  r"I:\APV\8矢量化结果\辽宁"


batch_raster_to_vector(input_folder, output_shapefile)
