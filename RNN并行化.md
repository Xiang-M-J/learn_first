这是一个基于 PyTorch 的 **Parallel Scan**（并行扫描）实现示例。

线性递归$h_t=a_th_{t-1}+b_t$可以写成非递归的形式，从而通过**“对数空间累积求和” (Log-Space Cumulative Sum)** 的技巧来实现，这是在纯 PyTorch 中（不编写 CUDA 代码）实现线性递归并行化的常用数学技巧。

下面是公式推导
$$
\eqalign{
  & {h_t} = (1 - {z_t}) \cdot {h_{t - 1}} + {z_t} \cdot {{\tilde h}_t} = {\alpha _t}{h_{t - 1}} + {b_t}  \cr 
  &  = {\alpha _t}\left( {{\alpha _{t - 1}}{h_{t - 1}} + {b_{t - 1}}} \right) + {b_t} = {\alpha _t}{\alpha _{t - 1}}{h_{t - 1}} + {\alpha _t}{b_{t - 1}} + {b_t}  \cr 
  &  \cdots   \cr 
  &  = \sum\limits_{i = 1}^t {{b_i}\prod\limits_{j = i + 1}^t {{\alpha _j}} }  = \sum\limits_{i = 1}^t {{b_i}{e^{\log \left( {\prod\limits_{j = i + 1}^t {{\alpha _j}} } \right)}}}   \cr 
  &  = \sum\limits_{i = 1}^t {{b_i}{e^{\sum\limits_{j = i + 1}^t {\log {\alpha _j}} }}}  = \sum\limits_{i = 1}^t {{b_i}{e^{\sum\limits_{j = 1}^t {\log {\alpha _j}}  - \sum\limits_{j = 1}^i {\log {\alpha _j}} }}}   \cr 
  &  = \sum\limits_{i = 1}^t {{b_i}{e^{\sum\limits_{j = 1}^t {\log {\alpha _j}} }}{e^{ - \sum\limits_{j = 1}^i {\log {\alpha _j}} }}}  = {e^{\sum\limits_{j = 1}^t {\log {\alpha _j}} }}\sum\limits_{i = 1}^t {{b_i}{e^{ - \sum\limits_{j = 1}^i {\log {\alpha _j}} }}}   \cr 
  &  = {e^{{L_t}}}\sum\limits_{i = 1}^t {{b_i}} {e^{ - {L_i}}} \cr}
$$
$L_t=\sum_{j=1}^t \log \alpha_j$ 可以直接计算，$L_i=\sum_{j=1}^i \log \alpha_j$则可以使用torch.cumsum实现，GPU 上的 cumsum（前缀和）是高度优化的并行操作（耗时 $O(\log N)$），而 Python 的 for 循环是串行的 $O(N)$。

mingru实现时参考了 [glassroom/heinsen_sequence: Code implementing "Efficient Parallelization of a Ubiquitious Sequential Computation" (Heinsen, 2023)](https://github.com/glassroom/heinsen_sequence)



### PyTorch 代码实现



```python
import torch
import time

def parallel_scan_pytorch(a, x):
    """
    使用 PyTorch 原生算子实现的并行扫描。
    公式: h_t = a_t * h_{t-1} + x_t
    
    参数:
        a: 衰减项/门控 (Batch, Seq_Len, Dim), 范围通常在 (0, 1) 之间
        x: 输入项 (Batch, Seq_Len, Dim)
    返回:
        h: 隐藏状态序列 (Batch, Seq_Len, Dim)
    """
    # 1. 将乘法转换为对数空间的加法
    # 为了防止 log(0)，通常加一个极小值，或者假设 a 已经被 sigmoid 处理过且 > 0
    log_a = torch.log(a.clamp(min=1e-8)) 
    
    # 2. 计算 log_a 的前缀和 (Parallel Step 1)
    # L_t = sum_{i=1}^t log(a_i)
    acc_log_a = torch.cumsum(log_a, dim=1)
    
    # 3. 准备累积项
    # 根据公式推导: h_t = exp(L_t) * cumsum( x_k * exp(-L_k) )
    # 我们需要计算 x_k * exp(-L_k)
    term_to_sum = x * torch.exp(-acc_log_a)
    
    # 4. 计算加权输入的累积和 (Parallel Step 2)
    summed_terms = torch.cumsum(term_to_sum, dim=1)
    
    # 5. 恢复结果
    h = torch.exp(acc_log_a) * summed_terms
    
    return h

def sequential_scan_loop(a, x):
    """
    传统的串行实现 (用于验证正确性)
    """
    batch, seq_len, dim = x.shape
    h = torch.zeros_like(x)
    h_prev = torch.zeros((batch, dim), device=x.device)
    
    for t in range(seq_len):
        # h_t = a_t * h_{t-1} + x_t
        h_t = a[:, t, :] * h_prev + x[:, t, :]
        h[:, t, :] = h_t
        h_prev = h_t
        
    return h

# --- 测试与验证 ---

# 设置参数
B, L, D = 2, 1024, 64  # Batch=2, Length=1024, Dim=64
device = 'cuda' if torch.cuda.is_available() else 'cpu'

print(f"运行设备: {device}")

# 随机初始化数据
# a 通常经过 Sigmoid 变为 (0, 1) 之间
gates = torch.sigmoid(torch.randn(B, L, D, device=device))
tokens = torch.randn(B, L, D, device=device)

# 1. 运行串行版
start = time.time()
res_seq = sequential_scan_loop(gates, tokens)
print(f"串行耗时: {time.time() - start:.4f}s")

# 2. 运行并行版
start = time.time()
res_par = parallel_scan_pytorch(gates, tokens)
print(f"并行耗时: {time.time() - start:.4f}s")

# 3. 验证结果一致性
# 由于浮点数精度误差，我们允许微小的差异 (1e-5)
diff = (res_seq - res_par).abs().max()
print(f"最大误差: {diff:.6f}")

if diff < 1e-4:
    print("✅ 验证通过：并行实现与串行逻辑结果一致！")
else:
    print("❌ 验证失败：误差过大。")
```

### 代码解析

1. **数学推导的对应关系**：
   - `acc_log_a` 对应推导中的 $L_t$。
   - `term_to_sum` 对应推导中的 $x_k / \exp(L_k)$。
   - 最后相乘对应 $\exp(L_t) \times \sum (...)$。

2. **性能差异**：

   - 当序列长度 $L$ 很短（如 32, 64）时，串行和并行差别不大。
   - 当序列长度 $L$ 很长（如 2048, 4096 或更长）时，并行版会比 Python 循环版快几个数量级。



### 注意事项 (工业级实现)



虽然上面的代码展示了并行化的原理，但在实际的工业级模型（如 Mamba, RWKV, MGRU）中，通常不会直接使用上述纯 PyTorch 代码，原因如下：

1. **数值稳定性**：当序列非常长时，`exp(cumsum)` 可能会导致数值溢出（inf）或下溢（0）。
2. **显存占用**：上述方法需要保存完整的中间变量 `acc_log_a` 和 `summed_terms`，显存占用是 $O(N \times D)$。

解决方案：

实际的高性能库（如 mamba-ssm 或 flash-linear-attention）会使用 Triton 或 CUDA 编写定制的 Kernel。它们会在 GPU 的 SRAM（高速缓存）中进行分块计算（Chunked Scan），既能保持并行速度，又能极大地减少显存读写。

**您是否需要了解如何编写一个简单的 Triton Kernel 来进一步优化这个过程？**





