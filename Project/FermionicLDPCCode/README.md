# Construction for Fermionic Quantum LDPC Code

## 1 映射链
考虑一个从一个qubit稳定子编码到Fermionic稳定子编码的映射链。

### 1.1 第一层映射

第一层映射是$[n,k,d]\rightarrow[2n,k,2d]_f$，这里从一个qubit稳定子编码映射到了一个Majorana Fermionic code。我们定义稳定子编码的稳定子为$\{\hat S_n\}$，每个qubit上的算符是$\hat X$或$\hat Z$。再考虑映射到的Majorana Fermionic code，它上面有$2n$个Fermions，它的稳定子由两部分组成，第一部分是从$\{\hat S_n\}$映射来的。

$$
\begin{equation}
\begin{cases}
\hat X_j\rightarrow\hat\gamma_{j}\hat\gamma_{j+3}\\
\hat Z_j\rightarrow\hat\gamma_{j+2}\hat\gamma_{j+3}
\end{cases}
\end{equation}
$$

此外还要补充一部分稳定子，对应每一个原来的qubit，我们定义下面的稳定子。

$$
\begin{equation}
\hat S_j=\hat\gamma_{j}\hat\gamma_{j+1}\hat\gamma_{j+2}\hat\gamma_{j+3}
\end{equation}
$$

### 1.2 第二层映射

第二层映射是$[n,k,d]_f\rightarrow[2n,2k,2d]$，这里从一个Majorana Fermionic code映射到了一个self-dual CSS code。从稳定子的角度，我们用下面的映射定义CSS code的稳定子，考虑稳定子$\hat S$在Majorana Fermionic code稳定子中，我们将它映射为两个CSS code稳定子。

$$
\begin{equation}
\begin{cases}
\hat\gamma_j\rightarrow\hat X_j\\
\hat\gamma_j\rightarrow\hat Z_j
\end{cases}
\end{equation}
$$

例如$\hat S=\hat\gamma_0\hat\gamma_2$，映射结果是$\hat S_X=\hat X_0\hat X_2$和$\hat S_Z=\hat Z_0\hat Z_2$，由于引入的X-check和Z-check相同，这是一个self-dual CSS code。

### 1.3 第三层映射

第三层映射是$[n,k,d]\rightarrow[n,k,d]_f$，这里从一个self-dual CSS code映射为一个Majorana Fermionic code。从稳定子的角度，我们用下面的映射定义Majorana Fermionic code的稳定子，考虑稳定子$\hat S$在self-dual CSS code的稳定子中，我们将它映射如下。

$$
\begin{equation}
\begin{cases}
\hat X_j\rightarrow\hat\gamma_j\\
\hat Z_j\rightarrow\hat\gamma_{j+1}
\end{cases}
\end{equation}
$$

这里的两个Majorana算符不一定要是相邻的，只要两两配对即可。

## 2 问题

目前的问题是：这种构造方式从一个good quantum LDPC code出发能否得到一个good Fermionic LDPC code。



