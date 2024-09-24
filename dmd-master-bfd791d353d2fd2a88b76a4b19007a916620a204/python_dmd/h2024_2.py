import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.linalg import svd

# 读取 Excel 文件
file_path = '103_totalV2.xlsx'
df = pd.read_excel(file_path)

# 提取数据列
time = df['时间（s）']
avg_speed = df['平均车速（km/h）']
total_flow = df['总车流量']
emergency_flow = df['应急车道车流量']
congestion_index = df['拥堵系数']

# 创建输入数据矩阵 X，将相关列组合在一起
X = np.vstack([avg_speed, total_flow, emergency_flow, congestion_index])

# 构建 Hankel 矩阵
def construct_hankel_matrix(data, rows, cols):
    """构造 Hankel 矩阵"""
    n = data.shape[1]  # 时间序列的长度
    if rows + cols - 1 > n:
        raise ValueError("数据长度不足以构造该大小的 Hankel 矩阵")
    
    hankel_matrix = np.zeros((rows, cols))
    for i in range(rows):
        hankel_matrix[i, :] = data[:, i:i+cols].flatten()
    
    return hankel_matrix

# 定义 Hankel 矩阵的行数和列数
rows = 4  # 我们有四个特征：平均车速、总车流量、应急车道车流量、拥堵指数
cols = 10  # 预测十分钟后的数据

H = construct_hankel_matrix(X, rows, cols)

# 动态模态分解 (DMD) - 基于 Hankel 矩阵
def dmd(X1, X2, r):
    """基于 SVD 的动态模态分解"""
    U, S, Vh = svd(X1, full_matrices=False)
    
    # 截断 SVD，只保留 r 个模态
    Ur = U[:, :r]
    Sr = np.diag(S[:r])
    Vr = Vh.conj().T[:, :r]
    
    # 计算 A 矩阵
    A_tilde = Ur.T @ X2 @ Vr @ np.linalg.inv(Sr)
    
    # 特征值分解 A 矩阵
    eigenvalues, eigenvectors = np.linalg.eig(A_tilde)
    
    # 计算 DMD 模态
    Phi = X2 @ Vr @ np.linalg.inv(Sr) @ eigenvectors
    
    return eigenvalues, Phi

# 定义用于 DMD 的 X1 和 X2
X1 = H[:, :-1]  # 当前时刻的 Hankel 矩阵
X2 = H[:, 1:]   # 下一时刻的 Hankel 矩阵

# 执行 DMD
r = 2  # 保留 2 个主导模态（可以根据数据调整）
eigenvalues, Phi = dmd(X1, X2, r)

# 预测未来十分钟的拥堵指数
dt = time[1] - time[0]  # 时间步长
omega = np.log(eigenvalues) / dt  # 频率

# 初始状态
x0 = H[:, 0]

# 预测未来十分钟
future_steps = 10
future_states = np.zeros((r, future_steps), dtype=complex)

for i in range(future_steps):
    future_states[:, i] = x0 * np.exp(omega * (i+1) * dt)

# 预测拥堵指数
predicted_congestion_index = Phi @ future_states

# 可视化结果
plt.figure(figsize=(10, 6))
plt.plot(time[:len(congestion_index)], congestion_index, label='实际拥堵指数')
plt.plot(time[:len(congestion_index)], predicted_congestion_index.real.flatten(), label='DMD 预测拥堵指数', linestyle='--')
plt.xlabel('时间 (s)')
plt.ylabel('拥堵指数')
plt.title('DMD 预测与实际拥堵指数的比较')
plt.legend()
plt.grid(True)
plt.show()
