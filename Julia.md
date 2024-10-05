1. 函数+!如`step!()`代表改变输入参数的值，如果是绘图函数如`plot!()`代表在同一图窗中绘图

2. `::`用于声明/标注变量类型

3. `Base.@kwdef`广播结构创建，`mutable`代表可变

4. `@gif`为宏定义，创建一个gif

5. `:`代表在维度内的所有索引，经常与索引结合

6. `args`是非关键字参数，`kw`是关键字参数；如

   ```julia
   fun(1,2,a=3,b=4)
   ```

   1和2就是非关键字参数，3和4就是关键字参数

7. plot的参数`leg`代表legend，即图例；`leg=false`代表不显示图例

8. julia中创建行向量使用下列代码

   ```julia
   a = [1 2 3]
   ```

   julia中创建列向量使用下列代码

   ```julia
   b = [1,2,3]
   ```

9. 当使用`Dash.jl`库时，推荐使用`julia code.jl`的方式来运行

10. julia读取CSV文件时，可以通过以下方式

  ```julia
  using CSV, DataFrames
  df = CSV.read(path, DataFrame) # DataFrame为指定的输出格式
  ```

11. 在使用`Dash.jl`时最好使用`127.0.0.1`本机地址作为监听地址。

12. 在`app.layout`中每一个元素后都要加上`,`,否则就会被覆盖

    ```julia
    app.layout = html_div() do
        html_h1("hello world"),	# 此处如果不加,会导致无法显示hello world
        html_div("Julia"),
    end
    ```

13. `julia Dash`不太行，不如`python`中的Dash

14. 当遇到一些不太了解的函数时，可以通过在`julia`环境中键入`?`，再输入待查询的函数名即可

15. julia中查询特殊字符如何输入，使用`?特殊变量`，如查询ŷ，在julia的环境下输入`?ŷ`

16. 在julia环境下，按`]`进入包管理
