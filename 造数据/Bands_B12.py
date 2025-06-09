import numpy as np
import matplotlib.pyplot as plt


# 模拟数据：150个采样点
num_points = 150
# 模拟B12波段反射率：假设水光伏的反射率较高，水体和浅滩较低
water_fpv_b12 = 0.5 + 0.05 * np.random.randn(num_points)  # 水光伏，均值偏高，带有少量噪声
water_b12 = 0.3 + 0.1 * np.random.randn(num_points)  # 水体，均值偏低，带有较大噪声
sandbar_b12 = 0.2 + 0.15 * np.random.randn(num_points)  # 浅滩，较低且波动较大

# 绘制B12波段的图表
plt.figure(figsize=(10, 6))

plt.plot(range(1, num_points + 1), water_fpv_b12, label='Water FPV', color='tab:blue', linestyle='-', linewidth=2)
plt.plot(range(1, num_points + 1), water_b12, label='Water', color='tab:green', linestyle='--', linewidth=2)
plt.plot(range(1, num_points + 1), sandbar_b12, label='Sandbar', color='tab:orange', linestyle='-.', linewidth=2)

# 图表设置
plt.title('Reflectance of B12 Band for Water FPV, Water, and Sandbar')
plt.xlabel('Sampling Point Number')
plt.ylabel('B12 Band Reflectance')
plt.legend(title='Categories')
plt.grid(True)
plt.tight_layout()

# 保存为高分辨率图像（1000 DPI）
plt.savefig('./', dpi=2000)

# 显示图表
plt.show()
