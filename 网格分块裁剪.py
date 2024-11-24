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

def intersect_with_grid(shapefile, grid_size):
    gdf = gpd.read_file(shapefile)
    gdf = gdf.to_crs(epsg=4326)  # 转换为 EPSG:4326

    bounds = gdf.total_bounds

    # 创建网格
    grid_gdf = create_grid(bounds, grid_size, gdf.crs)

    # 进行空间连接
    joined = gpd.sjoin(grid_gdf, gdf, op='intersects')

    # 保留与输入多边形相交的完整格子
    complete_grid_gdf = grid_gdf[grid_gdf.index.isin(joined.index)]

    return complete_grid_gdf

# 传递三个参数：grid_size 是网格大小，chunk_size 是分块大小
def process_in_chunks(shapefile, grid_size, chunk_size):
    gdf = gpd.read_file(shapefile)
    gdf = gdf.to_crs(epsg=4326)  # 在这里转换坐标系为 EPSG:4326
    print("坐标投影是", gdf.crs)

    all_results = []

    # 计算总边界
    total_bounds = gdf.total_bounds

    # 打印整块的大小
    print("Total bounds:", total_bounds)
    print("Height of the area:", total_bounds[3] - total_bounds[1])
    print("Width of the area:", total_bounds[2] - total_bounds[0])

    # 按照块进行处理
    rows = int((total_bounds[3] - total_bounds[1]) / chunk_size) + 1
    cols = int((total_bounds[2] - total_bounds[0]) / chunk_size) + 1
    print("Number of rows:", rows)
    print("Number of columns:", cols)
    print("Number of total:", cols*rows)
    # 按照块进行处理
    for i in range(int((total_bounds[3] - total_bounds[1]) / chunk_size) + 1):
        print("当前是第:" + str(i) + "块")
        for j in range(int((total_bounds[2] - total_bounds[0]) / chunk_size) + 1):
            xmin = total_bounds[0] + j * chunk_size
            ymin = total_bounds[1] + i * chunk_size
            xmax = xmin + chunk_size
            ymax = ymin + chunk_size

            # 创建当前块的边界
            current_bounds = (xmin, ymin, xmax, ymax)
            # 每一个块生成格子
            grid_gdf = create_grid(current_bounds, grid_size, gdf.crs)
            # 格子与目标相交
            intersected = gpd.sjoin(grid_gdf, gdf, predicate='intersects')

            # 收集结果
            if not intersected.empty:
                all_results.append(intersected)

    if all_results:
        final_result = gpd.GeoDataFrame(pd.concat(all_results, ignore_index=True))
        return final_result
    else:
        return gpd.GeoDataFrame()  # 返回空的 GeoDataFrame

def main():
    input_shapefile = r'I:\APV\噪声过滤后.shp'
    grid_size = 0.005
    chunk_size = 1  # 可以根据需要调整分块大小
    result = process_in_chunks(input_shapefile, grid_size, chunk_size)

    if not result.empty:
        result.to_file(r'I:\APV\网格化裁剪后.shp')
        print("File has been saved.")
    else:
        print("No intersections found. No file saved.")

if __name__ == "__main__":
    main()
