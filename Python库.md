
## flash attention

提供了注意力机制的快速实现

[Dao-AILab/flash-attention: Fast and memory-efficient exact attention](https://github.com/Dao-AILab/flash-attention)

### Linux

在官方仓库中[Releases · Dao-AILab/flash-attention](https://github.com/Dao-AILab/flash-attention/releases) 提供了针对不同环境的whl文件，可以直接下载并安装


### Windows

官方提供的库只能在linux上安装，

[kingbri1/flash-attention: Fast and memory-efficient exact attention](https://github.com/kingbri1/flash-attention)中提供了适合部分pytorch、cuda版本的适用于Windows系统的whl文件。

实测：torch2.4.0 + cuda12.4 + flash_attn-2.7.1.post1 在Windows10上可行。


## triton

Triton 是一个专门为深度学习和高性能计算任务设计的编程语言和编译器

[triton-lang/triton: Development repository for the Triton language and compiler](https://github.com/triton-lang/triton)

### Linux

官方提供了whl文件，可以直接 `pip install`

### Windows（似乎不行）

仅支持cuda12.x
[woct0rdho/triton-windows: Fork of the Triton language and compiler for Windows support](https://github.com/woct0rdho/triton-windows) 提供了适用于Windows平台的triton whl文件


## Mamba 

一个新的网络架构

目前只能在linux下运行

先下载 causal-conv1d，注意最好用 pip 下载，可能需要加上代理

```sh
pip install causal-conv1d --proxy=156.238.18.163:2095
```

再下载mamba，这里直接在[state-spaces/mamba: Mamba SSM architecture](https://github.com/state-spaces/mamba) 找到符合条件的whl文件下载再安装。

