

# Triton

Triton 提供了一种使用python进行gpu编程的方法，相比于直接使用CUDA更加方便

## 基础

Triton中使用 `triton.jit` 修饰核函数，核函数运行在设备（GPU）上，需要将数据提前送入设备中。

下面是两个向量相加的例子，核函数中接收的数据实际上都是以指针的形式送入，这样可以避免大量的内存操作。

```python
import torch

import triton
import triton.language as tl

DEVICE = torch.device("cuda:0")


@triton.jit
def add_kernel(x_ptr,  # 向量 x 的指针
               y_ptr,  # 向量 y 的指针
               output_ptr,  # 输出向量的指针
               n_elements,  # 向量的大小
               BLOCK_SIZE: tl.constexpr,  # 程序处理的大小（注意tl.constexpr不能少）
               ):
    # 通过pid确定目前程序运行到的位置，因为使用了一维grid，因此axis为0
    pid = tl.program_id(axis=0) 
    
    # pid 乘上 BLOCK_SIZE 即为当前程序处理的向量的起始位置 block_start
    block_start = pid * BLOCK_SIZE
    offsets = block_start + tl.arange(0, BLOCK_SIZE)
    # mask 用来保证内存操作不会超过边界
    mask = offsets < n_elements
    # 从 DRAM 中加载 x 和 y，
    # 当 n_elements 不是 BLOCK_SIZE 的整数倍，mask 可以用来处理多余的元素
    x = tl.load(x_ptr + offsets, mask=mask)
    y = tl.load(y_ptr + offsets, mask=mask)
    output = x + y
    # 将结果写回 DRAM.
    tl.store(output_ptr + offsets, output, mask=mask)

def add(x: torch.Tensor, y: torch.Tensor):
    # 预分配输出的空间
    output = torch.empty_like(x)
    assert x.device == DEVICE and y.device == DEVICE and output.device == DEVICE
    n_elements = output.numel()
    # grid 用来计算一共需要多少个块 meta 为参数
    grid = lambda meta: (triton.cdiv(n_elements, meta['BLOCK_SIZE']), )
    
    add_kernel[grid](x, y, output, n_elements, BLOCK_SIZE=1024)
    return output

torch.manual_seed(0)
size = 98432
x = torch.rand(size, device=DEVICE)
y = torch.rand(size, device=DEVICE)
output_triton = add(x, y)
```

为了测量程序运行时间和效率，可以使用自带的benchmark

对于benchmark函数，需要传入确定张量大小的形状（如下例中的 `size`），对于不变的维度，可以通过 `triton.testing.Benchmark` 中的 `args` 作为字典传入，对于改变的维度，可以在 `x_names` 中声明变量名（如下例中的 `x_names=['size']`），同时在 `x_vals` 中给出具体的值

```python
@triton.testing.perf_report(
    triton.testing.Benchmark(
        x_names=['size'], # 这里的参数对应下面x_vals中的具体值
        x_vals=[2**i for i in range(12, 28, 1)], # x_vals 为向量的大小
        x_log=True,  # x 轴是对数
        line_arg='provider',
        line_vals=['triton', 'torch'],
        line_names=['Triton', 'Torch'],
        styles=[('blue', '-'), ('green', '-')],
        ylabel='GB/s',
        plot_name='vector-add-performance', 
        args={},  # 这里
    ))

def benchmark(size, provider):
    x = torch.rand(size, device=DEVICE, dtype=torch.float32)
    y = torch.rand(size, device=DEVICE, dtype=torch.float32)
    quantiles = [0.5, 0.2, 0.8]
    if provider == 'torch':
        ms, min_ms, max_ms = triton.testing.do_bench(lambda: x + y, quantiles=quantiles)
    if provider == 'triton':
        ms, min_ms, max_ms = triton.testing.do_bench(lambda: add(x, y), quantiles=quantiles)
    gbps = lambda ms: 3 * x.numel() * x.element_size() * 1e-9 / (ms * 1e-3)
    return gbps(ms), gbps(max_ms), gbps(min_ms)

benchmark.run(print_data=True, show_plots=True)
```



## 例子


### Softmax

对于二维向量，softmax可以通过对每行进行softmax来实现加速，下面给出一个对单行进行softmax的核函数。

对于多维向量，为了能够准确找到每行的起始位置，需要获得张量当前行和下一行的相同列的元素之间的步长（该值可能和列数相等，也有可能不相等）

```python
import torch

import triton
import triton.language as tl
from triton.runtime import driver

DEVICE = torch.device("cuda:0")
# properties = driver

@triton.jit
def softmax_kernel(
    o_ptr, x_ptr, 
    input_row_stride,    # 输入行的stride，stride指从当前行跳到下一行的同列位置的步长
    output_row_stride, n_cols, BLOCK_SIZE: tl.constexpr
):
    # 当前的程序id即为索引的行
    row_idx = tl.program_id(0)
    # 行起始的位置为行数×行步长
    row_start_ptr = x_ptr + row_idx * input_row_stride
    
    col_offsets = tl.arange(0, BLOCK_SIZE)
    input_ptrs = row_start_ptr + col_offsets
    # 将一行数据加载进 SRAM, 因为 BLOCK_SIZE 可能会比 n_cols 大，加上mask，多出来的部分补上负无穷
    row = tl.load(input_ptrs, mask=col_offsets < n_cols, other=-float('inf'))
    
    # 处于数值稳定性的考虑，减去最大值
    row_minus_max = row - tl.max(row, axis=0)
    numerator = tl.exp(row_minus_max)
    denominator = tl.sum(numerator, axis=0)
    softmax_output = numerator / denominator
    # 将数据写回 DRAM
    output_row_start_ptr = o_ptr + row_idx * output_row_stride
    output_ptrs = output_row_start_ptr + col_offsets
    tl.store(output_ptrs, softmax_output, mask=col_offsets < n_cols)

def softmax(x):
    n_rows, n_cols = x.shape
    # block size 需要为大于 n_cols 的 2 的幂
    BLOCK_SIZE = triton.next_power_of_2(n_cols)

    num_warps = 4
    if BLOCK_SIZE >= 2048:
        num_warps = 8
    if BLOCK_SIZE >= 4096:
        num_warps = 16
    y = torch.empty_like(x)
    # 为每行分配一个block
    softmax_kernel[(n_rows,)](
        y,
        x,
        x.stride(0),
        y.stride(0),
        n_cols,
        num_warps=num_warps,
        BLOCK_SIZE=BLOCK_SIZE,
    )
    return y


torch.manual_seed(0)
x = torch.randn(1823, 781, device='cuda')
y_triton = softmax(x)
y_torch = torch.softmax(x, axis=1)
assert torch.allclose(y_triton, y_torch), (y_triton, y_torch)
```


### 矩阵相乘

一种思路是将一个矩阵的一行和另一个矩阵的一列相乘，假设矩阵 `a` 的大小为 $m\times n$，矩阵 `b` 的大小为 $n\times k$，则可以同时用 $m\times k$ 个块计算。

```python
import torch
from torch import Tensor

import triton
import triton.language as tl

@triton.jit
def matmul_kernel(a_ptr, b_ptr, c_ptr, 
                  a_row_stride, b_row_stride, b_col_stride, c_row_stride, c_col_stride, 
                  m, n, k,  block_size: tl.constexpr):
    x_pid = tl.program_id(0)
    y_pid = tl.program_id(1)
    
    a_offsets = tl.arange(0, block_size)
    a_ptrs = a_ptr + x_pid * a_row_stride + a_offsets  # 获取 a 矩阵的一行
    
    a = tl.load(a_ptrs, mask=a_offsets < n)
    
    b_offsets = tl.arange(0, block_size) * b_row_stride
    b_ptrs = b_ptr + y_pid * b_col_stride + b_offsets
    b = tl.load(b_ptrs, mask=b_offsets < n * b_row_stride)   # 获取 b 矩阵的一列
    
    c = tl.sum(a * b)   # 计算一行和一列的点乘
    
    c_offset = x_pid * c_row_stride + y_pid * c_col_stride  # 写入对应位置
    tl.store(c_ptr + c_offset, c, mask=c_offset < m * k)

def matmul(a: Tensor, b: Tensor):
    m, n = a.shape
    n, k = b.shape
    
    block_size = triton.next_power_of_2(n)
    
    c = torch.empty((m, k), device=a.device, dtype=a.dtype)
    
    matmul_kernel[(m, k)](a, b, c, a.stride(0), b.stride(0), b.stride(1), 
                          c.stride(0), c.stride(1), m, n, k, block_size)
    return c
    
x = torch.randn((256, 133), device="cuda",)
y = torch.randn((133, 256), device="cuda",)

z_triton = matmul(x, y)
z_torch = torch.matmul(x, y)

print(torch.allclose(z_torch, z_triton, atol=1e-2, rtol=0))
print((z_torch - z_triton).abs().max())
```

另外一种思路见 [triton/python/tutorials/03-matrix-multiplication.py at v2.1.0 · triton-lang/triton](https://github.com/triton-lang/triton/blob/v2.1.0/python/tutorials/03-matrix-multiplication.py)


### Dropout

Dropout的实现比较简单，类似向量相加的执行形式即可

需要注意 `tl.rand` 产生 0-1 的随机数，使用 `tl.where` 对部分元素置为0。

```python
import torch
from torch import Tensor
import triton
import triton.language as tl


@triton.jit
def dropout_kernel(x_ptr, o_ptr, seed, p, n_ele, block_size: tl.constexpr):
    pid = tl.program_id(0)
    offsets = pid * block_size + tl.arange(0, block_size)

    x = tl.load(x_ptr + offsets, mask=offsets < n_ele)
    random = tl.rand(seed, offsets)
    x_keep = random > p
    
    o = tl.where(x_keep, x / (1 - p), 0.0)
    tl.store(o_ptr+offsets, o, mask=offsets < n_ele)

def dropout(x, seed, p):
    output = torch.empty_like(x)
    n_ele = x.numel()
    grid = lambda meta: (triton.cdiv(n_ele, meta['block_size']), )
    
    dropout_kernel[grid](x, output, seed, p, n_ele, 128)
    
    return output
```


### ReLU 前向和后向

ReLU 的前向小于0的置零，可以用 `tl.maximun(0, x)` 实现，后向过程中，小于0的部分的导数置为零。

```python
@triton.jit
def relu_fwd_kernel(x_ptr, y_ptr, n_elements, BLOCK_SIZE: tl.constexpr):
    pid = tl.program_id(0)
    block_start = pid * BLOCK_SIZE
    offsets = block_start + tl.arange(0, BLOCK_SIZE)
    mask = offsets < n_elements

    x = tl.load(x_ptr + offsets, mask=mask)
    y = tl.where(x > 0, x, 0.0)
    tl.store(y_ptr + offsets, y, mask=mask)
    
@triton.jit
def relu_bwd_kernel(x_ptr, dy_ptr, dx_ptr, n_elements, BLOCK_SIZE: tl.constexpr):
    pid = tl.program_id(0)
    block_start = pid * BLOCK_SIZE
    offsets = block_start + tl.arange(0, BLOCK_SIZE)
    mask = offsets < n_elements

    x = tl.load(x_ptr + offsets, mask=mask)
    dy = tl.load(dy_ptr + offsets, mask=mask)
    dx = tl.where(x > 0, dy, 0.0)
    tl.store(dx_ptr + offsets, dx, mask=mask)

class TritonReLUFunction(torch.autograd.Function):
    @staticmethod
    def forward(ctx, x: torch.Tensor, block_size=1024):
        n_ele = x.numel()
        y = torch.empty_like(x)
        grid = lambda meta: (triton.cdiv(n_ele, meta['BLOCK_SIZE']), )
        
        relu_fwd_kernel[grid](x, y, n_ele, block_size)
        ctx.save_for_backward(x)
        ctx.block_size = block_size
        return y

    @staticmethod
    def backward(ctx, grad_output: torch.Tensor):
        x, = ctx.saved_tensors
        n_ele = x.numel()
        grad_input = torch.empty_like(x)
        grid = lambda meta: (triton.cdiv(n_ele, meta['BLOCK_SIZE']), )
        block_size = ctx.block_size
        relu_bwd_kernel[grid](x, grad_output, grad_input, n_ele, block_size)
        return grad_input, None

def triton_relu(x: torch.Tensor, BLOCK_SIZE: int = 1024) -> torch.Tensor:
    return TritonReLUFunction.apply(x, BLOCK_SIZE)
```

> 似乎存在一些问题



### LayerNorm 前向和后向

LayerNorm 的前向公式为

$$
y = \frac{x-E[x]}{\sqrt{Var(x)+\epsilon}} * w + b
$$

反向比较复杂



# CUDA 原生
## conda

### conda 环境管理

#### 创建环境

> `conda create --name`  

```bash
# 创建一个名为meachineLearning的环境，指定Python版本是3.5（不用管是3.5.x，conda会为我们自动寻找3.５.x中的最新版本）
conda create --name meachineLearning python=3.5
```

#### 激活环境

> conda activate 

```bash
conda activate meachineLearing
```

#### 返回主环境

> conda deactivate

```bash
conda deactivate meachingLearning
```

#### 删除环境

> conda remove

```bash
# 删除一个已有的环境
conda remove --name meachineLearning --all
```

#### 查看系统中的所有环境

```bash
conda info -e
```

### conda包管理

#### 安装库

```bash
conda install numpy
```

#### 查看已经安装的库

```bash
conda list
conda list -n meachineLearning
```



## 编译环境


### Vscode + cmake

使用 cmake 进行编译，编写 CMakeLists.txt

```cmake
cmake_minimum_required(VERSION 3.29)

project(cuda_main LANGUAGES C CXX CUDA)

add_executable(cuda_main main.cu)

set_target_properties(cuda_main PROPERTIES CUDA_SEPARABLE_COMPILATION ON)
```

编译命令如下，可以保存为 build_cuda.bat 脚本（不能保存为 build.bat 脚本，否则会出现重复执行的问题）

```sh
cmake -B build -G"Visual Studio 17 2022"
cmake --build build
.\build\Debug\cuda_main.exe
```


### CLion

首先添加编译工具，参考 [Tutorial: Configure CLion on Windows | CLion Documentation (jetbrains.com)](https://www.jetbrains.com/help/clion/quick-tutorial-on-configuring-clion-on-windows.html#MSVC)。在 File | Settings | Build, Execution, Deployment | Toolchains 中点击 + 添加 Visual Studio，在 Toolset 一栏中填入 Visual Studio 的安装位置如 D:\VisualStudio\Community，等待检测完毕即可。

随后在 File | Settings | Build, Execution, Deployment | Cmake 中设置 Toolchain 为刚才设置的 Visual Studio，Generator 为 Visual Studio xx xxxx（安装的 VS 版本）。




### C 工程引入cuda


#### CMake

在 CMakeLists.txt 中加入

```cmake
include_directories(D:/cuda118/development/include)  
link_directories(D:/cuda118/development/lib/x64)  
link_libraries(cudart cudadevrt)
```

具体的路径需要根据实际情况进行修改。

如果想要在 `.c` 文件中导入 `.cu` 文件，需要对 .cu 中的代码进行额外的处理，将include包裹在extern "C" 中，还需要标记函数为 extern "C"

```c
extern "C" {
#include "xxx.cuh"
}

extern "C" void cuda_func(){
// ...
}
```



## 基本知识


### 简介


cuda 文件以 cu 结尾，编译命令如下

```shell
nvcc -o hello_world hello_world.cu
```


使用 [Nsight Systems](https://developer.nvidia.com/nsight-systems/get-started#latest-version) 测量程序性能

```sh
nsys profile ./main.exe
```


先来看一段简单的代码

```c
#include<stdio.h>
#include<stdlib.h>
__global__ void print_from_gpu(void) {
    printf("Hello World! from thread [%d,%d] From device\n", threadIdx.x,blockIdx.x);
}
int main(void) {
    printf("Hello World from host!\n");
    print_from_gpu<<<1,1>>>();
    cudaDeviceSynchronize();
    return 0;
}
```


+ `__global__`：在函数之前添加，用来告知编译器，这个函数将在 GPU 上运行，同时这里的函数返回类型只能为void

> [!NOTE] 
> 除了 `__global__`，还有 `__device__` 和 `__host__`。`__device__` 也表示函数在 GPU 上运行，但是只能由 GPU 上的函数进行调用，`__host__` 表示函数在主机上运行（可以省略）

+ `<<<>>>`：告知编译器调用在设备上运行的函数，而不是在主机上运行，这里的参数 1, 1 代表一个 block 和一个线程
+ `threadIdx.x blockIdx.x`：所有线程都会分配的一个独一无二的 ID
+ `cudaDeviceSynchronize()`：让 CPU 等待 CUDA 执行完毕后再执行下一条命令

CUDA 线程在 CUDA 核心上执行，CUDA 线程与 CPU 线程不同，CUDA 线程极其轻量并且提供快速上下文切换。每个 CUDA 线程必须执行同样的函数，在不同的数据上工作。

CUDA block：cuda 线程组合成一个逻辑实体称为 block，cuda block 在单个 Streaming Multiprocessor（SM）上执行。一个 block 运行在一个 SM 上，block 内的所有线程都只会在单个 SM 中运行，每个 GPU 可以有单个或多个 SM，如果需要并行计算，那么就需要分为 block 和 线程。

GRID：block 组合成一个逻辑实体称为 grid。

一个核函数（使用 `__global__` 标记的函数）只能有一个 grid，一个 grid 则可以有很多个 block，一个 block 则可以有许多 thread。

**使用 cuda 计算的一些步骤**

1. 在 CPU 上分配内存
2. 初始化 CPU 上的数据
3. 在 GPU 上分配空间 cudaMalloc
4. 将数据从 CPU 上转移到 GPU 上 cudaMemcpy
5. 使用 `<<<,>>>` 调用 GPU 函数
6. 使用 cudaDeviceSynchronize 同步 GPU 和 CPU，加上 cudaDeviceSynchronize 可以让核函数之后的代码在核函数之后执行，否则会在核函数之前执行（在计时时需要注意加上）。
7. 使用 cudaMemcpy 将数据从 GPU 转移到 CPU 中
8. 释放 GPU 内存，cudaFree

**创建多个 block，每个block一个线程**

```c
__global__ void device_add(int *a, int *b, int *c) {
    c[blockIdx.x] = a[blockIdx.x] + b[blockIdx.x];
}
device_add<<<N,1>>>();
```


**创建单个 block，多线程**

```c
__global__ void device_add(int *a, int *b, int *c) {
    c[threadIdx.x] = a[threadIdx.x] + b[threadIdx.x];
}
device_add<<<1,N>>>
```


**创建多block，多线程**

```c
__global__ void device_add(int *a, int *b, int *c) {
    int index = threadIdx.x + blockIdx.x * blockDim.x;
    c[index] = a[index] + b[index];
}

threads_per_block = 8;
no_of_blocks = N/threads_per_block;
device_add<<<no_of_blocks,threads_per_block>>>(d_a,d_b,d_c);
```

> [!NOTE]
>
> 注意上面的线程和 block 只有一个维度，最多可以有三个维度



### GPU 的基础架构

GPU围绕一组可扩增的 Streaming Multiprocessors（SM）构建，GPU硬件并行是通过复制这个架构构建块来实现的。每个 SM 可以支持数百个线程同时执行，一个GPU一般有多个 SM，当核 grid 运行时，grid 的线程块被分配到可用的SM上，一旦一个线程块的线程被分配到一个SM上，那么线程只会在该SM上运行，单个SM一次可以被分配多个线程块。CUDA 使用单指令多线程（SIMT）技术来管理和执行一组线程（有 32 个线程，称为 warps），一个warps 中的所有线程同时执行相同的指令，每个SM将分配给它的线程块划分为32个线程段，然后在可用的硬件资源上调度执行。一个 Warps 中的线程相对独立，有自己的指令地址计数器，寄存器状态和执行路径。


> [!NOTE]
> 由于一个 Warps 中的线程数为32，所以将线程块的大小设置为32的倍数可以更加有效的利用硬件资源。


SM 是GPU架构中的核心，寄存器和共享内存是SM中的稀缺资源，CUDA负责分配这些资源，这些资源也同样约束了一个SM中最多可以同时执行的warps（即并行能力）。


### warp divergence

假如一个 warp 中的线程需要执行的指令中包含分支，那么在执行指令时，就可能会有一部分线程因为不满足分支条件而不执行，这相当于浪费了一部分资源（称为 divergence），所以需要避免同个warp中执行包含分支的命令。

下面介绍了一种情况强制 branch 的间隔尺寸是 warp size 的倍数

```c
__global__ void mathKernel2(float *c)
{
	int tid = blockIdx.x* blockDim.x + threadIdx.x;
	float a = 0.0;
	float b = 0.0;
	if ((tid/warpSize) % 2 == 0)
	{
		a = 100.0f;
	}
	else
	{
		b = 200.0f;
	}
	c[tid] = a + b;
}
```

有时控制流依赖于线程索引，通过重排数据访问模式，可以减少甚至避免 warp 分支。先考虑一个并行求和问题

```c
int sum = 0; 
for (int i = 0; i < N; i++) sum += array[i];
```

**分组求和**

通用的方法是对数据进行分组，如相邻分组或者间隔分组，下面是间隔分组的代码

```c
int recursiveReduce(int *data, int const size)
{
	// terminate check
	if (size == 1) return data[0];
	// renew the stride
	int const stride = size / 2;
	if (size % 2 == 1)
	{
		for (int i = 0; i < stride; i++)
		{
			data[i] += data[i + stride];
		}
		data[0] += data[size - 1];
	}
	else
	{
		for (int i = 0; i < stride; i++)
		{
			data[i] += data[i + stride];
		}
	}
	// call
	return recursiveReduce(data, stride);
}
```

写成核函数的形式

```c
__global__ void reduceNeighbored(int * g_idata, int * g_odata, int n) {  
    const int id = threadIdx.x;  
    if (id >= n) return;  
    int *i_data = g_idata + blockIdx.x * blockDim.x;  
  
    for (int stride = 1; stride < blockDim.x; stride *= 2) {  
        // 第一次迭代时，x[id] += x[id+1] id = 0, 2, 4, 6, 8, ...  
        // 第二次迭代时, x[id] += x[id+2] id = 0, 4, 8, 12, 16,...  
        // 第三次迭代时，x[id] += x[id+4] id = 0, 8, 16, ...  
        if (id % (2 * stride) == 0) {    // 换成 id & (2 * stride - 1) == 0 更快
            i_data[id] += i_data[id + stride];  
            __syncthreads();   // 确保同个block中的threads在当前迭代时，部分和已经存入内存  
        }  
    }    if (id == 0) g_odata[blockIdx.x] = i_data[0];  
}
```

显然，对于上面的核函数，索引为奇数的线程不会执行，并且索引为 0 的线程执行了最多次计算。在主机函数中，grid 和 block 都是一维的，最后结果还需要对 g_odata 求和。

上面这个核函数是顺序执行，可以通过序号重排来降低 divergence

```c
__global__ void reduceNeighboredLess(int * g_idata, int * g_odata, int n) {  
    const int id = threadIdx.x;  
    const int idx = blockIdx.x * blockDim.x + threadIdx.x;  
    if (idx >= n) return;  
    int *i_data = g_idata + blockIdx.x * blockDim.x;  
    for (int stride = 1; stride < blockDim.x; stride *= 2) {  
        // 第一次迭代：x[index] += x[index+1]  index = 0, 2, 4, 6, 8, ...  
        // 第二次迭代：x[index] += x[index+2]  index = 0, 4, 8, 12, ...  
        // 第三次迭代：x[index] += x[index+4]  index = 0, 8, 16, ...  
        int index = 2 * stride * id;  
        if (index < blockDim.x) i_data[index] += i_data[index+stride];  
        __syncthreads();  
    }  
    if (id == 0) g_odata[blockIdx.x] = i_data[0];  
}
```

虽然每次迭代时的操作，但是索引为奇数的线程也能参与计算。假设一个块有 512 个线程，则第一个迭代有 8 个 warps 参与计算（512 / 2 / 32 = 8），第二次迭代则只有 4 个 warps 参与计算，这样便可以避免divergence。


**展开循环**

下面是一个展开循环的例子

```c
for (int i = 0; i < 100; i+=2) {  
    a[i] = b[i] + c[i];  
    a[i+1] = b[i+1] + c[i+1];  
}
```


写成核函数的形式为

```c
__global__ void reduceUnrolling2(int * g_idata, int * g_odata, int n) {  
    const int tid = threadIdx.x;  
    const int idx = 2 * blockIdx.x * blockDim.x + threadIdx.x;  
    int *i_data = g_idata + blockIdx.x * blockDim.x * 2;  
    // 两个 block 一起算  
    if (idx + blockDim.x < n) g_idata[idx] += g_idata[idx + blockDim.x]; 
    __syncthreads();  
    // 算单个block  
    for(int stride = blockDim.x / 2; stride > 0; stride >>= 1) {  
        if (tid < stride) i_data[tid] += i_data[tid + stride];  
        __syncthreads();  
    }  
    if (tid == 0) g_odata[blockIdx.x] = i_data[0];  
}
```

由于一个 block 能够计算两个 block 的数据，所以只需要一半的grid。

还可以进行完全展开

```c
__global__ void reduceUnrollingFull(int * g_idata, int * g_odata, int n) {  
    const int tid = threadIdx.x;  
    const int idx = 8 * blockIdx.x * blockDim.x + threadIdx.x;  
    if (tid >= n) return;  
    int *i_data = g_idata + blockIdx.x * blockDim.x * 8;  
    if (idx + 7 * blockDim.x < n) {  
        int a1 = g_idata[idx];  
        int a2 = g_idata[idx + blockDim.x];  
        int a3 = g_idata[idx + 2 * blockDim.x];  
        int a4 = g_idata[idx + 3 * blockDim.x];  
        int a5 = g_idata[idx + 4 * blockDim.x];  
        int a6 = g_idata[idx + 5 * blockDim.x];  
        int a7 = g_idata[idx + 6 * blockDim.x];  
        int a8 = g_idata[idx + 7 * blockDim.x];  
        g_idata[idx] = a1 + a2 + a3 + a4 + a5 + a6 + a7 + a8;  
    }  
    __syncthreads();  
  
    // 一个 block 最多能有 1024 个线程  
    if (blockDim.x >= 1024 && tid < 512) i_data[idx] = g_idata[idx + 512];  
    __syncthreads();  
    if (blockDim.x >= 512 && tid < 256) i_data[idx] = g_idata[idx + 256];  
    __syncthreads();  
    if (blockDim.x >= 256 && tid < 128) i_data[idx] = g_idata[idx + 128];  
    __syncthreads();  
    if (blockDim.x >= 128 && tid < 64) i_data[idx] = g_idata[idx + 64];  
    __syncthreads();  
  
    // 32 为一个 warp 中的线程数  
    if (tid < 32) {  
        volatile int *vmem = i_data;  
        vmem[tid] += vmem[tid + 32];  
        vmem[tid] += vmem[tid + 16];  
        vmem[tid] += vmem[tid + 8];  
        vmem[tid] += vmem[tid + 4];  
        vmem[tid] += vmem[tid + 2];  
        vmem[tid] += vmem[tid + 1];  
    }  
    if (tid == 0) g_odata[blockIdx.x] = i_data[0];  
}
```

volatile 用于确保数据及时写回到内存。


### cuda 内存

cuda 的内存包括寄存器、共享（Shared）内存、本地（Local）内存、常量（Constant）内存、纹理（Texture）内存和全局（Global）内存。

核中的线程有自己的本地内存，一个线程块有私有的共享内存，该线程块内的所有线程都可以访问，共享内存会持续整个线程块的周期。所有的线程可以访问全局内存。所有的线程可以访问两个只读的内存：常量内存和纹理内存。全局内存、常量内存和纹理内存有相同的周期。

GPU中的寄存器也是最快的，相比于CPU，GPU的寄存器数量更多，寄存器对于每个线程是私有的，寄存器通常保存被频繁使用的私有变量。寄存器是一种稀有资源，在 RTX3080Ti 中，每个线程块有65536个寄存器。寄存器的溢出对于性能有很大的影响，为了避免溢出，可以在核函数的代码中配置额外的信息来辅助优化。

```c
__global__ void __lauch_bounds__(maxThreadaPerBlock,minBlocksPerMultiprocessor)  
kernel(...) { 
}
```

也可以在编译选项中加入

```c
-maxrregcount=32
```

来控制一个编译单元里所有核函数使用 registers 的最大数量。

共享内存使用 `__share__` 修饰，由于共享内存可以被块内线程访问，所以存在竞争问题，需要使用 `__syncthreads()` 进行同步。

常量内存只读指的是不能被核函数修改，但是可以被主机函数修改，使用 `__constant__` 进行修饰，常量内存可以被 cudaMemcpyToSymbol 初始化。

全局内存是 GPU 上最大的内存，延迟也最高，最默认使用的内存（直接使用 cudaMalloc 分配的内存），对 CPU 可见。可以在设备端定义，使用 `__device__` 定义设备变量。下面是一个简单的定义设备变量的例子

```c
__device__ float val_d;  
__global__ void addGlobalVariable() {  
    val_d = val_d + 1.0;  
}  
  
void test_GlobalMemory() {  
    float val_h = 1.0;  
    cudaMemcpyToSymbol(val_d, &val_h, sizeof(float));  
    addGlobalVariable<<<1, 1>>>();  
    printf("before add, val_h: %f\n", val_h);  
    cudaMemcpyFromSymbol(&val_h, val_d, sizeof(float));  
    printf("after add, val_h: %f\n", val_h);  
}
```

获取设备变量的地址的方法如下

```c
float *dptr=NULL;  
cudaGetSymbolAddress((void**)&dptr,devData);
```


#### 内存管理

一般来说，CPU 和 GPU 之间的传输速度要远低于 GPU 访问 GPU内存的速度。CPU 中的数据默认为分页数据（使用虚地址寻址，可以访问更大的内存空间），然而 GPU 不能保证安全访问分页数据，所以当分页数据从主机内存传输至设备内存时，CUDA会先临时申请一个锁定（page-locked or pinned）内存（在主机上），然后将源主机数据复制给锁定内存，最后将数据从锁定内存传给设备内存。

CUDA提供了可以直接申请pinned主机内存的方法

```c
cudaError_t cudaMallocHost(void **devPtr, size_t count);
```

这个函数会在主机内存中分配 count 字节的 pinned 内存，该内存可以被设备访问。这种方法由于省略了一次内存复制，所以读取和写入的速度更快。但是，分配过多的pinned内存会影响主机性能。pinned内存使用 `cudaFreeHost` 释放。

一般来说，主机和设备之间不能直接访问，但是存在一个例外，zero-copy 内存。使用下面的函数创建zero-copy内存

```c
cudaError_t cudaHostAlloc(void ** pHost,size_t count,unsigned int flags)
```

flags 可以选择

- cudaHostAllocDefalt
- cudaHostAllocPortable
- cudaHostAllocWriteCombined
- cudaHostAllocMapped

cudaHostAllocDefalt表示和cudaMallocHost一致，cudaHostAllocMapped创建zero-copy内存。虽然zero-copy内存可以被直接访问，但是比较耗时（如果CPU和GPU集成在一起，能有更好的效果）。


#### 共享内存

共享内存是可编程的缓存，每个线程块会被分配固定大小的共享内存。warp发出对共享内存的访问请求，理想情况下，一个 warp 发出的请求在一个事务中处理，最坏情况则是在32个不同的事务中顺序处理。如果多线程读取共享内存的一个变量，那么有一个线程负责读取，并发送到其它线程。

下面的代码分配一个二维的共享内存数组

```c
__shared__ float a[size_x][size_y];
```

还可以使用extern动态声明一个数组，在调用核函数时需要指定大小

```c
extern __shared__ int tile[];
kernel<<<grid,block,isize*sizeof(int)>>>(...);
```

共享变量可以用来保存在执行阶段需要重复使用多次的数据，速度会比直接从全局内存中读取快。下面来看一个例子，对于图像，经常需要计算直方图，即统计不同像素出现的频率，如果不使用共享内存，那么可以考虑使用原子操作，但是速度会比较慢，可以使用共享内存来加速

```c
// histogram_with_shared<<< (SIZE + NUM_BINS - 1) / NUM_BINS, NUM_BINS>>>()  
__global__ void histogram_with_shared(int *d_a, int *d_b) {  
    int tid = blockIdx.x * blockDim.x + threadIdx.x;  
    int offset = blockDim.x * gridDim.x;  
  
    __shared__ int cached[NUM_BINS];  
    cached[threadIdx.x] = 0;  
    __syncthreads();  
    while (tid < SIZE) {  
        atomicAdd(&cached[d_a[tid]], 1);  
        tid += offset;  
    }  
    __syncthreads();  
    atomicAdd(&d_b[threadIdx.x], cached[threadIdx.x]);  
}
```


上面的求多个数据之和也可以利用共享内存

```c
__global__ void reduction_shared(float *in_data, float *out_data, int n_threads, int size)
{
    extern __shared__ float sum[];
    int idx = threadIdx.x + blockIdx.x * blockDim.x;
    sum[threadIdx.x] = (idx < size) ? in_data[idx] : 0; // 将值赋给共享内存
    __syncthreads();
    if (idx < size)
    {  
        for (int stride = 1; stride < n_threads; stride *= 2)
        {
            int index = 2 * stride * threadIdx.x;
            if (index + stride < n_threads)
            {
                sum[index] += sum[index + stride];
                __syncthreads();
            }
        }
    }

    if (threadIdx.x == 0) out_data[blockIdx.x] = sum[0];
}
```


假设共有 $2^{20}$ 个数据，则可以这样调用

```c
int n_threads = 1024;
int n_grid = size / n_threads;
reduction_shared<<<n_grid, n_threads, n_threads * sizeof(float), 0>>>(in_data_d, out_data_d, n_threads, size);
```





### 流和并发

CUDA流指的是一系列由主机发起的但在设备上执行的异步操作，同个CUDA流中的操作有着严格的顺序，不同流的操作在执行顺序上没有限制。使用多个流来运行多个同步核函数，可以实现grid级别并行。CUDA的API可以分成同步（sync）或者异步（async），同步函数在调用后会阻断主机线程，而异步函数在调用后会把控制权转交给主机线程，流和异步函数时实现grid级别并行的基本要素。

所有的CUDA操作都在流中运行，CUDA中由两种流：隐含声明流（NULL流）和显式声明流（non-NULL流），NULL流是核函数运行的默认流。如果想要实现不同cuda指令相互重叠，需要使用non-null流。异步的、基于流的内核启动和数据传输支持以下类型的粗粒度并发：1、主机计算与设备计算重叠，2、主机计算与主机-设备数据传输重叠，3、主机-设备数据传输与设备计算重叠，4、设备并行计算。

之前主机和设备内存的复制是通过cudaMemcpy完成的，这个函数是同步的，为了实现并行，需要使用异步版本

```c
cudaError_t cudaMemcpyAsync(void* dst, const void* src, size_t count,cudaMemcpyKind kind, cudaStream_t stream = 0);
```

相比于之前多了一个cudaStream_t类型的参数。此外，异步数据传输时，需要使用pinned内存，即使用下面这两种函数分配内存。

```c
cudaError_t cudaMallocHost(void **ptr, size_t size);
cudaError_t cudaHostAlloc(void **pHost, size_t size, unsigned int flags);
```

流的回收使用 `cudaStreamDestroy`，为了查询流的执行情况，可以使用

```c
cudaError_t cudaStreamSynchronize(cudaStream_t stream);  // 同步
cudaError_t cudaStreamQuery(cudaStream_t stream); // 异步，执行完了返回cudaSuccess，未执行完返回cudaErrorNotReady
```

多个流调度cuda操作的常见模式为

```c
for (int i = 0; i < nStreams; i++) {  
    int offset = i * bytesPerStream;  
    cudaMemcpyAsync(&d_a[offset], &a[offset], bytePerStream, streams[i]);  
    kernel<<grid, block, 0, streams[i]>>(&d_a[offset]);  
    cudaMemcpyAsync(&a[offset], &d_a[offset], bytesPerStream, streams[i]);  
}  
for (int i = 0; i < nStreams; i++) {  
    cudaStreamSynchronize(streams[i]);  
}
```


**虚假依赖**

如果所有流都在单一硬件工作队列中执行，便可能会出现虚假依赖，如存在三个流，流中的操作相互依赖，那么在工作时便会出现如下情况。

流1：`A-B-C`，流2：`P-Q-R`，流3：`X-Y-Z`

工作队列：`A - B - C P - Q - R X - Y - Z`

这是因为在执行时，会先执行 A，再执行 B 时发现 B依赖A所以阻塞队列，等到B执行完后，C也会因为相同的原因阻塞，不过当C开始执行时，发现 P 不依赖 C，所以如果有额外的硬件资源便会执行 P，X也是一样的道理。

解决虚假依赖最好的方法便是多个工作队列，有时不需要过多的工作队列，可以设置最大工作队列节约资源

```c
setenv("CUDA_DEVICE_MAX_CONNECTIONS", "32", 1);
```

不同流可以设置优先级，使用 `cudaStreamCreateWithPriority`，获取优先级使用 `cudaDeviceGetStreamPriorityRange`。


**Cuda 事件**

CUDA中的事件本质上是CUDA流中的一个标记，与该流中操作流中的某个点相关联，事件可以用来同步流执行和监测设备进程。

事件的创建和销毁如下

```c
cudaEvent_t event;
cudaError_t cudaEventCreate(cudaEvent_t* event);
cudaError_t cudaEventDestroy(cudaEvent_t event);
```

下面看一下事件用于记录事件之间的时间间隔的代码

```c
// create two events  
cudaEvent_t start, stop;  
cudaEventCreate(&start);  
cudaEventCreate(&stop);  
// record start event on the default stream  
cudaEventRecord(start);  
// execute kernel  
kernel<<<grid, block>>>(arguments);  
// record stop event on the default stream  
cudaEventRecord(stop);  
// wait until the stop event completes  
cudaEventSynchronize(stop);  
// calculate the elapsed time between two events  
float time;  
cudaEventElapsedTime(&time, start, stop);  
// clean up the two events  
cudaEventDestroy(start);  
cudaEventDestroy(stop);
```

之前曾经提到了线程的同步 `cudaThreadSynchronize`，流也有同步。流分为null流（同步流）和non-null流（异步流），异步流通常不会阻塞主机，同步流中部分操作会造成阻塞，主机等待，什么都不做，直到某操作完成。虽然non-null流都是异步操作，不会阻塞主机，但是可能会被null流中的操作阻塞，如果non-null流被声明为非阻塞的，那么就不会被null流阻塞，但如果声明为阻塞流，那么就会被null流阻塞。

下面来看一个例子

```c
kernel_1<<<1, 1, 0, stream_1>>>();
kernel_2<<<1, 1>>>();
kernel_3<<<1, 1, 0, stream_2>>>();
```

上面的例子中第一个和第三个是non-null流，第二个是null流（默认创建），在执行时，kernel_1先被启动，然后控制权转交给主机，主机启动kernel_2，此时kernel_2不会立即执行，而是等到kernel_1执行完毕才执行，kernel_3只能在kernel_2执行完成后再开始执行（以主机视角，每个kernel的启动是异步、非阻塞的，需要区分启动和执行之间的区别）。

CUDA提供了创建非阻塞流的函数

```c
cudaError_t cudaStreamCreateWithFlags(cudaStream_t* pStream, unsigned int flags);
```

flags可以选择cudaStreamDefault（阻塞）和cudaStreamNonBlocking（非阻塞），上例中，如果stream_1和stream_2声明为非阻塞流，那么三个核函数同时执行。


**同步**

同步有隐式同步和显式同步，cudaMemcpy为隐式同步（阻塞进程），隐式同步常见于内存操作中。

显示同步主要通过调用命令实现

```c
cudaError_t cudaDeviceSynchronize(void);  // 阻塞主机线程，直到设备完成所有操作

cudaError_t cudaStreamSynchronize(cudaStream_t stream);  // 同步流，会阻塞主机
cudaError_t cudaStreamQuery(cudaStream_t stream);  // 非阻塞，测试流是否完成

// 与流类似
cudaError_t cudaEventSynchronize(cudaEvent_t event);  
cudaError_t cudaEventQuery(cudaEvent_t event);
```

流之间同步的方法，通过事件来实现同步，流需要等待指定的事件，事件完成后再继续

```c
cudaError_t cudaStreamWaitEvent(cudaStream_t stream, cudaEvent_t event);
```


#### 并发核函数执行

一个 non-null 流的并发执行例子

```c
#include "stream_async.cuh"  
#define N 100000  
__global__ void kernel_1() {  
    double sum = 0.0;  
    for (int i = 0; i < N; i++) {  
        sum += tan(0.1) * tan(0.1);  
    }  
}  
  
__global__ void kernel_2() {  
    double sum = 0.0;  
    for (int i = 0; i < N; i++) {  
        sum += tan(0.1) * tan(0.1);  
    }  
}  
  
void test_simple_stream() {  
    int n_stream = 4;  
    cudaStream_t *stream = (cudaStream_t *)malloc(n_stream * sizeof(cudaStream_t));  
    for (int i = 0; i < n_stream; i++) {  
        cudaStreamCreate(&stream[i]);  
    }  
    cudaEvent_t start,stop;  
    cudaEventCreate(&start);  
    cudaEventCreate(&stop);  
    cudaEventRecord(start,0);  
    for (int i = 0; i < n_stream; i++) {  
        kernel_1<<<1, 1, 0, stream[i]>>>();
        kernel_2<<<1, 1, 0, stream[i]>>>();  
    }  
    cudaEventRecord(stop,0);  
    cudaEventSynchronize(stop);  
    float elapsed_time;  
    cudaEventElapsedTime(&elapsed_time,start,stop);  
    printf("elapsed time:%f ms\n",elapsed_time);  
    for(int i=0;i<n_stream;i++)  
    {  
        cudaStreamDestroy(stream[i]);  
    }  
    cudaEventDestroy(start);  
    cudaEventDestroy(stop);  
    free(stream);  
    cudaDeviceReset();  
}
```


上面提到了虚假依赖问题，虽然现代GPU上已经不存在这个问题，不过还是可以通过广度优先的方法来组织任务。


不光核函数或者设备使用多个流处理，使用 OpenMP 还可以让主机在多线程下工作

```c
omp_set_num_threads(n_stream);
#pragma omp parallel
    {      
        int i=omp_get_thread_num();
        kernel_1<<<grid,block,0,stream[i]>>>();
        kernel_2<<<grid,block,0,stream[i]>>>();
    }
```


#### 重叠内核执行和数据传输

数据传输和内核执行之间存在下面两种关系

- 如果内核使用数据A，那么对A进行数据传输必须要安排在内核启动之前，且必须在同一个流中

- 如果内核完全不使用数据A，那么内核执行和数据传输可以位于不同的流中重叠执行。

第二种情况是重叠内核执行和数据传输的基本做法，当数据传输和内核执行被分配到不同流中时，CUDA默认这是安全的。第一种情况也可以重叠，不过需要一定的技巧，以向量加法为例。

```c
__global__ void sumArraysGPU(float*a,float*b,float*res,int N)  
{  
    int idx=blockIdx.x*blockDim.x+threadIdx.x;  
    if(idx < N)  
    {  
        for(int j=0;j<N_REPEAT;j++)  
            res[idx]=a[idx]+b[idx];  
    }  
}
```


将整个过程分为 N_SEGMENT 份，也就是 N_SEGMENT 个流分别执行（深度优先）

```c
cudaStream_t stream[N_SEGMENT];  
for(int i=0;i<N_SEGMENT;i++)  
{  
    CHECK(cudaStreamCreate(&stream[i]));  
}  
cudaEvent_t start,stop;  
cudaEventCreate(&start);  
cudaEventCreate(&stop);  
cudaEventRecord(start,0);  
for(int i=0;i<N_SEGMENT;i++)  
{  
    int ioffset=i*iElem;  
    CHECK(cudaMemcpyAsync(&a_d[ioffset],&a_h[ioffset],nByte/N_SEGMENT,cudaMemcpyHostToDevice,stream[i]));  
    CHECK(cudaMemcpyAsync(&b_d[ioffset],&b_h[ioffset],nByte/N_SEGMENT,cudaMemcpyHostToDevice,stream[i]));  
    sumArraysGPU<<<grid,block,0,stream[i]>>>(&a_d[ioffset],&b_d[ioffset],&res_d[ioffset],iElem);  
    CHECK(cudaMemcpyAsync(&res_from_gpu_h[ioffset],&res_d[ioffset],nByte/N_SEGMENT,cudaMemcpyDeviceToHost,stream[i]));  
}  
//timer  
CHECK(cudaEventRecord(stop, 0));  
CHECK(cudaEventSynchronize(stop));
```

数据传输使用异步方式，数据声明为pinned内存。

使用广度优先调度重叠

```c
for(int i=0;i<N_SEGMENT;i++)
{
    int ioffset=i*iElem;
    CHECK(cudaMemcpyAsync(&a_d[ioffset], &a_h[ioffset], nByte/N_SEGMENT, cudaMemcpyHostToDevice, stream[i]));
    CHECK(cudaMemcpyAsync(&b_d[ioffset], &b_h[ioffset], nByte/N_SEGMENT, cudaMemcpyHostToDevice,stream[i]));
}
for(int i=0;i<N_SEGMENT;i++)
{
    int ioffset=i*iElem;
    sumArraysGPU<<<grid,block,0,stream[i]>>>(&a_d[ioffset], &b_d[ioffset], &res_d[ioffset], iElem);
}
for(int i=0;i<N_SEGMENT;i++)
{
    int ioffset=i*iElem;
    CHECK(cudaMemcpyAsync(&res_from_gpu_h[ioffset], &res_d[ioffset], nByte/N_SEGMENT, cudaMemcpyDeviceToHost, stream[i]));
}
```


很多语言中，流都支持回调，cuda也支持，下面是一个例子

```c
void CUDART_CB my_callback(cudaStream_t stream, cudaError_t status, void *data) {  
    printf("callback from stream %d\n", *((int *)data));  
}
```

回调函数中不可以调用CUDA的API，不可以执行同步。

使用回调函数时

```c
cudaError_t cudaStreamAddCallback(cudaStream_t stream,cudaStreamCallback_t callback, void *userData, unsigned int flags);
```


### cuda 指令

cuda 自带了单精度和双精度函数，包含了 C 标准数学库，只能在设备端代码使用，这些函数大多有着很好的优化。下面是一个例子

```c
__global__ void intrinsic_pow(float *ptr) {  
    *ptr = __powf(*ptr, 2.0f);   // cuda自带函数名往往以__开头
}  
  
void test_intrinsic() {  
    float val_h = 3.0f;  
    float *val_d;  
    float out_h;  
    cudaMalloc(&val_d, sizeof(float));  
    cudaMemcpy(val_d, &val_h, sizeof(float), cudaMemcpyHostToDevice);  
    intrinsic_pow<<<1, 1>>>(val_d);  
    cudaMemcpy(&out_h, val_d, sizeof(float), cudaMemcpyDeviceToHost);  
    printf("out_h: %f\n", out_h);  
}
```

cuda 自带的函数虽然速度更快，但是在某些场合下需要考虑精度问题，这时候需要在编译时防止优化器对代码进行优化，如设置 `--fmad=false` 禁止编译器使用乘加操作，还有一些其它指令，参考 [NVIDIA CUDA Compiler Driver options-for-steering-gpu-code-generation](https://docs.nvidia.com/cuda/cuda-compiler-driver-nvcc/index.html#options-for-steering-gpu-code-generation)


**原子指令**：原子指令指一个线程对一个变量执行一个不会被打断的指令，即不会被其它线程干扰读改写操作，可用于对全局内存和共享内存操作。大多数原子函数都是二元函数，输入是内存地址和一个值。下面是一个使用原子指令替换加法的例子


普通操作
```c
__global__ void incr(int *ptr) {
	int temp = *ptr;
	temp = temp + 1;
	*ptr = temp;
}
```

原子操作

```c
__global__ void incr(__global__ int *ptr) {
	int temp = atomicAdd(ptr, 1);
}
```

如果想要自定义一个原子函数，那么需要使用 atomicCAS 设备函数

```c
int atomicCAS(int *address, int compare, int val);
```

address 是目标内存地址，compare 是希望在这个位置的值，val 是想要写入的值。下面是一个例子

```c
__device__ int myAtomicAdd(int *addr, int incr) {  
    int expected = *addr;  
    int oldVal = atomicCAS(addr, expected, expected + incr);  
    while(oldVal != expected) {  
        expected = oldVal;  
        oldVal = atomicCAS(addr, expected, expected + incr);  
    }  
    return oldVal;  
}
```

如果分配错误，那就一直分配下去。

atomic指令虽然好用，但是会造成一定的性能损耗，不过可以减少，比如在计算向量和时，可以先用之前的方法计算部分和，再用原子操作的方式计算部分和之和。

一般atomic指令只支持整数类型，只有 atomicExch 和 atomicAdd 支持单精度，没有atomic指令支持双精度。可以自定义原子指令来实现对浮点数的支持，基本思路是将浮点数的原始比特存储为atomic指令的支持类型。

```c
__device__ float myAtomicAdd(float *address, float incr) {  
    // Convert address to point to a supported type of the same size  
    unsigned int *typedAddress = (unsigned int *)address;  
    // Stored the expected and desired float values as an unsigned int  
    float currentVal = *address;  
    unsigned int expected = __float2uint_rn(currentVal);  
    unsigned int desired = __float2uint_rn(currentVal + incr);  
    int oldIntValue = atomicCAS(typedAddress, expected, desired);  
    while (oldIntValue != expected) {  
        expected = oldIntValue;  
        //  Convert the value read from typedAddress to a float, increment,  
        // and then convert back to an unsigned int        desired = __float2uint_rn(__uint2float_rn(oldIntValue) + incr);  
        oldIntValue = atomicCAS(typedAddress, expected, desired);  
    }  
    return __uint2float_rn(oldIntValue);  
}
```



### cuda 库

[NVIDIA CUDA - NVIDIA Docs](https://docs.nvidia.com/cuda/doc/index.html) 这个链接下的 CUDA Math Libraries 一栏提供了一些cuda库，如快速傅里叶变换库 cuFFT，线性代数库 cuBLAS，随机生成库 cuRAND，信号处理库 NPP等。







## 基础操作


### cuda 函数计时

使用 cuda 官方示例中提供的函数，该函数可以从 [cuda-samples/Common/helper_timer.h](https://github.com/NVIDIA/cuda-samples/blob/master/Common/helper_timer.h) 下载（下载时注意 cuda 版本）。使用方法如下

```c
// Initialize timer
StopWatchInterface *timer;

sdkCreateTimer(&timer);

sdkStartTimer(&timer);
// ... Execution code ...

// Getting elapsed time
cudaDeviceSynchronize(); // Blocks the host until GPU finishes the work
sdkStopTimer(&timer);

// Getting execution time in micro-secondes

float execution_time_ms = sdkGetTimerValue(&timer)
// Termination of timer
sdkDeleteTimer(&timer);
```



### 错误处理

由于 cuda 基本上都是异步执行，当错误发生时，往往不知道是哪一条指令触发的，可以编写一个宏定义来检测 cuda 函数是否错误

```c
#define CHECK(call)\  
{\  
const cudaError_t error=call;\  
if(error!=cudaSuccess)\  
{\  
printf("ERROR: %s:%d,",__FILE__,__LINE__);\  
printf("code:%d,reason:%s\n",error,cudaGetErrorString(error));\  
exit(1);\  
}\  
}
```


### 矩阵的索引

矩阵在内存中以线性方式存储，对于一个大小为 `(nx, ny)` 的矩阵，内存中前 `nx` 个数据为第一行，`nx+1` 到 `2*nx` 个数据对应第二行，以此类推。

为了索引matrix，需要用到下面的等式

```c
// 二维形式的索引
ix = threadIdx.x + blockIdx.x * blockDim.x;
iy = threadIdx.y + blockIdx.y * blockDim.y;

// 转换为一维形式
idx = ix + nx * iy
```

若 nx=8，ny=6，block 的大小为 (4, 2)，则一个 grid 需要对应 6 个block，假设这 6 个block组成一个 (2, 3) 大小的 grid。即 blockDim = (4, 2) ，threadIdx.x = range(4)，threadIdx.y = range(2)，而每个 block 对应了一个 blockIdx。

如 block(0, 0) 的 blockIdx.x = blockIdx.y = 0，因此 ix = range(4)，iy = range(2)，而 idx = {0, 1, 2, 3, 8, 9, 10, 11}

如果一个 grid 中只有一个 block，那么自然 blockIdx.x = blockIdx.y = 0，则坐标的索引简化为

```c
// 二维形式的索引
ix = threadIdx.x
iy = threadIdx.y

// 转换为一维形式
idx = ix + nx * iy
```


如果 grid 和 block 都是 1 维，那么 y 坐标就不需要了，坐标索引简化为

```c
ix = threadIdx.x + blockIdx.x * blockDim.x;

// 转换为一维形式
idx = ix
```

一般来说，处理 matrix，二维的 block 和 grid 性能最好


### 获取设备信息

```c
int deviceCount = 0;  
cudaError_t err = cudaGetDeviceCount(&deviceCount);

cudaDeviceProp deviceProp{};  
cudaGetDeviceProperties(&deviceProp, 0);

int driverVersion = 0;  
cudaDriverGetVersion(&driverVersion);
```

在 deviceProp 中可以查看GPU的各种参数，如 3080Ti 的 warpSize 为 32，SM 数量为 80，一个 block 最多只能有 1024 个 thread。



## 实践


### 矩阵相乘


**一维形式**

```c
// 一维形式： R[i*w + j] = Σ(X[i*w + k] * Y[k*w + j])
__global__ void matmul(const float *X, const float *Y, float * R, const int w) {
    int idx = threadIdx.x + blockIdx.x * blockDim.x;
    int i = idx / w;
    int j = idx % w;
    if (i <w && j < w) {
        R[i * w + j] = 0;
        for (int k = 0; k < w; k++) {
            R[i * w + j] += X[i * w + k] * Y[k * w + j];
        }
    }

}

void test_matmul() {
    const int N = 12;
    size_t size = N * N * sizeof(float);

    // 主机内存变量（CPU）
    float *h_A = (float *)malloc(size);
    float *h_B = (float *)malloc(size);
    float *h_C = (float *)malloc(size);

    for (int i = 0; i < N; i++) {
        for (int j = 0; j < N; j++) {
            h_A[i * N + j] = rand() / (float)RAND_MAX;
            h_B[i * N + j] = rand() / (float)RAND_MAX;
            h_C[i * N + j] = 0.0;
        }
    }

    // 设备内存变量（GPU）
    float *d_A, *d_B, *d_C;
    cudaMalloc(&d_A, size);
    cudaMalloc(&d_B, size);
    cudaMalloc(&d_C, size);

    // 将主机内存中的数据拷贝到设备内存
    cudaMemcpy(d_A, h_A, size, cudaMemcpyHostToDevice);
    cudaMemcpy(d_B, h_B, size, cudaMemcpyHostToDevice);

	// threadsPerBlock * blocksPerGrid 需要大于等于 N * N，否则无法遍历所有的位置
    int threadsPerBlock = N;
    int blocksPerGrid = N;

    matmul<<<blocksPerGrid, threadsPerBlock>>>(d_A, d_B, d_C, N);

    cudaMemcpy(h_C, d_C, size, cudaMemcpyDeviceToHost);

    cudaFree(d_A);
    cudaFree(d_B);
    cudaFree(d_C);

    free(h_A);
    free(h_B);
    free(h_C);
}
```

**二维形式**

```c
#include "cuda_runtime.h"
#include "device_launch_parameters.h"
#include <stdio.h>

// 二维形式： R[i, j] = Σ(X[i, k] * Y[k, j])
__global__ void MatMul(int* M, int* N, int* P, int width)
{
	// 由于设置 block 为 1，所以可以直接令 x = threadIdx.x
    int x = threadIdx.x;
    int y = threadIdx.y;

    float Pervalue = 0;

    float elem1 = 0.0, elem2 = 0.0, value = 0.0;
    for (int i = 0; i < width; i++)
    {
        elem1 = M[y * width + i];  // 取 M 矩阵的一行
        elem2 = N[i * width + x];  // 取 N 矩阵的一列

        value += elem1 * elem2;    // 求和
    }

    P[y * width + x] = value;
}

int main()
{
    const int ND = 30;
    int a[ND][ND], b[ND][ND], c[ND][ND];
    int* M, * N, * P;

	for (int i = 0; i < ND; i++)
    {
        for (int j = 0; j < ND; j++)
        {
            a[i][j] = 2;
            b[i][j] = 3;
        }
    }
    int Size = ND * ND;
    
    int width = ND;
    int NUM = width * width;
    dim3 blockSize(ND, ND);
	
    // 利用 event 计算时间
    cudaEvent_t start, stop;
    float elapsedTime = 0;
    cudaEventCreate(&start);
    cudaEventCreate(&stop);

    // 设备端内存分配
    // M N P 都是一维数组
    cudaMalloc((void**)&M, ND * ND * sizeof(int));
    cudaMalloc((void**)&N, ND * ND * sizeof(int));
    cudaMalloc((void**)&P, ND * ND * sizeof(int));

    // 拷贝数据到GPU中
    cudaMemcpy(M, a, Size * sizeof(int), cudaMemcpyHostToDevice);
    cudaMemcpy(N, b, Size * sizeof(int), cudaMemcpyHostToDevice);

    cudaEventRecord(start, 0);
    MatMul << <1, blockSize >> > (M, N, P, width);
    cudaThreadSynchronize();
    cudaEventRecord(stop, 0);
    cudaEventSynchronize(stop);

    cudaEventElapsedTime(&elapsedTime, start, stop);

    printf("elapsedTime: %f", elapsedTime);

    // 将 GPU 中的数据传回 cpu 中
    cudaMemcpy(c, P, Size * sizeof(int), cudaMemcpyDeviceToHost);
    printf("c[0][0] = %d \n", c[0][0]);

    // 释放设备内存
    cudaFree(M);
    cudaFree(N);
    cudaFree(P);
    return 0;
}
```




### darknet

darknet 是一个使用 c++ 和 cuda 编写的神经网络框架，下面介绍如何在 Windows 中编译。

首先 clone 对应 Windows 平台的库

```powershell
git clone https://github.com/AlexeyAB/darknet.git
```


使用 cmake-gui 进行编译，如果需要附加 opencv，需要在 CMakeLists.txt 中设置 opencv 编译的路径

```cmake
set(OpenCV_DIR D:/opencv/build)
```

编译完成后使用 visual studio 打开项目，设置 darknet 为启动项目，编译后会发现缺少 pthreadVC2.dll，在 `darknet\3rdparty\pthreads\bin` 中可以找到 `pthreadVC2.dll`。

