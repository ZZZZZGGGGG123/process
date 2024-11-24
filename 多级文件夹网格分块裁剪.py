import os
import geopandas as gpd
from shapely.geometry import box
import pandas as pd


def create_grid(bounds, grid_size, crs):
    xmin, ymin, xmax, ymax = bounds
    rows = int((ymax - ymin) / grid_size)
    cols = int((xmax - xmin) / grid_size)

    grid = []
    for i in range(rows):
        for j in range(cols):
            minx = xmin + j * grid_size
            miny = ymin + i * grid_size
            maxx = minx + grid_size
            maxy = miny + grid_size
            grid.append(box(minx, miny, maxx, maxy))

    return gpd.GeoDataFrame(grid, columns=['geometry'], crs=crs)


def process_in_chunks(gdf, grid_size, chunk_size):
    gdf = gdf.to_crs(epsg=4326)  # 转换坐标系为 EPSG:4326
    all_results = []

    # 计算总边界
    total_bounds = gdf.total_bounds

    rows = int((total_bounds[3] - total_bounds[1]) / chunk_size) + 1
    cols = int((total_bounds[2] - total_bounds[0]) / chunk_size) + 1

    for i in range(rows):
        for j in range(cols):
            xmin = total_bounds[0] + j * chunk_size
            ymin = total_bounds[1] + i * chunk_size
            xmax = xmin + chunk_size
            ymax = ymin + chunk_size

            # 创建当前块的边界
            current_bounds = (xmin, ymin, xmax, ymax)
            # 每一块生成格子
            grid_gdf = create_grid(current_bounds, grid_size, gdf.crs)
            # 格子与目标相交
            intersected = gpd.sjoin(grid_gdf, gdf, predicate='intersects')

            if not intersected.empty:
                all_results.append(intersected)

    if all_results:
        return gpd.GeoDataFrame(pd.concat(all_results, ignore_index=True))
    else:
        return gpd.GeoDataFrame()  # 返回空的 GeoDataFrame


def process_shapefiles(input_folder, output_folder, grid_size, chunk_size):
    for root, dirs, files in os.walk(input_folder):
        for file in files:
            if file.endswith('.shp'):
                province_name = os.path.basename(root)
                shp_path = os.path.join(root, file)

                # 读取 shapefile 数据
                gdf = gpd.read_file(shp_path)

                # 分块处理 shapefile
                result_gdf = process_in_chunks(gdf, grid_size, chunk_size)

                # 创建输出文件夹路径
                province_output_folder = os.path.join(output_folder, province_name)
                os.makedirs(province_output_folder, exist_ok=True)

                # 保存结果
                output_shp_path = os.path.join(province_output_folder, file)
                if not result_gdf.empty:
                    result_gdf.to_file(output_shp_path)
                    print(f"Processed and saved: {output_shp_path}")
                else:
                    print(f"No intersections found for {file}. No file saved.")


def main():
    # 输入和输出文件夹路径
    input_folder = r'I:\APV\11'
    output_folder = r'I:\APV\12'
    grid_size = 0.005
    chunk_size = 1  # 调整分块大小

    process_shapefiles(input_folder, output_folder, grid_size, chunk_size)


if __name__ == "__main__":
    main()
