import galois
import numpy as np


def orthogonal_null_space_basis(H_matrix):
    """求解与H行向量线性无关、在零空间中且彼此正交的基矢"""
    GF = galois.GF(2)
    H = GF(H_matrix)

    # 计算行空间基矢
    row_reduced = H.row_reduce()
    row_basis = row_reduced[~np.all(row_reduced == 0, axis=1)]

    # 计算原始零空间基矢
    null_space = H.null_space()

    # 筛选与行空间无关的基矢
    filtered = []
    for vec in null_space:
        extended = np.vstack([row_basis, vec])
        if np.linalg.matrix_rank(extended) > np.linalg.matrix_rank(row_basis):
            filtered.append(vec)

    # 正交化过程
    ortho_basis = []
    for vec in filtered:
        # 复制向量以避免修改原始数据
        v = vec.copy()

        # 对现有正交基矢进行正交化
        for u in ortho_basis:
            dot_product = np.dot(v, u)
            if dot_product:
                v += u  # GF(2)中的加法等价于异或

        # 验证有效性
        if not np.all(v == 0):  # 非零验证
            # 再次检查与行空间的独立性
            ext_verify = np.vstack([row_basis, v])
            if np.linalg.matrix_rank(ext_verify) > np.linalg.matrix_rank(row_basis):
                # 检查与已有基矢的正交性
                is_ortho = all(np.dot(v, u) == 0 for u in ortho_basis)
                if is_ortho:
                    ortho_basis.append(v)

    return GF(ortho_basis)


# 验证示例
if __name__ == "__main__":
    # 案例1：标准正交情况
    H1 = [[0, 1, 1,0,0,0],
          [0, 0, 0, 1, 1, 0]]
    print("案例1结果：")
    print(orthogonal_null_space_basis(H1))

    # 案例2：需要正交化调整
    H2 = [[1, 0, 1, 1],
          [0, 1, 1, 0]]
    print("\n案例2结果：")
    print(orthogonal_null_space_basis(H2))

    # 案例3：多维度正交化
    H3 = [[1, 1, 0, 0, 0],
          [0, 0, 1, 1, 0]]
    print("\n案例3结果：")
    print(orthogonal_null_space_basis(H3))