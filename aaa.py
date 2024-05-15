import matplotlib.pyplot as plt

# 准备数据
x = [1, 2, 3, 4, 5]  # x轴数据
y = [10, 15, 13, 18, 16]  # y轴数据

# 使用plt.plot()函数绘制折线图
plt.plot(x, y)

# 添加标题和标签（可选）
plt.title('折线图示例')
plt.xlabel('X轴标签')
plt.ylabel('Y轴标签')

# 显示图形
plt.show()
