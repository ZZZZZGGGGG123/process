import geopandas as gpd
from shapely.geometry import box

def create_grid(shapefile, grid_size):
    gdf = gpd.read_file(shapefile)
    print("Loaded GeoDataFrame:", gdf.head())  # 打印加载的数据头部信息
    
    bounds = gdf.total_bounds
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
    input_shapefile = r'D:\shapefileceshi\in\jiangsuwater.shp'
    grid_size = 0.005
    result = intersect_with_grid(input_shapefile, grid_size)
    if not result.empty:
        result.to_file(r'D:\shapefileceshi\out6\output_shapefile.shp')
        print("File has been saved.")
    else:
        print("No intersections found. No file saved.")

if __name__ == "__main__":
    main()
