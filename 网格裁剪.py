import geopandas as gpd
from shapely.geometry import box

def create_grid(shapefile, grid_size):
    gdf = gpd.read_file(shapefile)
    print("Loaded GeoDataFrame:", gdf.head())  # 打印加载的数据头部信息
    print("原始坐标投影是", gdf.crs)
    
    bounds = gdf.total_bounds
    xmin, ymin, xmax, ymax = bounds

    rows = int((ymax - ymin) / grid_size)
    cols = int((xmax - xmin) / grid_size)

    print("Total bounds:", bounds)
    print("Height of the area:", bounds[3] - bounds[1])
    print("Width of the area:", bounds[2] - bounds[0])

    print("Number of rows:", rows)
    print("Number of columns:", cols)

    grid = []
    for i in range(rows):
        for j in range(cols):
            minx = xmin + j * grid_size
            miny = ymin + i * grid_size
            maxx = minx + grid_size
            maxy = miny + grid_size
            grid.append(box(minx, miny, maxx, maxy))
    
    grid_gdf = gpd.GeoDataFrame(grid, columns=['geometry'], crs=gdf.crs)
    print("Created grid GeoDataFrame:", grid_gdf.head())  # 打印创建的网格的头部信息
    return grid_gdf

def intersect_with_grid(shapefile, grid_size):
    grid_gdf = create_grid(shapefile, grid_size)
    gdf = gpd.read_file(shapefile)
     # 进行空间连接
    joined = gpd.sjoin(grid_gdf, gdf, op='intersects')
    
    # 保留与输入多边形相交的完整格子
    complete_grid_gdf = grid_gdf[grid_gdf.index.isin(joined.index)]
    
    print("Complete grid GeoDataFrame:", complete_grid_gdf.head())
    return complete_grid_gdf

def main():
    #输入
    input_shapefile = r'I:\APV\噪声过滤后\台湾\台湾.shp'
    grid_size = 0.005
    result = intersect_with_grid(input_shapefile, grid_size)
    if not result.empty:
        #输出
        result.to_file(r'I:\APV\网格化裁剪后\test\台湾.shp')
        print("File has been saved.")
    else:
        print("No intersections found. No file saved.")

if __name__ == "__main__":
    main()
