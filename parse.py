import pandas as pd
import matplotlib.pyplot as plt
import matplotlib

# 设置字体为 SimHei (黑体)
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用于正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False    # 用于正常显示负号


# 读取 Excel 文件
file_path = '103_totalV2.xlsx'
df = pd.read_excel(file_path)

# 显示前几行数据
print("前几行数据：")
print(df.head())

# 基本描述性统计信息
print("\n描述性统计信息：")
print(df.describe())

# 数据列的命名
time = df['时间（s）']
total_flow = df['总车流量']
emergency_flow = df['应急车道车流量']
avg_speed = df['平均车速（km/h）']
congestion_index = df['拥堵系数']

# 数据可视化
# 1. 总车流量随时间的变化
plt.figure(figsize=(10, 6))
plt.plot(time, total_flow, label='总车流量', color='b')
plt.xlabel('时间（秒）')
plt.ylabel('总车流量')
plt.title('总车流量随时间的变化')
plt.legend()
plt.grid(True)
plt.show()

# 2. 拥堵系数随时间的变化
plt.figure(figsize=(10, 6))
plt.plot(time, congestion_index, label='拥堵系数', color='r')
plt.xlabel('时间（秒）')
plt.ylabel('拥堵系数')
plt.title('拥堵系数随时间的变化')
plt.legend()
plt.grid(True)
plt.show()

# 3. 应急车道车流量随时间的变化
plt.figure(figsize=(10, 6))
plt.plot(time, emergency_flow, label='应急车道车流量', color='g')
plt.xlabel('时间（秒）')
plt.ylabel('应急车道车流量')
plt.title('应急车道车流量随时间的变化')
plt.legend()
plt.grid(True)
plt.show()

# 4. 平均车速随时间的变化
plt.figure(figsize=(10, 6))
plt.plot(time, avg_speed, label='平均车速（km/h）', color='m')
plt.xlabel('时间（秒）')
plt.ylabel('平均车速 (km/h)')
plt.title('平均车速随时间的变化')
plt.legend()
plt.grid(True)
plt.show()






# 提取平均车速和总车流量的列
avg_speed = df['平均车速（km/h）']
total_flow = df['总车流量']

# 画出车速和车流量的散点图
plt.figure(figsize=(10, 6))
plt.scatter(avg_speed, total_flow, color='blue', alpha=0.6)
plt.xlabel('平均车速 (km/h)')
plt.ylabel('总车流量')
plt.title('车速与车流量的关系')
plt.grid(True)
plt.show()