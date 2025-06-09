import numpy as np
import matplotlib.pyplot as plt

def relu(x):
    return np.maximum(0, x)

# 生成 x 值数据
x = np.linspace(-5, 5, 400)
y_relu = relu(x)

# 绘制图像
plt.figure(figsize=(8, 6))
plt.plot(x, y_relu, label='ReLU Function')
plt.title('ReLU', fontsize=20, fontweight='bold')
plt.xlabel('Input (x)', fontsize=18)
plt.ylabel('y', fontsize=18)
plt.grid(True, linestyle='--', alpha=0.9)
plt.legend()
plt.show()

# 保存图像
plt.savefig('relu.png', dpi=1000)  # 调整 dpi 提高清晰度
