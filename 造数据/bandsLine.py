import numpy as np
import matplotlib.pyplot as plt

# 模拟数据：150个采样点
num_points = 150

# # 模拟B11波段反射率：假设水光伏的反射率较高，水体和浅滩较低
# water_fpv = 500+1450+ 50 * np.random.randn(num_points)  # 水光伏，均值偏高，带有少量噪声
# water = 500+1380 + 50 * np.random.randn(num_points)  # 水体，均值偏低，带有较大噪声
# sandbar = 500+1400 + 50 * np.random.randn(num_points)  # 浅滩，较低且波动较大
# # NDVI
# 模拟NDVI反射率：假设水光伏的NDVI较高，水体和浅滩较低
water = 0.3 + 0.1 * np.random.randn(num_points)  # 水体，均值偏低，带有较大噪声
water_fpv = 0.7 + 0.15 * np.random.randn(num_points)  # 水光伏，均值偏高，带有少量噪声
sandbar = 0.45 + 0.15 * np.random.randn(num_points)  # 浅滩，较低且波动较大
# 绘制B11波段的图表
plt.figure(figsize=(10, 6))

# 绘制水光伏折线（带点）
plt.plot(range(1, num_points + 1), water_fpv, label='Water FPV', color='tab:Red', linestyle='-', marker='o', markersize=4, linewidth=2)
# 绘制水体折线（带点）
plt.plot(range(1, num_points + 1), water, label='Water', color='tab:green', linestyle='--', linewidth=2)
plt.plot(range(1, num_points + 1), sandbar, label='Sandbar', color='tab:orange', linestyle='-.', linewidth=2)

# 图表设置
plt.title('Reflectance of NDWI Band for Water FPV, Water, and Sandbar',size=18)
plt.xlabel('Sampling Point Number',size=18)
plt.ylabel('B11 Band Reflectance',size=18)
plt.legend(title='Categories')
plt.grid(True)
plt.tight_layout()

# 保存为高分辨率图像（1000 DPI）
plt.savefig('./', dpi=1000)

# 显示图表
plt.show()
