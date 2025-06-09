import numpy as np
import matplotlib.pyplot as plt

def softmax(x):
    e_x = np.exp(x - np.max(x))  # 防止溢出
    return e_x / e_x.sum(axis=0)

# 生成 x 值数据
x = np.linspace(-5, 5, 400).reshape(-1, 1)  # 转换为二维数组
y_softmax = softmax(x)

# 绘制图像
plt.figure(figsize=(8, 6))
plt.plot(x, y_softmax, label='Softmax Function')
plt.title('Softmax', fontsize=20, fontweight='bold')
plt.xlabel('Input (x)', fontsize=18)
plt.ylabel('y', fontsize=18)
plt.axhline(0, color='black', linewidth=0.5)
plt.axvline(0, color='black', linewidth=0.5)
plt.grid(True, linestyle='--', alpha=0.9)
plt.legend()
plt.show()

# 保存图像
plt.savefig('softmax.png', dpi=1000)  # 调整 dpi 提高清晰度