import numpy as np
import matplotlib.pyplot as plt
from scipy.linalg import svd

# 创建 DMD 函数
def DMD(X, Y, r):
    """
    使用 DMD 对数据进行分解
    X: 数据矩阵，t时刻
    Y: 数据矩阵，t+1时刻
    r: 截断的奇异值数量，决定模型的秩
    """
    # Step 1: SVD 分解 X
    U, S, Vh = svd(X, full_matrices=False)
    
    # Step 2: 截断矩阵
    U_r = U[:, :r]
    S_r = np.diag(S[:r])
    V_r = Vh.conj().T[:, :r]
    
    # Step 3: 计算近似 A 矩阵
    A_tilde = U_r.conj().T @ Y @ V_r @ np.linalg.inv(S_r)
    
    # Step 4: 特征值分解
    eigenvalues, eigenvectors = np.linalg.eig(A_tilde)
    
    # Step 5: 计算 DMD 模态
    Phi = Y @ V_r @ np.linalg.inv(S_r) @ eigenvectors
    
    return eigenvalues, Phi

# 生成一串随时间变化的拥堵指数数据（模拟数据）
np.random.seed(0)
t = np.linspace(0, 10, 100)
congestion_index = 5 + 2 * np.sin(2 * np.pi * t / 5) + 0.2 * np.random.randn(len(t))

# 可视化原始数据
plt.plot(t, congestion_index, label="Congestion Index (Raw)")
plt.title("Highway Congestion Index Over Time")
plt.xlabel("Time")
plt.ylabel("Congestion Index")
plt.legend()
plt.show()

#
