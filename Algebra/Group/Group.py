import numpy as np


class Group:
    def __init__(self,N,table):
        self.N = N
        self.product_matrix=np.array(table,dtype=object)
        self.element_vector=np.array(N,dtype=object)
        self._index_product_matrix=np.zeros_like(table,dtype=int)
        for index_tuple_iter,element_iter in np.ndenumerate(self.product_matrix):
            index_temp=np.argwhere(self.element_vector==element_iter)[0][0]
            self._index_product_matrix[index_tuple_iter]=index_temp


    #%%  USER：群乘法
    def product(self,*args):
        index_0=np.argwhere(self.element_vector==args[0])[0][0]
        index_1=np.argwhere(self.element_vector==args[1])[0][0]
        index_result=self._index_product_matrix[index_0,index_1]
        for i in range(2,len(args)):
            index_temp=tuple(np.argwhere(self.element_vector==args[i])[0])
            index_result=self._index_product_matrix[index_result,index_temp]
        result=self.element_vector[index_result]
        return result


    #%%  USER：检查群乘法是否满足公设
    def check(self):
        ##  检查群的封闭性，单位元存在性和逆元存在性
        for i in range(self.product_matrix.shape[0]):
            check_vector=np.zeros(self.N)
            for j in range(self.product_matrix.shape[1]):
                check_vector[self._index_product_matrix[i,j]]=1
            if np.all(check_vector==0):
                return False
        for j in range(self.N):
            check_vector=np.zeros(self.N)
            for i in range(self.N):
                check_vector[self._index_product_matrix[i, j]] = 1
            if np.all(check_vector == 0):
                return False

        ##  检查群的结合律
        for i in self.N:
            for j in self.N:
                for k in self.N:
                    index_ij=self._index_product_matrix[i,j]
                    index_jk=self._index_product_matrix[j,k]
                    index_ij_k=self._index_product_matrix[index_ij,k]
                    index_i_jk=self._index_product_matrix[i,index_jk]
                    if index_ij_k!=index_i_jk:
                        return False

        ##  都满足的情况下检查通过
        return True

