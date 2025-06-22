

# 自制深度学习推理框架

参考：[zjhellofss/KuiperInfer](https://github.com/zjhellofss/KuiperInfer)


## 设置环境

首先拉取远程仓库

```sh
git clone --recursive https://github.com/zjhellofss/KuiperInfer.git
```

代码最好在Linux环境下运行，可以使用wsl

代码需要用到一些C++库，使用cmake进行安装，安装参考 [ubuntu安装cmake的三种方法（超方便！）-CSDN博客](https://blog.csdn.net/Man_1man/article/details/126467371)

如果遇到找不到cmake的情况，可以进行如下操作

```sh
vim ~/.bashrc
export PATH=/usr/local/cmake/bin:$PATH
source ~/.bashrc
```

具体安装的C++库的步骤可以参考[dockerfile](https://github.com/zjhellofss/KuiperInfer/blob/main/dockerfile)中的安装步骤

在安装 glog 遇到错误时可以不安装这个库，影响不大。（可以尝试安装0.6.0版本的）

armadillo库用于矩阵运算，文档为 [Armadillo](https://arma.sourceforge.net/docs.html)，`+` 为矩阵相加，`-` 为矩阵相减，`*` 为矩阵乘法，`%` 为矩阵点乘，`/` 为矩阵点除。


## 张量的设计与实现

从头设计一个张量非常复杂，直接基于 armadillo 库提供的 `arma::fcube` （三维矩阵）进行开发。

封装一个Tensor类

```c++
template <>
class Tensor<float> {
 public:
 
  uint32_t rows() const;

  uint32_t cols() const;

  uint32_t channels() const;

  uint32_t size() const;

  void set_data(const arma::fcube& data);

 private:
  std::vector<uint32_t> raw_shapes_;  // 张量数据的实际尺寸大小
  arma::fcube data_;                  // 张量数据
};
```

初始化张量的方法为

```c++
Tensor<float>::Tensor(uint32_t size)
{
	data_ = arma::fcube(1, size, 1);
	this->raw_shapes_ = std::vector<uint32_t>{size};
}
```


armadillo 中默认的数据存储方式为列主序。

reshape 时调用armadillo 提供的reshape 方法

```c++
template <typename T>
void Tensor<T>::Reshape(const std::vector<uint32_t>& shapes, bool row_major) {
  const size_t origin_size = this->size();
  const size_t current_size =
      std::accumulate(shapes.begin(), shapes.end(), size_t(1), std::multiplies<size_t>());
  if (!row_major) {
    if (shapes.size() == 3) {
      this->data_.reshape(shapes.at(1), shapes.at(2), shapes.at(0));
      this->raw_shapes_ = {shapes.at(0), shapes.at(1), shapes.at(2)};
    } else if (shapes.size() == 2) {
      this->data_.reshape(shapes.at(0), shapes.at(1), 1);
      this->raw_shapes_ = {shapes.at(0), shapes.at(1)};
    } else {
      this->data_.reshape(1, shapes.at(0), 1);
      this->raw_shapes_ = {shapes.at(0)};
    }
  } else {
    if (shapes.size() == 3) {
      this->Review({shapes.at(0), shapes.at(1), shapes.at(2)});
      this->raw_shapes_ = {shapes.at(0), shapes.at(1), shapes.at(2)};
    } else if (shapes.size() == 2) {
      this->Review({1, shapes.at(0), shapes.at(1)});
      this->raw_shapes_ = {shapes.at(0), shapes.at(1)};
    } else {
      this->Review({1, 1, shapes.at(0)});
      this->raw_shapes_ = {shapes.at(0)};
    }
  }
}
```

Flatten 相当于调用 reshape 方法

```c++
template <typename T>
void Tensor<T>::Flatten(bool row_major) {
  const uint32_t size = this->data_.size();
  this->Reshape({size}, row_major);
}
```

Padding 时先创建一个新的张量，再将旧的张量的值赋值到对应位置上

```c++
template <typename T>
void Tensor<T>::Padding(const std::vector<uint32_t>& pads, T padding_value) {
  uint32_t pad_rows1 = pads.at(0);  // up
  uint32_t pad_rows2 = pads.at(1);  // bottom
  uint32_t pad_cols1 = pads.at(2);  // left
  uint32_t pad_cols2 = pads.at(3);  // right

  arma::Cube<T> new_data(this->data_.n_rows + pad_rows1 + pad_rows2,
                         this->data_.n_cols + pad_cols1 + pad_cols2, this->data_.n_slices);
  new_data.fill(padding_value);

  new_data.subcube(pad_rows1, pad_cols1, 0, new_data.n_rows - pad_rows2 - 1,
                   new_data.n_cols - pad_cols2 - 1, new_data.n_slices - 1) = this->data_;
  this->data_ = std::move(new_data);
  this->raw_shapes_ = std::vector<uint32_t>{this->channels(), this->rows(), this->cols()};
}
```


## 计算图的定义


计算图包括以下几个部分：

1、Operator：计算节点

2、Graph：有多个 Operator 串联得到的有向⽆环图，规定了各个计算节点（ Operator ）执⾏的流程和顺序。

3、Layer：计算节点中运算的具体执⾏者， Layer 类先读取输⼊张量中的数据，然后对输⼊张量进⾏计算，得到的结果存放到计算节点的输出张量中

4、Tensor：⽤于存放多维数据的数据结构，⽅便数据在计算节点之间传递，同时该结构也封装矩阵乘、点积等与矩阵相关的基本操作。

ONNX格式的模型会将一个复杂算子拆分为多个细碎的算子，这样不利于推理的优化。自制的深度学习推理框架采用新的PNNX：[PNNX: PyTorch Neural Network Exchange](https://zhuanlan.zhihu.com/p/427620428)

PNNX 采用了一些优化方法：

1、使⽤模板匹配（pattern matching）的⽅法将匹配到的⼦图⽤对应等价的⼤算⼦替换掉。

2、在 PyTorch 中编写的简单算术表达式在转换为 PNNX 后，会保留表达式的整体结构，⽽不会被拆分成许多⼩的加减乘除算⼦。

3、加入大量图优化的技术，包括了算⼦融合， 常量折叠和消除，公共表达式消除等技术

PNNX 由图结构 Graph，运算符 Operator 和操作数 Operand 这三种结构组成，定义一个模型

```python
class Model(nn.Module): 
	def __init__(self): 
		super(Model, self).__init__() 
		self.linear = nn.Linear(32, 128) 
	def forward(self, x): 
		x = self.linear(x) 
		x = F.sigmoid(x) 
		return x
```

PNNX 中的图结构定义如下

```c++
class Graph
{
public:
    Graph();
    ~Graph();

    int load(const std::string& parampath, const std::string& binpath);
    int save(const std::string& parampath, const std::string& binpath);

    int python(const std::string& pypath, const std::string& binpath);

    int parse(const std::string& param);

    Operator* new_operator(const std::string& type, const std::string& name);

    Operator* new_operator_before(const std::string& type, const std::string& name, const Operator* cur);

    Operator* new_operator_after(const std::string& type, const std::string& name, const Operator* cur);

    Operand* new_operand(const std::string& name);

    Operand* get_operand(const std::string& name);
    const Operand* get_operand(const std::string& name) const;

    std::vector<Operator*> ops;
    std::vector<Operand*> operands;
};
```

Graph 的核心作用是管理计算图中的运算符和操作数，Operator 类⽤来表⽰计算图中的运算符，Operand 类⽤来表⽰计算图中的操作数，即与⼀个运算符有关的输⼊和输出张量。Graph 类的成员函数提供了⽅便的接⼝⽤来创建和访问操作符和操作数，以构建和遍历计算图。同时，它也是模型中运算符（算⼦）和操作数的集合。

Operator类如下所示

```c++
class Operator
{
public:
    std::vector<Operand*> inputs;
    std::vector<Operand*> outputs;

    // keep std::string typed member the last for cross cxxabi compatibility
    std::string type;
    std::string name;

    std::vector<std::string> inputnames;
    std::map<std::string, Parameter> params;
    std::map<std::string, Attribute> attrs;
};
```

Operand 类如下所示

```c++
class Operand
{
public:
    void remove_consumer(const Operator* c);

    Operator* producer;
    std::vector<Operator*> consumers;

    // 0=null 1=f32 2=f64 3=f16 4=i32 5=i64 6=i16 7=i8 8=u8 9=bool 10=cp64 11=cp128 12=cp32
    int type;
    std::vector<int> shape;
    // keep std::string typed member the last for cross cxxabi compatibility
    std::string name;
    std::map<std::string, Parameter> params;
};
```



## 构建计算图关系和执行顺序

使用拓扑排序确定算法执行的顺序，要进行拓扑排序，先要建图，建图时，先从输入开始，通过输出名字，遍历得到输入的后继算子，对每个算子都进行相同的操作。

建图时还需要确定一下张量的大小


## 算⼦和注册⼯⼚

计算图中的计算节点在本项⽬中被称之为 RuntimeOperator，在一个计算节点中，记录了与该节点相关的类型、名称，以及输⼊输出数等信息。其中最重要的是 layer 变量，它表⽰与计算节点关联的算⼦，也就是进⾏具体计算的实施者。

通过访问 `RuntimeOperator` 的输⼊数 `input_operand`， `layer` 可以获取计算所需的输⼊张量数据，并根据 `layer` 各派⽣类别中定义的计算函数 (`forward`) 对输⼊张量数据进⾏计算。计算完成后，计算结果将存储在该节点的输出数 (`output_operand`) 中。

在 KuiperInfer 中算⼦注册机制使⽤了单例模式和⼯⼚模式。⾸先，在全局范围内创建⼀个唯⼀的注册表 registry ，它是⼀个 map 类型的对象。这个注册表的键是算⼦的类型，⽽值是算⼦的初始化过程。

开发者完成⼀个算⼦的开发后，需要通过特定的注册机制将算⼦写⼊全局注册表中。这可以通过在注册表中添加键值对来实现。算⼦的类型作为键，算⼦的初始化过程作为值。这样，当需要使⽤某个算⼦时，可以根据算⼦的类型从全局注册表中⽅便地获取对应的算⼦。

在实现上单例模式确保了只有⼀个全局注册表实例，并且可以在代码的任何地⽅访问该注册表。⼯⼚模式则负责根据算⼦的类型返回相应的算⼦实例。这种注册机制的设计使得推理框架能够感知到开发者已经实现的算⼦，并且能够⽅便地调⽤和使⽤这些算⼦。

