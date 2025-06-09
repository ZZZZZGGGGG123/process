import numpy as np
import matplotlib.pyplot as plt

# 模拟训练过程的轮次（epochs）
epochs = np.arange(1, 51)

# 模拟损失值（loss）和精度（accuracy）的变化
# 使用平滑的曲线（指数衰减）来减少震荡，并加上少量噪声
loss = np.exp(-epochs / 10) + 0.02 * np.random.randn(50)  # 更小的噪声以确保平稳
accuracy = 50 + 0.5 * epochs + 0.5 * np.random.randn(50)  # 精度逐渐上升，加入较小噪声

# 绘图
fig, ax1 = plt.subplots(figsize=(8, 6))

# 绘制损失曲线
ax1.set_xlabel('Epochs')
ax1.set_ylabel('Loss', color='tab:blue')
ax1.plot(epochs, loss, color='tab:blue', label='Loss')
ax1.tick_params(axis='y', labelcolor='tab:blue')

# 创建共享y轴的第二个坐标轴来绘制精度曲线
ax2 = ax1.twinx()
ax2.set_ylabel('Accuracy', color='tab:red')
ax2.plot(epochs, accuracy, color='tab:red', label='Accuracy')
ax2.tick_params(axis='y', labelcolor='tab:red')

# 标题和图例
plt.title('Training Loss and Accuracy Over Epochs')
fig.tight_layout()

# 保存为高质量图像（1000 DPI）
plt.savefig('./', dpi=1000)

# 显示图像
plt.show()
