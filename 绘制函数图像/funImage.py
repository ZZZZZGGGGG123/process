import numpy as np
import matplotlib.pyplot as plt

# 定义 sigmoid 函数
def sigmoid(x):
    return 1 / (1 + np.exp(-x))

# 生成 x 值数据
x = np.linspace(-5, 5, 400)
y_sigmoid = sigmoid(x)

# 绘制图像
plt.figure(figsize=(8, 6))
plt.plot(x, y_sigmoid, label='Sigmoid Function')
plt.title('Sigmoid', fontsize=18, fontweight='bold')
plt.xlabel('Input (x)', fontsize=18)
plt.ylabel('y', fontsize=18)
plt.grid(True, linestyle='--', alpha=0.9)
plt.legend()
plt.show()

# 保存图像
plt.savefig('sigmoid.png', dpi=1000)  # 调整 dpi 提高清晰度
