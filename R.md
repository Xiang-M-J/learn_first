# R
[R 基础语法 | 菜鸟教程 (runoob.com)](https://www.runoob.com/r/r-basic-syntax.html)
R语言实战 Robert I, Kabacoff 2th

交互式窗口：`R`
执行脚本文件：`RScript filename`

命令行执行脚本文件：`source(main.R)`

IDE：`RStudio`

**设置工作目录**

```R
setwd("D:/xxx/R")
```

**RMarkdown**：RMarkdown可以在Markdown中执行R（在RStudio环境下）

## 基础知识

### 变量
**变量名**
注意R中允许变量中出现点号`.`，所以`a.1`是一个合法变量名，而不是类的属性
```R
# 这是注释
tom.id = 1001
print(tom.id)
```

**赋值**
可以使用左箭头`<-`、等号`=`、右箭头`->`赋值，注意等号是在新版本的R中引入的赋值符号



### 输入输出

#### 输出

##### cat
**拼接输出**
注意会在每两个拼接元素之间自动加上空格
```R
cat(1, "+", 1, "=", 2) # 1 + 1 = 2
```
**输出到文件**
```R
cat(1, "+", 1, "=", 2, file)
a = "asasjaksj"
cat(a, file="112.txt", append = TRUE)
```
注意文件默认生成在当前工作目录，默认为C盘的用户文档目录下。`cat`默认为覆盖写入，设置参数`append=TRUE`为追加写入

##### sink
`sink()`函数可以把控制台输出的文字直接输出到文件中去：
```R
sink("console.txt")
```
取消输出到文件用`sink()`
```R
sink("r_test.txt", split=TRUE)  # 控制台同样输出
for (i in 1:5) 
    print(i)
sink()   # 取消输出到文件

sink("r_test.txt", append=TRUE) # 控制台不输出，追加写入文件
print("hello")
```

#### 输入

##### 从控制台输入
```
num = readline("print input num: ")
```

##### 从键盘输入

```R
mydata <- data.frame(age=numeric(0), 
                     gender=character(0), weight=numeric(0)) 
mydata <- edit(mydata) 
```

这会自动调用一个允许手动输入数据的文本编辑器。

##### 从文件中读入文字

```R
readLines("rtest.txt")
```
> 注意：所读取的文本文件每一行 (包括最后一行) 的结束必须有换行符，否则会有警告信息。

##### 其它文件格式
**csv**

```R
read.csv("test.csv", encoding="UTF-8")
write.csv(newcsv,"test.csv")
```

**xlsx**
安装`xlsx`库，通过RStudio的图形化界面或者命令行

```R
install.packages("xlsx", repos = "https://mirrors.ustc.edu.cn/CRAN/")
```
验证并载入包
```R
any(grepl("xlsx",installed.packages()))  
# 载入包  
library("xlsx")
```
读取
```R
data <- read.xlsx("test.xlsx", sheetIndex = 1)
print(data)
```

**xml**
安装`xml`库，读取XML文件
```R
# 载入 XML 包
library("XML")
# 设置文件名
result <- xmlParse(file = "test.xml")
# 提取根节点
rootnode <- xmlRoot(result)
# 查看第 2 个节点数据
print(rootnode[2])
# 查看第 2 个节点的第  1 个数据
print(rootnode[[2]][[1]])
# 查看第 2 个节点的第 3 个数据
print(rootnode[[2]][[3]])
```

**JSON**
安装`rjson`库，读取JSON文件
```R
# 载入 rjson 包  
library("rjson") 
# 获取 json 数据  
result <- fromJSON(file = "sites.json")  
# 输出结果  
print(result)
```

**MYSQL**
安装`RMySQL`库
```R
library(RMySQL)

# dbname 为数据库名，这边的参数请根据自己实际情况填写
mysqlconnection = dbConnect(MySQL(), user = 'root', password = '', dbname = 'test',host = 'localhost')

# 查看数据
dbListTables(mysqlconnection)
# 查询
result = dbSendQuery(mysqlconnection, "select * from sites")  
# 获取前面两行数据  
data.frame = fetch(result, n = 2)  
print(data.frame)
```

### 基础运算

**算术运算符**

| 优先级 | 符号            | 含义     |
| :----- | :-------------- | :------- |
| 1      | ()              | 括号     |
| 2      | ^               | 乘方运算 |
| 3      | &#37;&#37;             | 整除求余 |
|        | &#37;&#47;&#37; | 整除     |
| 4      | *               | 乘法     |
|        | /               | 除法     |
| 5      | +               | 加法     |
|        | -               | 减法     |

**关系运算符**

| 运算符 | 描述                                                         |
| :----- | :----------------------------------------------------------- |
| >      | 判断第一个向量的每个元素是否大于第二个向量的相对应元素。     |
| <      | 判断第一个向量的每个元素是否小于第二个向量的相对应元素。     |
| ==     | 判断第一个向量的每个元素是否等于第二个向量的相对应元素。     |
| !=     | 判断第一个向量的每个元素是否不等于第二个向量的相对应元素。   |
| >=     | 判断第一个向量的每个元素是否大于等于第二个向量的相对应元素。 |
| <=     | 判断第一个向量的每个元素是否小于等于第二个向量的相对应元素。 |



**逻辑运算符**

| 运算符 | 描述                                                         |
| :----- | :----------------------------------------------------------- |
| &      | 逻辑与，将第一个向量的每个元素与第二个向量的相对应元素进行组合，如果两个元素都为 TRUE，则结果为 TRUE，否则为 FALSE。 |
| ｜     | 逻辑或，将第一个向量的每个元素与第二个向量的相对应元素进行组合，如果两个元素中有一个为 TRUE，则结果为 TRUE，如果都为 FALSE，则返回 FALSE。 |
| !      | 逻辑非，返回向量每个元素相反的逻辑值，如果元素为 TRUE 则返回 FALSE，如果元素为 FALSE 则返回 TRUE。 |
| &&     | 逻辑与，只对两个向量对第一个元素进行判断，如果两个元素都为 TRUE，则结果为 TRUE，否则为 FALSE。 |
| \|\|   | 逻辑或，只对两个向量对第一个元素进行判断，如果两个元素中有一个为 TRUE，则结果为 TRUE，如果都为 FALSE，则返回 FALSE。 |

建议使用`&&`和`||`作为逻辑与和或的运算。

**其它运算符**

| 运算符 | 描述                                                         |
| :----- | :----------------------------------------------------------- |
| :      | 冒号运算符，用于创建一系列数字的向量                         |
| %in%   | 用于判断元素是否在向量里，返回布尔值，有的话返回 TRUE，没有返回 FALSE。 |
| %*%    | 用于矩阵与它转置的矩阵相乘。                                 |

```R
v <- 1:10
print(v)
print(1 %in% v)

M1 = matrix( c(2,6,5,1), nrow = 2,ncol = 2,byrow = TRUE)
M2 = matrix( c(1,2,3,4), nrow=2, ncol = 2, byrow = TRUE)
print(M1 %*% M2)
```



**数学函数**

| 函数     | 说明                            |
| :------- | :------------------------------ |
| sqrt(n)  | n的平方根                       |
| exp(n)   | 自然常数e的n次方，              |
| log(m,n) | m的对数函数，返回n的几次方等于m |
| log10(m) | 相当于log(m,10)                 |
| sin(m)   | 正弦函数                        |
| asin(m)  | 反正弦函数                      |

**取整函数**

| 名称    | 参数模型 | 含义                       |
| :------ | :------- | :------------------------- |
| round   | (n)      | 对 n 四舍五入取整          |
|   ko      | (n, m)   | 对 n 保留 m 位小数四舍五入 |
| ceiling | (n)      | 对 n 向上取整              |
| floor   | (n)      | 对 n 向下取整              |

**正态分布**

dnorm、pnorm、qnorm、rnorm

- **d** - 概率密度函数
- **p** - 概率密度积分函数（从无限小到 x 的积分）
- **q** - 分位数函数
- **r** - 随机数函数（常用于概率仿真）

### 函数

```R
function_name <- function(arg_1, arg_2, ...) {
    # 函数体
    # 执行的代码块
    return(output)
}

```

注意内置函数`str()`的作用是显示对象的结构和内容摘要。



### 判断和循环

#### 判断

```R
if(boolean_expression_1) {
    # 布尔表达式为真将执行的语句
} else if (boolean_expression_2){
    
} else{
    
}
```

switch语句允许测试一个变量等于多个值时的情况。每个值称为一个 case。

```R
switch(expression, case1, case2, case3....)
```

- **switch** 语句中的 **expression** 是一个常量表达式，可以是整数或字符串，如果是整数则返回对应的 case 位置值，如果整数不在位置的范围内则返回 NULL。
- 如果匹配到多个值则返回第一个。
- **expression**如果是字符串，则对应的是 case 中的变量名对应的值，没有匹配则没有返回值。
- switch 没有默认参数可用。

#### 循环

```R
repeat { 
    # 相关代码 
    if(condition) {
       break
    }
}
```

```R
while(condition)
{
   statement(s);
}
```

```R
for (value in vector) {
    statements
}
```

**循环控制**：break，next（类似于continue）

### 数据类型

#### 普通类型

支持科学计数法：`1.23E2`

##### 字符串的操作函数

| 函数名                      | 功能                  | 输出              |
| --------------------------- | --------------------- | ----------------- |
| toupper("Runoob")           | 转换为大写            | "RUNOOB"          |
| tolower("Runoob")           | 转换为小写            | "runoob"          |
| nchar("中文", type="bytes") | 统计字节长度          | 4                 |
| nchar("中文", type="char")  | 总计字符数量          | 2                 |
| substr("123456789", 1, 5)   | 截取字符串，从1到5    | "12345"           |
| substring("1234567890", 5)  | 截取字符串，从5到结束 | "567890"          |
| as.numeric("12")            | 将字符串转换为数字    | 12                |
| as.character(12.34)         | 将数字转换为字符串    | "12.34"           |
| strsplit("2019;10;1", ";")  | 分隔符拆分字符串      | "2019" "10"   "1" |
| gsub("/", "-", "2019/10/1") | 替换字符串            | "2019-10-1"       |

##### 列表

**等差数列**

步长为1

```R
c <- 1:10
```

步长不为1

```R
c <- seq(from=1, to=10, by=2)
```



列表可以用于存储和操作多种类型的数据对象

```R
list_data <- list("runoob", "google", c(11,22,33), 123, 51.23, 119.1)
print(list_data)
```

也可以使用`c()`来创建列表，也可以使用该函数将多个对象**合并**为一个列表，例如：

```R
my_list <- c(object1, object2, object3)
```

> 索引从1开始，符号为`[]`

```R
# 列表包含向量、矩阵、列表
li <- list(1,2,3,4)

# 列表元素访问
print(li[1])

# 给列表元素设置名字
names(li) <- c("first", "second", "third", "fourth")

# 添加元素
li = c(li, 5)
print(li[5])

# 删除元素
li = li[-5]  # 删除列表中第5个元素
print(li[5]) # 应为null

print(length(li)) # 列表长度

# 遍历
for (e in li){
    print(e)
}

# map
l2 = lapply(l2, function(x) x*2) # 每个元素都×2

# 转向量，方便算术运算
l2 = unlist(l2)

```



### 高阶类型

#### 矩阵

```R
M <- matrix(data = NA, nrow = 1, ncol = 1, byrow = FALSE,dimnames = NULL)
```

- **byrow** 逻辑值，为 FALSE 按列排列，为 TRUE 按行排列
- **dimname** 设置行和列的名称

```R
# byrow 为 TRUE 元素按行排列
M <- matrix(c(3:14), nrow = 4, byrow = TRUE)
print(M)

# Ebyrow 为 FALSE 元素按列排列
N <- matrix(c(3:14), nrow = 4, byrow = FALSE)
print(N)

# 定义行和列的名称
rownames = c("row1", "row2", "row3", "row4")
colnames = c("col1", "col2", "col3")

P <- matrix(c(3:14), nrow = 4, byrow = TRUE, dimnames = list(rownames, colnames))
print(P)
```

**矩阵转置**：`t()`

**矩阵索引**：`M[1,2]`

**行列式**：`det(M)`

**逆矩阵**：`solve(M)`，`solve(A, B)`可用于求解线性方程组

**特征值和特征向量**：`eigen(M)`返回`values`和`vectors`



#### 数组

矩阵可视为一个二维数组

```R
array(data = NA, dim = length(data), dimnames = NULL)
```

```R
my_array <- array(1:12, dim = c(2, 3, 2))  # 创建一个3维数组
element <- my_array[1, 2, 1]  # 访问第一个维度为1，第二个维度为2，第三个维度为1的元素
print(element)  # 输出：2

# 逻辑条件筛选
filtered_elements <- my_array[my_array > 5]  # 选择大于5的元素
print(filtered_elements)  # 输出：6 7 8 9 10 11 12
```

可以使用`apply()`元素对数组元素进行跨维度计算

```R
apply(X, MARGIN, FUN, ...)
```

- `MARGIN`：指定应用函数的维度，可以是1表示行，2表示列，或者c(1, 2)表示同时应用于行和列。

```R
# 创建两个不同长度的向量
vector1 <- c(5,9,3)
vector2 <- c(10,11,12,13,14,15)

# 创建数组
new.array <- array(c(vector1,vector2),dim = c(3,3,2))
print(new.array)

# 计算数组中所有矩阵第一行的数字之和
result <- apply(new.array, c(1), sum)
print(result)
```



#### 因子

因子用于存储不同类别的数据类型，例如人的性别有男和女两个类别，年龄来分可以有未成年人和成年人。

```R
factor(x = character(), levels, labels = levels,
       exclude = NA, ordered = is.ordered(x), nmax = NA)
```

- levels：指定各水平值, 不指定时由x的不同值来求得。
- labels：水平的标签, 不指定时用各水平值的对应字符串。
- exclude：排除的字符。
- ordered：逻辑值，用于指定水平是否有序。
- nmax：水平的上限数量。

#### 数据框

类似表格，数据框每一列都有一个唯一的列名，长度都是相等的，同一列的数据类型需要一致，不同列的数据类型可以不一样。

```R
table = data.frame(
    姓名 = c("张三", "李四"),
    工号 = c("001","002"),
    月薪 = c(1000, 2000)
    
)
print(table) # 查看 table 数据
```

提取指定列

```R
print(table$姓名)
```

扩展数据框

```R
table = data.frame(
    姓名 = c("张三", "李四","王五"),
    工号 = c("001","002","003"),
    月薪 = c(1000, 2000,3000)
)
# 添加部门列
table$部门 <- c("运营","技术","编辑")
print(table)
```

#### 处理数据对象的实用函数

| 函数                         | 用途                                                         |
| ---------------------------- | ------------------------------------------------------------ |
| `length(object)`             | 显示对象中元素/成分的数量                                    |
| `dim(object)`                | 显示某个对象的维度                                           |
| `str(object)`                | 显示某个对象的结构                                           |
| `class(object)`              | 显示某个对象的类或类型                                       |
| `names(object)`              | 显示某对象中各成分的名称                                     |
| `c(object, object,...)`      | 将对象合并入一个向量                                         |
| `cbind(object, object, ...)` | 按列合并对象                                                 |
| `rbind(object, object, ...)` | 按行合并对象                                                 |
| `object`                     | 输出某个对象                                                 |
| `head(object)`               | 列出某个对象的开始部分                                       |
| `tail(object)`               | 列出某个对象的最后部分                                       |
| `ls()`                       | 显示当前的对象列表                                           |
| `rm(object, object, ...)`    | 删除一个或更多个对象语句`rm(list = ls())`将删除当前工作环境中的几乎所有对象 |
| `newobject <- edit(object)`  | 编辑对象并另存为 newobject                                   |
| `fix(object)`                | 直接编辑对象                                                 |
| `mode(object)`               | 显示某个对象的模式                                           |


### 绘图

#### 饼图

```R
pie(x, labels = names(x), edges = 200, radius = 0.8,
    clockwise = FALSE, init.angle = if(clockwise) 90 else 0,
    density = NULL, angle = 45, col = NULL, border = NULL,
    lty = NULL, main = NULL, …)
```

- x: 数值向量，表示每个扇形的面积。
- labels: 字符型向量，表示各扇形面积标签。
- edges: 这个参数用处不大，指的是多边形的边数（圆的轮廓类似很多边的多边形）。
- radius: 饼图的半径。
- main: 饼图的标题。
- clockwise: 是一个逻辑值,用来指示饼图各个切片是否按顺时针做出分割。
- angle: 设置底纹的斜率。
- density: 底纹的密度。默认值为 NULL。
- col: 是表示每个扇形的颜色，相当于调色板。

```R
# 数据准备
info = c(1, 2, 4, 8)

# 命名
names = c("Google", "Runoob", "Taobao", "Weibo")

# 涂色（可选）
cols = c("#ED1C24","#22B14C","#FFC90E","#3f48CC")

# 绘图
pie(info, labels=names, col=cols)
```

可以使用 png()、jpeg()、bmp() 函数设置输出的文件格式为图片（注意要在绘图前），中文字体需要设置字体参数 `family='GB1'`

```R
# 数据准备
info = c(1, 2, 4, 8)

# 命名
names = c("Google", "Runoob", "Taobao", "Weibo")

# 涂色（可选）
cols = c("#ED1C24","#22B14C","#FFC90E","#3f48CC")
# 计算百分比
piepercent = paste(round(100*info/sum(info)), "%")

png(file='runoob-pie.png', height=300, width=300)
# 绘图
pie(info, labels=piepercent, main = "网站分析", col=cols, family='GB1')
# 添加颜色样本标注
legend("topright", names, cex=0.8, fill=cols)
```

#### 条形图

```R
barplot(H,xlab,ylab,main, names.arg,col,beside)
```

- **H** 向量或矩阵，包含图表用的数字值，每个数值表示矩形条的高度。
- **xlab** x 轴标签。
- **ylab** y 轴标签。
- **main** 图表标题。
- **names.arg** 每个矩形条的名称。
- **col** 每个矩形条的颜色。



#### 曲线图

```R
curve(expr, from = NULL, to = NULL, n = 101, add = FALSE,
      type = "l", xname = "x", xlab = xname, ylab = NULL,
      log = NULL, xlim = NULL, …)

# S3 函数的方法，S3 类用的比较广，创建简单粗糙但是灵活
plot(x, y = 0, to = 1, from = y, xlim = NULL, ylab = NULL, …)
```

- expr：函数表达式
- from 和 to：绘图的起止范围
- n：一个整数值，表示 x 取值的数量
- add：是一个逻辑值，当为 TRUE 时，表示将绘图添加到已存在的绘图中。
- type：绘图的类型，p 为点、l 为直线， o 同时绘制点和线，且线穿过点。
- xname：用于 x 轴变量的名称。
- xlim 和 ylim 表示x轴和y轴的范围。
- xlab，ylab：x 轴和 y 轴的标签名称。



#### 散点图

```R
plot(x, y, type="p", main, xlab, ylab, xlim, ylim, axes)
```

- **x** 横坐标 x 轴的数据集合
- **y** 纵坐标 y 轴的数据集合
- type：绘图的类型，p 为点、l 为直线， o 同时绘制点和线，且线穿过点。
- **main** 图表标题。
- **xlab、ylab** x 轴和 y 轴的标签名称。
- **xlim、ylim** x 轴和 y 轴的范围。
- **axes** 布尔值，是否绘制两个 x 轴。

type 参数可选择值：

- p：点图
- l：线图
- b：同时绘制点和线
- c：仅绘制参数 b 所示的线
- o：同时绘制点和线，且线穿过点
- h：绘制出点到横坐标轴的垂直线
- s：阶梯图，先横后纵
- S：阶梯图，先纵后竖
- n： 空图

## R语言实战

### 图形初阶

#### 使用图形

在通常的交互式会话中，你可 以通过逐条输入语句构建图形，逐渐完善图形特征，直至得到想要的效果。

```R
attach(mtcars)
plot(wt, mpg)
abline(lm(mpg~wt))
title("Regression of MPG on Weight") 
detach(mtcars) 
```

首句绑定了数据框mtcars。第二条语句打开了一个图形窗口并生成了一幅散点图，横轴表 示车身重量，纵轴为每加仑汽油行驶的英里数。第三句向图形添加了一条最优拟合曲线。第四句 添加了标题。最后一句为数据框解除了绑定。

可以通过代码或图形用户界面来保存图形。要通过代码保存图形，将绘图语句夹在开启目标图形设备的语句和关闭目标图形设备的语句之间即可。例如，以下代码会将图形保存到当前工作目录中名为`mygraph.pdf`的PDF文件中：

```r
pdf("mygraph.pdf") 
    attach(mtcars) 
    plot(wt, mpg) 
    abline(lm(mpg~wt)) 
    title("Regression of MPG on Weight") 
    detach(mtcars) 
dev.off() 
```

除了PDF，还可以使用`png("filename.png")`、`jpeg("filename.jpg")`等。有时需要创建多个图形并随时查看每一个，可以使用`dev.new()`

```R
x <- c(-10:10)
y1 <- x * 2
y2 <- x*x + 5*x+1
dev.new()
plot(x, y1)
dev.new()
plot(x, y2)
```

可以使用函数`dev.new()`、`dev.next()`、`dev.prev()`、`dev.set()`和`dev.off()`同时打开多个图形窗口，并选择将哪个输出发送到哪个窗口中。这种方法全平台适用。 关于这种方法的更多细节，请参考`help(dev.cur)`。



#### 图形参数

先看一个简单的例子

```R
dose <- c(20, 30, 40, 45, 60) 
drugA <- c(16, 20, 27, 40, 60) 
drugB <- c(15, 18, 25, 31, 40)
plot(dose, drugA, type="p")
```

可以通过修改称为图形参数的选项来自定义一幅图形的多个特征（字体、颜色、坐标轴、标签）。一种方法是通过函数`par()`来指定这些选项。以这种方式设定的参数值除非被再次修改， 否则将在会话结束前一直有效。其调用格式为`par(optionname=value,  optionname=name,...)`。不加参数地执行`par()`将生成一个含有当前图形参数设置的列表。 添加参数`no.readonly=TRUE`可以生成一个可以修改的当前图形参数列表。

```R
opar <- par(no.readonly=TRUE) 
par(lty=2, pch=17)
plot(dose, drugA, type="b") 
par(opar)
```

首个语句复制了一份当前的图形参数设置，第二句将默认的线条类型修改为虚线`lty=2`并将默认的点符号改为了实心三角`pch=17`，然后我们绘制了图形并还原了原始设置。

指定图形参数的第二种方法是为高级绘图函数直接提供optionname=value的键值对。这种 情况下，指定的选项仅对这幅图形本身有效。

```R
plot(dose, drugA, type="b", lty=2, pch=17)
```

 上面这段代码可以生成与上图相同的图形。

符号和线条类型见原书3.3.1节，颜色见原书3.3.2节，文本属性见原书3.3.3节，图形尺寸与边界尺寸见原书3.3.4节

```R
dose <- c(20, 30, 40, 45, 60) 
drugA <- c(16, 20, 27, 40, 60) 
drugB <- c(15, 18, 25, 31, 40) 
opar <- par(no.readonly=TRUE) 
par(pin=c(2, 3)) 
par(lwd=2, cex=1.5) 
par(cex.axis=.75, font.axis=3) 
plot(dose, drugA, type="b", pch=19, lty=2, col="red") 
plot(dose, drugB, type="b", pch=23, lty=6, col="blue", bg="green") 
par(opar)
```

#### 自定义坐标轴和图例

添加文本以下代码在图形上添加了标题（main）、副标题（sub）、坐标轴标签（xlab、ylab）并指定了坐标轴范围（xlim、ylim）。

```R
plot(dose, drugA, type="b", 
    col="red", lty=2, pch=2, lwd=2, 
    main="Clinical Trials for Drug A", 
    sub="This is hypothetical data", 
    xlab="Dosage", ylab="Drug Response", 
    xlim=c(0, 60), ylim=c(0, 70)) 
```

##### 标题和其它

可以使用`title()`函数为图形添加标题和坐标轴标签，函数`title()`中亦可指定其他图形参数（如文本大小、字体、旋转角度和颜色）。举例来说， 以下代码将生成红色的标题和蓝色的副标题，以及比默认大小小25%的绿色x轴、y轴标签

```R
title(main="My Title", col.main="red", 
    sub="My Subtitle", col.sub="blue", 
    xlab="My X label", ylab="My Y label", 
    col.lab="green", cex.lab=0.75) 
```

除了标题，还能设置坐标轴`axis`，参考线`abline`，图例`legend`，文本标注`text`和`mtext`，数学标注（需要安装`latex2exp`），注意`\sum`需要写成`\\sum`

```R
library(latex2exp)
par(pin = c(4, 3), mai = c(1, 1, 1, 1)) # 控制绘图区域
plot(x = c(0, 1), y = c(0, 1), 
     xlab = TeX("$\\sum_{i=1}{n}$"), 
     ylab = TeX("$y=e^{\\beta}$"), 
     main = TeX("$\\frac{a}{b}$"))
text(0.5, 0.5, TeX("$\\sqrt{2}$"))
```

#### 图形的组合

可以在`par()`函数中使用图形参数`mfrow=c(nrows, ncols)`来创建按行填充的、行数为`nrows`、列数为`ncols`的图形矩阵。另外，可以使用`mfcol=c(nrows, ncols)`按列填充矩阵。

```R
attach(mtcars) 
opar <- par(no.readonly=TRUE) 
par(mfrow=c(2,2))
plot(wt,mpg, main="Scatterplot of wt vs. mpg") 
plot(wt,disp, main="Scatterplot of wt vs. disp") 
hist(wt, main="Histogram of wt") 
boxplot(wt, main="Boxplot of wt") 
par(opar) 
detach(mtcars) 
```

除了使用`par()`，还可以用`layout()`，其中的mat是一个矩阵，它指定了所要组合的多个图形的所在位置。在以下代码中，一幅图被置于第1行，另两幅图则被置于第2行：

```R
attach(mtcars) 
layout(matrix(c(1,1,2,3), 2, 2, byrow = TRUE)) 
hist(wt) 
hist(mpg) 
hist(disp) 
detach(mtcars) 
```

其中`layout`的参数为`matrix`，`matrix(c(1,1,2,3), 2, 2, byrow = TRUE)`对应如下矩阵

```
     [,1] [,2]
[1,]    1    1
[2,]    2    3
```

其中数字1、2和3对应三张图片的编号，数字的位置则对应图片的位置，如1在第1行的1、2两列，2在第2行的第1列，3在第2行的第2列，则1对应的图片在第一行，2和3对应的图片在第二行，分别占1、2两列。为了更精确地控制每幅图形的大小，可以有选择地在layout()函数中使用widths=和heights=两个参数。其形式为： 

+ widths = 各列宽度值组成的一个向量
+ heights = 各行高度值组成的一个向量

```R
attach(mtcars) 
layout(matrix(c(1, 1, 2, 3), 2, 2, byrow = TRUE), 
       widths=c(3, 1), heights=c(1, 2)) 
hist(wt) 
hist(mpg) 
hist(disp) 
detach(mtcars)
```

第一列的宽度为3/4，第二列的宽度为1/4；第一行的高度为1/3，第二行的高度为2/3。还有更加精细的布局，参见原书。

### 基本数据管理

#### 缺失值

`is_na`函数检测是否存在缺失值

#### 日期值

日期值通常以字符串的形式输入到R中，然后转化为以数值形式存储的日期变量。函数`as.Date()`用于执行这种转化。其语法为`as.Date(x, "input_format")`，其中`x`是字符型数据，`input_format`则给出了用于读入日期的适当格式。
`%d`：数字表示的日期（0~31） 
`%a`：缩写的星期名
`%A`：非缩写星期名
`%m`：月份（00~12）
`%b`：缩写的月份
`%B`：非缩写月份
`%y`：两位数的年份
`%Y`：四位数的年份

日期值的默认输入格式为yyyy-mm-dd。语句： mydates <- as.Date(c("2007-06-22", "2004-02-13"))
如果以mm/dd/yy的格式编码为字符型变量，有
```R
myformat <- "%m/%d/%y"
leadership$date <- as.Date(leadership$date, myformat)
```

使用`as.character()`可将日期值转换为字符型。

#### 数据排序
可以使用`order()`函数对一个数据框进行排序。默认的排序顺序是升序。在排序变量的 前边加一个减号即可得到降序的排序结果。
```R
a <- c(17,12,32,23,44,29)
print(a[order(a)])  # 12 17 23 29 32 44
print(a[order(-a)]) # 44 32 29 23 17 12
```

#### 取子集
##### subset
```R
newdata <- subset(leadership, age >= 35 | age < 24, select=c(q1, q2, q3, q4))
```
选择所有age值大于等于35或age值小于24的行，保留了变量q1到q4。
##### 随机抽样
`sample()`函数能够让你从数据集中（有放回或无放回地）抽取大小为n的一个随机样本，`sample()`函数中的第一个参数是一个待抽样的元素组成的向量。在这里，这个向量是1到数据框中观测的数量，第二个参数是要抽取的元素数量，第三个参数表示无放回抽样。

### 高级数据管理
#### 数学和统计函数
`scale(x,center=TRUE, scale=TRUE)`：为数据对象x按列进行中心化`(center=TRUE)`或标准化`(center=TRUE,scale=TRUE)`
`quantile(x,probs)`：求分位数，其中x为待求分位数的数值型向量，probs为一个由`[0,1]`之间的概率值组成的数值向量
##### 字符处理函数
`grep(pattern, x, ignore.case=FALSE, fixed=FALSE)`在x中搜索某种模式
`sub(pattern, replacement, x, ignore.case=FALSE, fixed=FALSE)`在x中搜索pattern，并以文本 replacement将其替换
`strsplit(x, split, fixed=FALSE)`在split处分割字符向量x中的元素



### 基本图形

#### 条形图

```R
vec <- c(3,4,2,5,3,1)
barplot(vec, main="Simple barplot", xlab="n", ylab="x(n)")
```

#### 直方图

```R
vec <- c(3,4,2,5,3,1)
hist(vec, col = "blue", main="Simple hist", xlab="n", ylab="x(n)")
```

#### 核密度图

概率密度函数。

#### 箱线图

```R
vec <- 1:10
vec <- c(vec, seq(10, 30, 2))
boxplot(vec, col = "blue", main="Simple hist", xlab="n", ylab="x(n)")
```

<img src="D:\TyporaImages\image-20231221222720796.png" alt="image-20231221222720796" style="zoom: 80%;" />

### 基本统计分析

描述性统计分析、频数表和列联表、相关、t检验、组间差异的非参数检验。

#### 列联表

用于分析两个属性变量是否有联系，由两个以上的变量交叉分类的频数分布表。下面是一个频数列联表。

|       | $B_1$         | $B_2$         | 合计          |
| ----- | ------------- | ------------- | ------------- |
| $A_1$ | $n_{11}$      | $n_{12}$      | $n_{1 \cdot}$ |
| $A_2$ | $n_{21}$      | $n_{22}$      | $n_{2 \cdot}$ |
| $A_3$ | $n_{31}$      | $n_{32}$      | $n_{3 \cdot}$ |
| 合计  | $n_{\cdot 1}$ | $n_{\cdot 2}$ | $n$           |

`table(var1, var2, ...)`：使用N个类别型变量（因子）创建一个N维列联表。

R提供了多种检验类别型变量独立性的方法。本节中描述的三种检验分别为卡方独立性检验、 Fisher精确检验和Cochran-Mantel-Haenszel检验。

#### 相关

如果变量间不独立，还可以衡量变量的相关性度量。R可以计算多种相关系数，包括Pearson相关系数、Spearman相关系数、Kendall相关系数、偏相关系数、多分格（polychoric）相关系数和多系列（polyserial）相关系数。



#### t检验

t检验的前提是要求样本服从正态分布或近似正态分布，不然可以利用一些变换（取对数、开根号、倒数等等）试图将其转化为服从正态分布的数据，如若还是不满足正态分布，只能利用非参数检验方法。不过当样本量大于30的时候，可以认为数据近似正态分布。

t检验最常见的四个用途：

1. 单样本均值检验（One-sample *t*-test）
    用于检验**总体方差未知、正态数据或近似正态的单样本的均值是否与已知的总体均值相等**
2. 两独立样本均值检验（Independent two-sample *t*-test）
    用于检验两**对独立的 正态数据或近似正态的样本的均值是否相等**，这里可根据总体方差是否相等分类讨论
3. 配对样本均值检验（Dependent *t*-test for paired samples）
    用于检验**一对配对样本的均值的差是否等于某一个值**
4. 回归系数的显著性检验（t-test for regression coefficient significance）
    用于检验**回归模型的解释变量对被解释变量是否有显著影响**

单样本均值检验实际上就是假设拒绝检验。



### 回归

#### 普通最小二乘（OLS）回归

在R中，拟合线性模型最基本的函数就是`lm()`，格式为：

```R
myfit <- lm(formula, data)
```

其中，`formula`指要拟合的模型形式，`data`是一个数据框，包含了用于拟合模型的数据。

R的表达式中有一些常用的负号

`~`：分隔符号，左边为响应变量，右边为解释变量。例如，要通过x、z和w预测y，代码为`y~x+z+w`

`+`：分隔预测变量

`:`：表示预测变量的交互项。例如，要通过x、z及x与z的交互项预测y，代码为`y~x+z+x:z`

`*`：表示所有可能交互项的简洁方式。`y~x*z*w`可展开为`y~x+z+w+x:z+x:w+z:w+x:z:w`

`.`：表示包含除因变量外的所有变量。例如，若一个数据框包含变量x、y、z和w，代码`y~.`可展开为`y~ x+z+w`

`-`：减号，表示从等式中移除某个变量。例如，`y~(x + z + w)^2-x:w`可展开为`y~x+z+w+x:z+z:w`

`^`：表示交互项达到某个次数。代码`y~(x+z+w)^2`可展开为`y~x+z+w+x:z+x:w+z:w`

`I()`：从算术的角度来解释括号中的元素，代码`y~x+I((z+w)^2)`将展开为`y~x+h`，h是一个由z和w的平方和创建的新变量



##### 简单线性回归

```R
x <- c(1:50)
y <- x * 3 + 5 + rnorm(50, 2, 4)
sp = data.frame(
  x <- x,
  y <- y
)
fit <- lm(y~x, data=sp)
print(fit$coefficients)
plot(x, y)
par(col="red")
lines(x, fit$coefficients['x'] * x + fit$coefficients['(Intercept)'], type = 'l', )
```

##### 多项式回归

```R
x <- c(1:20)
y <- x^2 + x * 3 + 5 + 10*rnorm(20, 0, 1)
sp = data.frame(
  x <- x,
  y <- y
)
fit <- lm(y~I(x^2)+x, data=sp)
print(summary(fit))
par(col="grey")
print(fit$coefficients)
plot(x, y)
par(col="red")
lines(x, fit$coefficients['I(x^2)'] * (x^2)+fit$coefficients['x'] * x + fit$coefficients['(Intercept)'], type = 'l', )
```

#### 异常观测值

一个全面的回归分析要覆盖对异常值的分析，包括离群点、高杠杆值点和强影响点。

##### 离群点

离群点是指那些模型预测效果不佳的观测点。它们通常有很大的、或正或负的残差$Y_t-\hat{Y}_t$

##### 高杠杆值点

高杠杆值观测点，即与其他预测变量有关的离群点。换句话说，它们是由许多异常的预测变量值组合起来的，与响应变量值没有关系。高杠杆值的观测点可通过帽子统计量（hat statistic）判断。

##### 强影响点

强影响点，即对模型参数估计值影响有些比例失衡的点。有两种方法可以检测强影响点：Cook距离，或称D统计量，以及变量添加图（added variable  plot）。



### 方差分析

#### 单因素方差分析（ANOVA）

检验每个组的**平均数**是否相同，判断表现是否有显著的区别。

ANOVA有主要有以下3个假设：

1. 方差的同质性。可以理解为每组样本背后的总体（也叫族群）都有相同的方差；
2. 族群遵循正态分布；
3. 每一次抽样都是独立的。

ANOVA中有两个重要概念：组间均方（mean squared between, MSB），相当于每个族群相对于总体的方差；组内均方（mean squared error, MSE），也就是每个分布自身的方差。

通过$F=MSB/MSE$（具体做法比较复杂，还需知道分子分母的自由度，查表）来判断是否接受每组的平均数相等的假设

#### 单因素协方差分析（ANCOVA）

单因素协方差分析（ANCOVA）扩展了单因素方差分析（ANOVA），包含一个或多个定量的协变量。



#### 双因素方差分析



#### 重复测量方差分析



#### 多元方差分析

当因变量（结果变量）不止一个时，可用多元方差分析（MANOVA）对它们同时进行分析。



### 功效分析

功效分析可以帮助在给定置信度的情况下，判断检测到给定效应值时所需的样本量。反过来， 它也可以帮助你在给定置信度水平情况下，计算在某样本量内能检测到给定效应值的概率。如果 概率低得难以接受，修改或者放弃这个实验将是一个明智的选择。

习如何对多种统计检验进行功效分析，包括比例检验、t检验、卡方检验、 平衡的单因素ANOVA、相关性分析，以及线性模型分析。由于功效分析针对的是假设检验，我 们将首先简单回顾零假设显著性检验（NHST）过程，然后学习如何用R进行功效分析，主要关注pwr包。最后，我们还会学习R中其他可用的功效分析方法。



### 中级绘图

#### 散点图

使用`pairs()`函数创建基础的散点图矩阵，`car`包中的`scatterplotMatrix()`函数也可以用于生成散点图矩阵

```R
pairs(~mpg+disp+drat+wt, data=mtcars, main="Basic Scatter Plot Matrix") 
```

如果遇到了数据点重叠很严重时，用散点图来观察变量关系就显得“力不从心”了。可以使用`smoothScatter()`函数利用核密度估计生成用颜色密度来表示点分布的散点图。下面是一个例子

```R
set.seed(1234) 
n <- 10000 
c1 <- matrix(rnorm(n, mean=0, sd=.5), ncol=2) 
c2 <- matrix(rnorm(n, mean=3, sd=2), ncol=2) 
mydata <- rbind(c1, c2) 
mydata <- as.data.frame(mydata) 
names(mydata) <- c("x", "y") 
with(mydata, smoothScatter(x, y, main="Scatter Plot Colored by Smoothed Densities"))
```

还可以使用`hexbin()`函数将二元变量的封箱放到六边形单元格中，生成用颜色密度来表示点分布的散点图。

散点图和散点图矩阵展示的都是二元变量关系。倘若想一次对三个定量变量的交互关系进行可视化呢？可以使用三维散点图。可以使用`scatterplot3d`包中的`scatterplot3d()`函数来绘制它们的关系

```R
library(scatterplot3d)
attach(mtcars)
scatterplot3d(wt, disp, mpg, main="Basic 3D Scatter Plot")
```

可以在这幅图上加上一个回归面

```R
library(scatterplot3d) 
attach(mtcars) 
s3d <-scatterplot3d(wt, disp, mpg, pch=16, highlight.3d=TRUE, type="h", 
                    main="3D Scatter Plot with Vertical Lines and Regression Plane") 
fit <- lm(mpg ~ wt+disp) 
s3d$plane3d(fit)
```

如果希望创建可交互的三维散点图，可以使用`rgl`包中的`plot3d()`函数。

除了使用三维散点图来展示三个定量变量间的关系。现在介绍另外一种思路：先创建一个二维散点图，然后用点的大小来代表第三个变量的值。这便是气泡图。

```R
attach(mtcars) 
r <- sqrt(disp/pi) 
png("bubble1.png")
symbols(wt, mpg, circle=r, inches=0.30, fg="white", bg="lightblue", 
        main="Bubble Plot with point size proportional to displacement", 
        ylab="Miles Per Gallon", xlab="Weight of Car (lbs/1000)") 
text(wt, mpg, rownames(mtcars), cex=0.6) 
detach(mtcars)
dev.off()
```



#### 相关图

使用`cor`函数可以获得相关矩阵，`corrgram`包中的`corrgram()`函数可以绘制相关图

#### 马赛克图

若有两个以上的类别型变量，可以使用三维柱状图，或者马赛克图

```R
mosaicplot(~Class+Sex+Age+Survived, data=Titanic, shade=TRUE)
```


### 重抽样与自助法

#### 置换检验

假设在一个有两种处理方式的实验，如何说明两种处理方式的影响不同。

在参数方法中，你可能会假设数据抽样自等方差的正态分布，然后使用假设独立分组的双尾`t`检验来验证结果。此时，零假设为A处理的总体均值与B处理的总体均值相等，根据数据计算了`t`统计量，将其与理论分布进行比较，如果观测到的`t`统计量值十分极端，比如落在理论分布值的95%置信区间外，那么你将会拒绝零假设，断言在0.05的显著性水平下两组的总体均值不相等。

置换检验的思路与之不同。如果两种处理方式真的等价，那么分配给观测得分的标签（A处理或B处理）便是任意的。为检验两种处理方式的差异，我们可遵循如下步骤： 

(1) 与参数方法类似，计算观测数据的t统计量，称为t0；

(2) 将10个得分放在一个组中；

(3) 随机分配五个得分到A处理中，并分配五个得分到B处理中；

(4) 计算并记录新观测的t统计量；

(5) 对每一种可能随机分配重复步骤(3)~(4)，此处有252种可能的分配组合$C_{10}^5=252$；

(6) 将252个t统计量按升序排列，这便是基于（或以之为条件）样本数据的经验分布；

(7) 如果t0落在经验分布中间95%部分的外面，则在0.05的显著性水平下，拒绝两个处理组的总体均值相等的零假设。

可以使用`coin`包做置换检验。

```R
library(coin) 
score <- c(40, 57, 45, 55, 58, 57, 64, 55, 62, 65) 
treatment <- factor(c(rep("A",5), rep("B",5))) 
mydata <- data.frame(treatment, score) 
test <- t.test(score~treatment, data=mydata, var.equal=TRUE)
print(test)
```

依靠基础的抽样分布理论知识，置换检验提供了另外一个十分强大的可选检验思路。对于上面描述的每一种置换检验，我们完全可以在做统计假设检验时不理会正态分布、t分布、F分布或者卡方分布。置换检验真正发挥功用的地方是处理非正态数据（如分布偏倚很大）、存在离群点、样本很小或无法做参数检验等情况。不过，如果初始样本对感兴趣的总体情况代表性很差，即使是置换检验也无法提高推断效果。置换检验主要用于生成检验零假设的p值，它有助于回答“效应是否存在”这样的问题。置换方法对于获取置信区间和估计测量精度是比较困难的，不过这可以通过自助法来解决。



#### 自助法

所谓自助法，即从初始样本重复随机替换抽样，生成一个或一系列待检验统计量的经验分布。 无需假设一个特定的理论分布，便可生成统计量的置信区间，并能检验统计假设。

比如，你想计算一个样本均值95%的置信区 间。样本现有10个观测，均值为40，标准差为5。如果假设均值的样本分布为正态分布，那么 (1–α/2)%的置信区间计算如下：
$$
\bar X - t{s \over {\sqrt n }} < \mu  < \bar X + t{s \over {\sqrt n }}
$$
其中，t是自由度为n–1的t分布的1–α上界值。

倘若你假设均值的样本分布不是正态分布，该怎么办呢？可使用自助法。

(1) 从样本中随机选择10个观测，抽样后再放回。有些观测可能会被选择多次，有些可能一直都不会被选中。 

(2) 计算并记录样本均值。

(3) 重复1和2一千次。

(4) 将1000个样本均值从小到大排序。

(5) 找出样本均值2.5%和97.5%的分位点。此时即初始位置和最末位置的第25个数，它们就限定了95%的置信区间。

在许多案例中，自助法优势会十分明显。比如，你想估计样本中位数的置信区间，或者两样本中位数之差，该怎么做呢？正态理论没有现成的简单公式可套用，而自助法此时却是不错的选择。即使潜在分布未知，或出现了离群点，或者样本量过小，再或者是没有可供选择的参数方法，自助法将是生成置信区间和做假设检验的一个利器。

`boot`包扩展了自助法和重抽样的相关用途。

如果想获得95%的R平方值的置信区间（预测变量对响应变量可解释的方差比），那么便可使用非参数的自助法来获取置信区间。

```R
rsq <- function(formula, data, indices) { 
  d <- data[indices,]    # 该语句必须声明，因为boot()要用其来选择样本
  fit <- lm(formula, data=d) 
  return(summary(fit)$r.square) 
}
library(boot)
set.seed(1234)
results <- boot(data = mtcars, statistic = rsq, R=1000, formula=mpg~wt+disp)
print(results)
plot(results)
```



### 广义线性模型

线性模型可以通过一系列连续型和/或类别型预测变量来预测正态分布的响应变量。广义线性模型扩展了线性模型的框架，包含了非正态因变量的分析。
#### 广义线性模型与glm
广义线性模型拟合的形式为：
$$
g({\mu _Y}) = {\beta _0} + \sum\limits_{j = 1}^p {{\beta _j}{X_j}}
$$
预测变量$X_j$不需要呈正态分布，另外，对预测变量使用非线性函数也是允许的，比如你常会使用预测变量$X^2$或者$X_1\times X_2$，只要等式的参数$(\beta_0, \beta_1, \cdots, \beta_p)$为线性即可。
使用`glm()`函数拟合广义线性模型，函数的基本形式为：
```R
glm(formula, family=family(link=function) data=)
```
`glm()`函数可以拟合许多流行的模型，比如Logistic回归、泊松回归。
Logistic回归适用于二值响应变量（0和1）。模型假设Y服从二项分布，线性模型的拟合形式为：
$$
{\log _e}\left( {{\pi  \over {1 - \pi }}} \right) = {\beta _0} + \sum\limits_{j = 1}^p {{\beta _j}{X_j}}
$$
其中$\pi=\mu_Y$是Y的条件均值，即给定一系列X的值时Y=1的概率。${\pi  \over {1 - \pi }}$为Y=1时的优势比，$\log \left( {{\pi  \over {1 - \pi }}} \right)$为对数优势比。
```R
glm(Y~X1+X2+X3, family=binomial(link="logit"), data=mydata) 
```
泊松回归适用于在给定时间内响应变量为事件发生数目的情形。它假设Y服从泊松分布，线性模型的拟合形式为：
$$
{\log _e}(\lambda ) = {\beta _0} + \sum\limits_{j = 1}^p {{\beta _j}{X_j}}
$$
其中$\lambda$是$Y$的均值（也等于方差）。此时，连接函数为log(λ)，概率分布为泊松分布，可用如下代码 拟合泊松回归模型：
```R
glm(Y~X1+X2+X3, family=poisson(link="log"), data=mydata)
```
如果令连接函数$g({\mu _Y}) = {\mu _Y}$或恒等函数，并设定概率分布为正态（高斯）分布，那么glm和lm相同。
**与glm连用的函数（lm也可以连用）**

| 函数                   | 描述                                |
| ---------------------- | ----------------------------------- |
| summary()              | 展示拟合模型的细节                  |
| coefficients(), coef() | 列出拟合模型的参数（截距项和斜率）  |
| confint()              | 给出模型参数的置信区间（默认为95%） |
| residuals()            | 列出拟合模型的残差值                |
| anova()                | 生成两个拟合模型的方差分析表        |
| plot()                 | 生成评价拟合模型的诊断图            |
| predict()              | 用拟合模型对新数据集进行预测        |
| deviance()             | 拟合模型的偏差                      |
| df.residual()          | 拟合模型的残差自由度                |



### 主成分分析和因子分析

`principal()`函数可以根据原始数据矩阵或者相关系数矩阵做主成分分析。格式为： 

```R
principal(r, nfactors=, rotate=, scores=)
```

其中：

1. r是相关系数矩阵或原始数据矩阵；
2. nfactors设定主成分数（默认为1）；
3. rotate指定旋转的方法；
4. scores设定是否需要计算主成分得分（默认不需要）

主成分旋转是一系列将成分载荷阵变得更容易解释的数学方法，它们尽可能地对成分去噪。旋转方 法有两种：使选择的成分保持不相关（正交旋转），和让它们变得相关（斜交旋转）。


探索性因子分析的目标是通过发掘隐藏在数据下的一组较少的、更为基本的无法观测的变量，来解释一 组可观测变量的相关性。这些虚拟的、无法观测的变量称作因子。（每个因子被认为可解释多个 观测变量间共有的方差，因此准确来说，它们应该称作公共因子。）模型的形式为：
$$
{X_i} = {a_1}{F_1} + {a_2}{F_2} +  \cdots  + {a_p}{F_p} + {U_i}
$$
其中$X_i$是第$i$个可观测变量$(i=1\cdots k)$，$F_j$是公共因子$(j=1\cdots k)$，并且$p<k$。$U_i$是$X_i$变量独有的部分（无法被公共因子解释）。$a_i$可认为是每个因子对复合而成的可观测变量的贡献值。
使用`fa.parallel()`函数可判断需提取的因子数，`fa()`函数可以提取因子。

### 时间序列

#### 时序的季节性分解
`ts()`用于生成时序对象，`start()`和`end()`用于返回开始日期和结束日期
```R
sales <- c(18, 33, 41, 7, 34, 35, 24, 25, 24, 21, 25, 20, 
           22, 31, 40, 29, 25, 21, 22, 54, 31, 25, 26, 35)
tsales <- ts(sales, start=c(2003, 1), frequency=12)
print(tsales)
```
存在季节性因素的时间序列数据（如月度数据、季度数据等）可以被分解为趋势因子、季节性因子和随机因子。趋势因子（trend component）能捕捉到长期变化；季节性因子（seasonal component）能捕捉到一年内的周期性变化；而随机（误差）因子（irregular/error component）则能捕捉到那些不能被趋势或季节效应解释的变化。
可以通过相加模型，也可以通过相乘模型来分解数据。在相加模型中，各种因子之和应等于对应的时序值，即：
$$
{Y_t} = Tren{d_t} + Seasona{l_t} + Irregula{r_t}
$$
其中时刻`t`的观测值即这一时刻的趋势值、季节效应以及随机影响之和。
相乘模型则将时间序列表示为：
$$
{Y_t} = Tren{d_t} \times Seasona{l_t} \times Irregula{r_t}
$$
可以通过R中的`stl()`函数实现
```R
stl(ts, s.window=, t.window=)
```
其中`ts`是将要分解的时序，参数`s.window`控制季节效应变化的速度，`t.window`控制趋势项变化的速度。较小的值意味着更快的变化速度。令`s.windows="periodic"`可使得季节效应在各年间都一样。

#### 指数预测模型
指数模型是用来预测时序未来值的最常用模型。这类模型相对比较简单，但是实践证明它们 的短期预测能力较好。不同指数模型建模时选用的因子可能不同。比如单指数模型（simple/single exponential model）拟合的是只有常数水平项和时间点i处随机项的时间序列，这时认为时间序列 不存在趋势项和季节效应；双指数模型（double exponential model；也叫Holt指数平滑，Holt exponential smoothing）拟合的是有水平项和趋势项的时序；三指数模型（triple exponential model；也叫Holt-Winters指数平滑，Holt-Winters exponential smoothing）拟合的是有水平项、趋势项以及季节效应的时序。
R中自带的HoltWinters()函数或者forecast包中的ets()函数可以拟合指数模型。

#### ARIMA预测模型
ARIMA(p, d, q)模型意味着时序被差分了d次，且序列中的每个观测值都是用过去的p个观测值和q个残差的线性组合表示的。预测是“无误差的”或完整（integrated）的，来实现最终的预测。 
建立ARIMA模型的步骤包括：
(1) 确保时序是平稳的（对数据进行差分）；
(2) 找到一个（或几个）合理的模型（即选定可能的p值和q值，通过ACF图和PACF图来确定）；
(3) 拟合模型；
(4) 从统计假设和预测准确性等角度评估模型；
(5) 预测。

```R
fit <- arima(sunspots)
print(fit)
```

### 聚类分析
最常用的两种聚类方法是层次聚类和划分聚类。在层次聚类中，每一个观测值自成一类，这些类每次两两合并，直到所 有的类被聚成一类为止。在划分聚类中，首先指定类的个数K，然后观测值被随机分成K类，再 重新形成聚合的类。对于层次聚类来说，最常用的算法是单联动、全联动、平均联动、质心和Ward方法。对于划分聚类来说，最常用的算法是K均值和围绕中心点的划分。
#### 层次聚类分析
在层次聚类中，起初每一个实例或观测值属于一类。聚类就是每一次把两类聚成 新的一类，直到所有的类聚成单个类为止，算法如下：
(1) 定义每个观测值（行或单元）为一类；
(2) 计算每类和其他各类的距离；
(3) 把距离最短的两类合并成一类，这样类的个数就减少一个；
(4) 重复步骤(2)和步骤(3)，直到包含所有观测值的类合并成单个的类为止。
在层次聚类算法中，主要的区别是它们对类的定义不同。

| 聚类方法 | 两类之间的距离定义                     |
| -------- | -------------------------------------- |
| 单联动   | 一个类中的点和另一个类中的点的最小距离 |
| 全联动   | 一个类中的点和另一个类中的点的最大距离 |
| 平均联动 | 一个类中的点和另一个类中的点的平均距离 |
| 质心     | 两类中质心（变量均值向量）之间的距离   |
| Ward法   | 两个类之间所有变量的方差分析的平方和   |

单联动聚类方法倾向于发现细长的、雪茄型的类。它也通常展示一种链式的现象，即不相似的观测值分到一类中，因为它们和它们的中间值很相像。全联动聚类倾向于发现大致相等的直径紧凑类。它对异常值很敏感。平均联动提供了以上两种方法的折中。相对来说，它不像链式，而且对异常值没有那么敏感。它倾向于把方差小的类聚合。Ward法倾向于把有少量观测值的类聚合到一起，并且倾向于产生与观测值个数大致相等的类。它对异常值也是敏感的。质心法是一种很受欢迎的方法，因为其中类距离的定义比较简单、 易于理解。相比其他方法，它对异常值不是很敏感。但是它可能不如平均联动法或Ward方法表现得好。

层次聚类方法可以用`hclust()`函数来实现，格式是`hclust(d, method=)`，其中`d`是通过`dist()`函数产生的距离矩阵，并且方法包括`"single"`、`"complete"`、`"average"`、`"centroid"`和`"ward"`。

```R
data(nutrient, package = "flexclust")
row.names(nutrient) <- tolower(row.names(nutrient)) 
nutrient.scaled <- scale(nutrient) 
d <- dist(nutrient.scaled)
fit.average <- hclust(d, method = "average")
plot(fit.average, hang=-1, cex=.8, main="Average Linkage Clustering")
```

`plot()`函数中的`hang`命令展示观测值的标签（让它们在挂在0下面）。

```R
clusters <- cutree(fit.average, k=5)
table(clusters)
print(aggregate(nutrient, by=list(cluster=clusters), median))
```

使用`cutree()`把树状图分成五类，`aggregate()`函数用来获取每类的中位数。

#### 划分聚类分析

R中的K均值的函数格式是`kmeans(x, centers)`，这里x表示数值数据集（矩阵或数据框）， centers是要提取的聚类数目。`kmeans()`函数有一个nstart选项尝试多种初始配置并输出最好的一个。例如，加上`nstart=25`会生成25个初始配置。通常推荐使用这种方法。
因为K均值聚类方法是基于均值的，所以它对异常值是敏感的。一个更稳健的方法是围绕中心点的划分（PAM）。与其用质心（变量均值向量）表示类，不如用一个最有代表性的观测值来表示（称为中心点）。
PAM算法如下：
(1) 随机选择K个观测值（每个都称为中心点）；
(2) 计算观测值到各个中心的距离/相异性；
(3) 把每个观测值分配到最近的中心点；
(4) 计算每个中心点到每个观测值的距离的总和（总成本）；
(5) 选择一个该类中不是中心的点，并和中心点互换；
(6) 重新把每个点分配到距它最近的中心点；
(7) 再次计算总成本；
(8) 如果总成本比步骤(4)计算的总成本少，把新的点作为中心点；
(9) 重复步骤(5)～(8)直到中心点不再改变。
可以使用cluster包中的`pam()`函数使用基于中心点的划分方法。格式是`pam(x, k, metric="euclidean", stand=FALSE)`，这里的x表示数据矩阵或数据框，k表示聚类的个数， metric表示使用的相似性/相异性的度量，而stand是一个逻辑值，表示是否有变量应该在计算 该指标之前被标准化。

### 分类
通过`rpart`、`rpart.plot`和`party`包来实现决策树模型及其可视化，通过`randomForest`包拟合随机森林，通过`e1071`包构造支持向量机，通过R中的基本函数`glm()`实现逻辑回归。

使用的数据如下：
```R
loc <- "http://archive.ics.uci.edu/ml/machine-learning-databases/" 
ds <- "breast-cancer-wisconsin/breast-cancer-wisconsin.data" 
url <- paste(loc, ds, sep="") 
breast <- read.table(url, sep=",", header=FALSE, na.strings="?") 
names(breast) <- c("ID", "clumpThickness", "sizeUniformity",
                   "shapeUniformity", "maginalAdhesion",
                   "singleEpithelialCellSize", "bareNuclei",
                   "blandChromatin", "normalNucleoli", "mitosis", "class")
df <- breast[-1]
df$class <- factor(df$class, levels=c(2,4),
                   labels=c("benign", "malignant")) 
set.seed(1234)
train <- sample(nrow(df), 0.7*nrow(df))
df.train <- df[train,]
df.validate <- df[-train,]
table(df.train$class)
table(df.validate$class)
```

#### 逻辑回归
逻辑回归是广义线性模型的一种，可根据一组数值变量预测二元输出。R中的基本函数`glm()`可用于拟合逻辑回归模型。`glm()`函数自动将预测变量中的分类变量编码为相应的虚拟变量。
```R
fit.logic <- glm(class~., data=df.train, family = binomial())
print(summary(fit.logic))
prob <- predict(fit.logic, df.validate, type="response")
logit.pred <- factor(prob > .5, levels = c(FALSE, TRUE), labels = c("benign", "mailgnant"))
logit.perf <- table(df.validate$class, logit.pred, dnn = c("Actual", "Predicted"))
print(logit.perf)
```

#### 经典决策树
R中的rpart包支持`rpart()`函数构造决策树，`prune()`函数对决策树进行剪枝。
```R
library(rpart)
set.seed(1234)
dtree <- rpart(class ~., data = df.train, method="class", parms = list(split="information"))
print(dtree$cptable)
plotcp(dtree)
dtree.pruned <- prune(dtree, cp=.0125)
library(rpart.plot)
prp(dtree.pruned, type = 2, extra = 104, fallen.leaves = TRUE, main="Decision Tree")
dtree.pred <- predict(dtree.pruned, df.validate, type="class")
dtree.perf <- table(df.validate$class, dtree.pred, 
                      dnn=c("Actual", "Predicted")) 
print(dtree.perf)
```
`prune()`函数根据复杂度参数剪掉最不重要的枝，从而将树的大小控制在理想范围内。`rpart.plot`包中的`prp()`函数可用于画出最终的决策树，`predict()`函数用来对验证集中的观测点分类。

#### 随机森林
假设训练集中共有N个样本单元，M个变量，则随机森林算法如下。 
(1) 从训练集中随机有放回地抽取N个样本单元，生成大量决策树
(2) 在每一个节点随机抽取m<M个变量，将其作为分割该节点的候选变量。每一个节点处的变量数应一致
(3) 完整生成所有决策树，无需剪枝（最小节点为1）
(4) 终端节点的所属类别由节点对应的众数类别决定
(5) 对于新的观测点，用所有的树对其进行分类，其类别由多数决定原则生成
```R
library(randomForest)
set.seed(1234)
fit.forest <- randomForest(class~., data=df.train, na.action=na.roughfix, importance=TRUE)
print(fit.forest)
print(importance(fit.forest, type=2))
forest.pred <- predict(fit.forest, df.validate) 
forest.perf <- table(df.validate$class, forest.pred, dnn=c("Actual", "Predicted")) 
print(forest.perf)
```

#### 支持向量机
支持向量机（SVM）是一类可用于分类和回归的有监督机器学习模型。其流行归功于两个方 面：一方面，他们可输出较准确的预测结果；另一方面，模型基于较优雅的数学理论。SVM旨在在多维空间中找到一个能将全部样本单元分成两类的最优平面，这一平面应使两类中距离最近的点的间距（margin）尽可能大，在间距边界上的点被称为支持向量（support vector，它们决定间距），分割的超平面位于间距的中间。

SVM可以通过R中kernlab包的`ksvm()`函数和e1071包中的`svm()`函数实现。`ksvm()`功能更强大，但`svm()`相对更简单。
```R
library(e1071)
set.seed(1234)
fit.svm <- svm(class ~., data=df.train)
print(fit.svm)
svm.pred <- predict(fit.svm, na.omit(df.validate)) 
svm.perf <- table(na.omit(df.validate)$class, svm.pred, dnn=c("Actual", "Predicted")) 
print(svm.perf) 
```

#### 用 rattle 包进行数据挖掘
Rattle（R Analytic Tool to Learn Easily）为R语言用户提供了一个可做数据分析的图像式交互界面（GUI）。RGTK2包安装不了，暂时不能使用。



### 处理缺失数据的高级方法

一个完整的处理方法通常包含以下几个步骤：
(1) 识别缺失数据；
(2) 检查导致数据缺失的原因；
(3) 删除包含缺失值的实例或用合理的数值代替（插补）缺失值。

#### 识别缺失值
R中的函数`is.na()`、`is.nan()`和`is.infinite()`可分别用来识别缺失值、不可能值和无穷值。
函数`complete.cases()`可以用来识别矩阵或数据框中没有缺失值的行。若每行都包含完整的实例，则返回TRUE的逻辑向量；若每行有一个或多个缺失值，则返回FALSE。
```R
data(sleep, package = "VIM")
print(sleep[complete.cases(sleep),])
print(sleep[!complete.cases(sleep),])
```

#### 探索缺失值模式
mice包中的`md.pattern()`函数可生成一个以矩阵或数据框形式展示缺失值模式的表格。
VIM包提供了大量能可视化数据集中缺失值模式的函数，如`aggr()`、`matrixplot()`和`scattMiss()`
可以用指示变量替代数据集中的数据（1表示缺失，0表示存在），这样生成的矩阵有时被称作影子矩阵。求这些指示变量之间和它们与初始（可观测）变量之间的相关性，有助于观察哪些变量常一起缺失，以及分析变量“缺失”与其他变量间的关系。

#### 多重插补

多重插补（MI）是一种基于重复模拟的处理缺失值的方法。在面对复杂的缺失值问题时，MI是最常选用的方法，它将从一个包含缺失值的数据集中生成一组完整的数据集。
函数mice()首先从一个包含缺失数据的数据框开始，然后返回一个包含多个（默认为5个） 完整数据集的对象。每个完整数据集都是通过对原始数据框中的缺失数据进行插补而生成的。
R中还支持其他一些处理缺失值的方法

| 软件包           | 描述                                                     |
| ---------------- | -------------------------------------------------------- |
| mvnmle           | 对多元正态分布数据中缺失值的最大似然估计                 |
| cat              | 对数线性模型中多元类别型变量的多重插补                   |
| arrayImpute      | 处理微阵列缺失数据的实用函数                             |
| longitudinalData | 相关的函数列表，比如对时间序列缺失值进行插补的一系列函数 |
| kmi              | 处理生存分析缺失值的Kaplan-Meier多重插补                 |
| mix              | 一般位置模型中混合类别型和连续型数据的多重插补           |
| pan              | 多元面板数据或聚类数据的多重插补                         |



### 使用ggplot2进行高级绘图

```R
library(ggplot2)
ggplot(data = mtcars, aes(x=wt, y=mpg)) + geom_point() +
         labs(title = "Automobile Data", x="Weight", y="Miles Per Gallon")
```
ggplot()初始化图形并且指顶要用到的数据来源（mtcars）和变量（wt、 mpg）。aes()函数的功能是指定每个变量扮演的角色（aes代表aesthetics，即如何用视觉形式呈现信息）。在这里，变量wt的值映射到沿x轴的距离，变量mpg的值映射到沿y轴的距离。
在ggplot2中有很多的函数，并且大多数包含可选的参数。扩展一下前面的例子，代码如下：
```R
library(ggplot2) 
plot(ggplot(data=mtcars, aes(x=wt, y=mpg)) + 
  geom_point(pch=17, color="blue", size=2) + 
  geom_smooth(method="lm", color="red", linetype=2) + 
  labs(title="Automobile Data", x="Weight", y="Miles Per Gallon"))
```
`ggplot()`函数指定要绘制的数据源和变量，几何函数则指定这些变量如何在视觉上进行表示（使用点、条、线和阴影区）。几何函数一共有37个，下面只给出了4个。
线图：`geom_line()`；散点图：`geom_point()`；拟合曲线：`geom_smooth()`；文字注解：`geom_text()`

`scale_x_continuous()`和`scale_y_continuous`：breaks=指定刻度标记，labels=指定刻度标记标签，limits=控制要展示的值的范围
`scale_x_discrete()`和`scale_y_discrete()`：breaks=对因子的水平进行放置和排序，labels=指定这些水平的标签，limits=表示哪些水平应该展示 
`coord_flip()`：颠倒x轴和y轴

使用gridExtra包中的grid.arrange()函数可以同时展示多张图片
```R
data(Salaries, package="carData") 
library(ggplot2) 
p1 <- ggplot(data=Salaries, aes(x=rank)) + geom_bar() 
p2 <- ggplot(data=Salaries, aes(x=sex)) + geom_bar() 
p3 <- ggplot(data=Salaries, aes(x=yrs.since.phd, y=salary)) + geom_point() 
library(gridExtra) 
grid.arrange(p1, p2, p3, ncol=3)
```
保存图片可以使用`ggsave()`

### 高级编程
多行语句可以用`+`号连接
`ifelse()`是`if()`的量化版本，矢量化允许一个函数来处理没有明确循环的对象，类似于三元表达式
```R
ifelse(test, yes, no)
```
其中test是已强制为逻辑模式的对象，yes返回test元素为真时的值，no返回test元素为假时的值。

处于全局环境时可以通过new.env()函数创建一个新的环境并通过assign()函数在环境中创建任务。
```R
x<-5
myenv <- new.env()
assign("x", "Homer", env = myenv)
print(ls())
print(ls(myenv))
print(x)    # 5
print(get("x", env=myenv))  # "Homer"
```
可以使用foreach和doParallel 包在单机上并行化运行。foreach包支持 foreach循环构建（遍历集合中的元素）同时便于并 行执行循环。doParallel包为foreach包提供了一个平行的后端。
```R
library(foreach)
library(doParallel) 
registerDoParallel(cores=4)
eig <- function(n, p){ 
  x <- matrix(rnorm(100000), ncol=100)
  r <- cor(x)
  eigen(r)$values 
} 
n <- 100000 
p <- 100 
k <- 500
system.time(x <- foreach(i=1:k, .combine=rbind) %do% eig(n, p))     # 常规执行
system.time(x <- foreach(i=1:k, .combine=rbind) %dopar% eig(n, p))  # 并行执行
```

### 创建包
不过多介绍，如果需要调用自己写的函数，可以使用`source("fun.R")`

### 创建动态报告
使用R和Markdown来创建动态报告，还可以利用`R2wd`用R和Microsoft Word创建动态报告

```R
library(rmarkdown) 
render("main.Rmd", "html_document") 
```




### 使用lattice进行高级绘图
```R
library(lattice) 
histogram(~height | voice.part, data = singer, 
          main="Distribution of Heights by Voice Pitch", 
          xlab="Height (inches)")
```
height是独立的变量，`|`后面的voice.part被称作调节变量。
lattice包提供了大量的函数来产生单因素图（点图、核密度图、直方图、条形图、箱线图），二元图（散点图、条形图、平行箱线图）和多元图（3D图、散点图矩阵）。每个高水平的画图函数都服从下面的格式：`graph_function(formula, data=, options)`
其中：
graph_function是下表中的一个绘图函数；
formula指定要展示的变量和任意的调节变量；
data=指定数据框；
options是用逗号分隔的参数，用来调整图形的内容、安排和注释。

| 图类型         | 函数           | 公式例子  |
| -------------- | -------------- | --------- |
| 3D等高线图     | contourplot()  | z~x*y     |
| 3D水平图       | levelplot()    | z~y*x     |
| 3D散点图       | cloud()        | z~x*y\|A  |
| 3D线框图       | wireframe()    | z~y*x     |
| 条形图         | barchart()     | x~A或A~x  |
| 箱线图         | bwplot()       | x~A或A~x  |
| 点图           | dotplot()      | ~x\|A     |
| 柱状图         | histogram()    | ~x        |
| 核密度图       | densityplot()  | ~x\|A*B   |
| 平行坐标曲线图 | parallelplot() | dataframe |
| 散点图         | xyplot()       | y~x\|A    |
| 散点图矩阵     | splom()        | dataframe |
| 线框图         | stripplot()    | A~x或x~A  |



#### 调节变量

lattice绘图的一个强大特征是可以增加调节变量。如果存在一个调节变量，就可以绘制出对应每个水平的面板图。如果存在两个调节变量，就可以绘制出给定两个变量每个水平的任意组合的面板图。如果是连续量，可以先转换成离散的变量。
```R
library(lattice) 
displacement <- equal.count(mtcars$disp, number=3, overlap=0) # 把连续变量转化为三水平的shingle变量
xyplot(mpg~wt|displacement, data=mtcars, 
       main = "Miles per Gallon vs. Weight by Engine Displacement", 
       xlab = "Weight", ylab = "Miles per Gallon", layout=c(3, 1), aspect=1.5)
```

#### 面板函数
每一个高水平的画图函数都采用了默认的函数来绘制面板图。默认函数遵循命名规则`panel.graph_function`，其中`graph_function`指的是高水平的函数。

```R
library(lattice) 
displacement <- equal.count(mtcars$disp, number=3, overlap=0) 
mypanel <- function(x, y) { 
  panel.xyplot(x, y, pch=19) 
  panel.rug(x, y) 
  panel.grid(h=-1, v=-1) 
  panel.lmline(x, y, col="red", lwd=1, lty=2) 
} 
print(xyplot(mpg~wt|displacement, data=mtcars, 
       layout=c(3, 1), 
       aspect=1.5, 
       main = "Miles per Gallon vs. Weight by Engine Displacement", 
       xlab = "Weight", 
       ylab = "Miles per Gallon", 
       panel = mypanel))
```
`panel.xyplot()`函数使用一个填充的圆（pch=19）产生散点图。`panel.rug()`函数把地毯图加到x轴和y轴的每个标签上。`panel.rug(x, FALSE)`和`panel.rug(FALSE, y)`将分别把地毯加到横轴和纵轴。`panel.grid()`函数添加水平和垂直的网格线（使用负数迫使其用轴标签排队）。最后，`panel.lmline()`函数添加了被渲染成红色（col="red"）、标准厚度（lwd=2）的虚线（lty=2）回归曲线。

#### 图形参数
lattice函数使用的图形默认设置包含在一个大的列表对象中，可以通过`trellis.par.get()`函数获得并通过`trellis.par.set()`函数更改，使用`show.settings()`函数来直观地展示当前的图形设置。

#### 自定义图形条带
面板条带默认的背景是：第一个调节变量是桃红色，第二个调节变量是浅绿色，第三个调节 变量是浅蓝色。
```R
library(lattice)
histogram(~height | voice.part, data = singer, 
          strip = strip.custom(bg="lightgrey", 
                               par.strip.text=list(col="black", cex=.8, font=3)), 
          main="Distribution of Heights by Voice Pitch", 
          xlab="Height (inches)")
```

#### 页面布局
在lattice中将多个图放在一个页面使用带有split=或position=选项的plot() 函数来保存成单个图片。
```R
library(lattice) 
graph1 <- histogram(~height | voice.part, data = singer, main = "Heights of Choral Singers by Voice Part" ) 
graph2 <- bwplot(height~voice.part, data = singer) 
plot(graph1, split = c(1, 1, 1, 2)) 
plot(graph2, split = c(1, 2, 1, 2), newpage = FALSE)
```

