import numpy as np
import matplotlib.pyplot as plt

# 定义 tanh 函数
def tanh(x):
    return np.tanh(x)

# 生成 x 值数据
x = np.linspace(-5, 5, 400)
y_tanh = tanh(x)

# 绘制图像
plt.figure(figsize=(8, 6))
plt.plot(x, y_tanh, label='Tanh Function')
plt.title('Tanh', fontsize=18, fontweight='bold')
plt.xlabel('Input (x)', fontsize=18)
plt.ylabel('y', fontsize=18)
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend()
plt.show()

# 保存图像
plt.savefig('tanh.png', dpi=1000)  # 调整 dpi 提高清晰度
