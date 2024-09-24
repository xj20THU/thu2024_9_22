import numpy as np
from scipy.linalg import hankel, svd

# 构造 Hankel 矩阵
def construct_hankel_matrix(data, m, k):
    """ 构造 Hankel 矩阵 """
    return hankel(data[:m], data[m-1:m+k-1])

# 基于 Hankel 矩阵进行预测
def predict_hankel(data, m, k, p):
    """
    使用 Hankel 矩阵对未来 p 步进行预测
    data: 时间序列数据
    m: Hankel 矩阵的行数
    k: Hankel 矩阵的列数
    p: 预测步长
    """
    # Step 1: 构造 Hankel 矩阵
    H = construct_hankel_matrix(data, m, k)
    
    # Step 2: 对 Hankel 矩阵进行奇异值分解 (SVD)
    U, S, Vh = svd(H)
    
    # Step 3: 使用 SVD 提取系统状态
    # 可以选择截断某些奇异值（这里只保留所有的奇异值）
    r = len(S)
    U_r = U[:, :r]
    S_r = np.diag(S[:r])
    V_r = Vh[:r, :]
    
    # Step 4: 使用系统的状态预测未来的值
    future_states = []
    y_p = data[-m:]  # 使用最后 m 个数据点作为初始状态
    
    for i in range(p):
        # 预测未来的一个数据点
        y_next = U_r @ S_r @ V_r[:, 0]
        future_states.append(y_next[0])
        
        # 更新系统状态，移除第一个点，添加预测值
        y_p = np.append(y_p[1:], y_next[0])

        # 更新 Hankel 矩阵
        H = construct_hankel_matrix(y_p, m, k)
        U, S, Vh = svd(H)
        U_r = U[:, :r]
        S_r = np.diag(S[:r])
        V_r = Vh[:r, :]
    
    return np.array(future_states)

# 示例数据
data = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

# 设置 Hankel 矩阵的大小 (m, k)，并预测未来 5 个数据点
m = 3
k = 3
p = 5

# 进行预测
predicted_data = predict_hankel(data, m, k, p)

# 打印预测的结果
print("预测的未来数据: ", predicted_data)
