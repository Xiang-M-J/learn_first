## 基本知识



cuda 文件以 cu 结尾，编译命令如下

```shell
nvcc -o hello_world hello_world.cu
```



### Introduction



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

这段代码中有一些关键字值得注意

+ `__global__`：在函数之前添加，用来告知编译器，这个函数将在 GPU 上运行，同时这里的函数返回类型只能为void
+ `<<<>>>`：告知编译器调用在设备上运行的函数，而不是在主机上运行，这里的参数 1, 1 代表一个 block 和一个线程
+ `threadIdx.x blockIdx.x`：所有线程都会分配的一个独一无二的 ID
+ `cudaDeviceSynchronize()`：让 CPU 等待 CUDA 执行完毕后再执行下一条命令

CUDA 线程在 CUDA 核心上执行，CUDA 线程与 CPU 线程不同，CUDA 线程极其轻量并且提供快速上下文切换。每个 CUDA 线程必须执行同样的函数，在不同的数据上工作。

CUDA block：cuda 线程组合成一个逻辑实体称为 block，cuda block 在单个 Streaming Multiprocessor（SM）上执行。一个 block 运行在一个 SM 上，block 内的所有线程都只会在单个 SM 中运行，每个 GPU 可以有单个或多个 SM，如果需要并行计算，那么就需要分为 block 和 线程。

GRID：block 组合成一个逻辑实体称为 grid。

**使用 cuda 计算的一些步骤**

1. 在 CPU 上分配内存
2. 初始化 CPU 上的数据
3. 在 GPU 上分配空间 cudaMalloc
4. 将数据从 CPU 上转移到 GPU 上 cudaMemcpy
5. 使用 `<<<,>>>` 调用 GPU 函数
6. 使用 cudaDeviceSynchronize 同步 GPU 和 CPU
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









## 实践


### 矩阵

#### 矩阵相乘

```c

#include "cuda_runtime.h"
#include "device_launch_parameters.h"

#include <stdio.h>


__global__ void MatMul(int* M, int* N, int* P, int width)
{
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

