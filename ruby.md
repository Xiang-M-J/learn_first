## 字符串

字符串分为单引号和双引号，单引号不支持转义字符，而双引号支持

```ruby
puts '123\t123'    # 输出为 123\t123
puts "123\t123"	   # 输出为 123     123
```

字符串分割 split

```ruby
puts "123,456".split(",")[0]	# 123
```

字符串格式化 "#{xxx}"

```ruby
name1 = "Joe"
name2 = "Mary"
puts "你好 #{name1},  #{name2} 在哪?"  # 你好 Joe,  Mary 在哪?
```



## 类和变量

Ruby 中有四种变量

- **局部变量：**局部变量是在方法中定义的变量。局部变量在方法外是不可用的。在后续的章节中，您将看到有关方法的更多细节。局部变量以小写字母或 _ 开始。
- **实例变量：**实例变量可以跨任何特定的实例或对象中的方法使用。这意味着，实例变量可以从对象到对象的改变。实例变量在变量名之前放置符号（@）。
- **类变量：**类变量可以跨不同的对象使用。类变量属于类，且是类的一个属性。类变量在变量名之前放置符号（@@）。
- **全局变量：**类变量不能跨类使用。如果您想要有一个可以跨类使用的变量，您需要定义全局变量。全局变量总是以美元符号（$）开始。**未初始化的全局变量为 nil**
- **常数**：大写字母开头。

除了上述变量，还有一些伪变量

- **self:** 当前方法的接收器对象。
- **true:** 代表 true 的值。
- **false:** 代表 false 的值。
- **nil:** 代表 undefined 的值。
- `__FILE__`： 当前源文件的名称。
- `__LINE__`：当前行在源文件中的编号。



下面是类的一个例子

```ruby
class Person
  @@num = 0     # 类变量类似静态变量，所有的实例会访问同一个变量
  def initialize(id, name, addr)
    @id = id    # @id 是实例变量
    @name = name
    @addr = addr
  end
  def display
    puts "id #{@id}"
    puts "name #{@name}"
    puts "address #{@addr}"
  end
  def total_num
    @@num += 1
    puts "number: #@@num"
  end
end

p1=Person.new("1", "John", "A")
p2=Person.new("2", "Poul", "B")

p1.display
p2.display
p1.total_num    # 1
p2.total_num    # 2
```



> [!NOTE]
>
> Ruby 中类变量只能是私有的，无法直接通过 `.@xxx` 的方式访问，如何想要访问，需要创建访问器（成员函数）或者使用 `::xxx` 的方式访问
>
> ```ruby
> class Person
> 
>   def initialize(id)
>     @id = id
>   end
>   def id    # 访问器
>     @id
>   end
> end
> ```



## 运算符

除法：/

求模：%

指数：**

<=>：联合比较运算符，如果第一个操作数等于第二个操作数则返回 0，如果第一个操作数大于第二个操作数则返回 1，如果第一个操作数小于第二个操作数则返回 -1。

===：用于测试 *case* 语句的 when 子句内的相等。

.eql?：是否具有相同类型和数值，`1.eql?(1.0)` 返回false

.equal?：是否具有相同的对象 id

> 支持 +=，但不支持 ++

并行赋值：`a, b, c = 1,2,3`， `a, b = b, a`

> Ruby 支持 and 和 && 这两种逻辑与，其中 and 需要两边都为真，而 && 需要两边都不为零，类似还有 or 和 ||



三元运算符：cond ? expr1 : expr2

范围运算符：`..`（包含终点） ：`1..5` 创建一个从 1 到 5 的序列，`...`（不包含终点）：`1...5` 创建一个从 1 到 4 的序列

`defined ?`：判断变量是否已经定义，如果未定义，返回 nil

`.` 和 `::`：`.` 用来调用类和模块内的方法，而 `::` 用来引用类和模块中的常量

```ruby
MR_COUNT = 0        # 定义在主 Object 类上的常量
module Foo
  MR_COUNT = 0
  ::MR_COUNT = 1    # 设置全局计数为 1
  MR_COUNT = 2      # 设置局部计数为 2
end
puts MR_COUNT       # 这是全局常量
puts Foo::MR_COUNT  # 这是 "Foo" 的局部常量
```



## 条件

```ruby
a = 10
if a < 0
    puts "<0"
elsif a > 10
    puts ">10"
else
    puts "0-10"
end
```

还有 unless 和 case 不过多介绍



## 循环

**while**

```ruby
$i = 0
$num = 5

while $i < $num  do
    puts("在循环语句中 i = #$i" )
    $i +=1
end
```



**for i **

```ruby
for i in 0..5
    puts "局部变量的值为 #{i}"
end
```



**for each**

```ruby
(0..5).each do |i|
   puts "局部变量的值为 #{i}"
end
```



> break 中止内部循环，next 中止本次循环（类似continue），redo 无条件重新开始循环



## 函数

```ruby
def hello
    out = "hello world\n"
    puts out   # puts 打印字符
end
hello     # 函数调用

def helloa(name)    # 带参数
  puts "Hello, #{name}!"
end

helloa("tom")
```

返回还是用 return



## 模块

```ruby
# 定义在 trig.rb 文件中的模块
module Trig
   PI = 3.141592654
   def Trig.sin(x)
   # ..
   end
   def Trig.cos(x)
   # ..
   end
end
```

导入模块的语法为 `require filename`

```ruby
$LOAD_PATH << '.'
 
require 'trig.rb'   # 后缀名可以省略
 
y = Trig.sin(Trig::PI/4)
```

在类中导入模块则是 `include filename`



## 数组

**创建数组**

```ruby
names = Array.new
names = Array.new(20)  # 指定大小
puts names.length
names = Array.new(4, "mac")  # 统一赋初值
nums = Array.new(10) { |e| e = e * 2 }  # 列表迭代式 结果为 0,2,4,...,18
nums = Array[1, 2, 3, 4,5]  # 直接赋初值
digits = Array(0..9)   # 更简单的用于获取简单数字数组方式

```



**数组操作**

数组连接：arr1 + arr2

数组删除相同值：arr1 - arr2

数组添加新元素：arr << obj

索引：arr.at(index)，支持负值索引

切片：arr.slice(start, len)



## 哈希（字典）

```ruby
H = Hash["a" => 100, "b" => 200]
puts "#{H['a']}"
puts "#{H['b']}"

months = Hash.new( "month" )
months = {"1" => "January", "2" => "February"}
keys = months.keys
puts "#{keys}" # ["1", "2"]

months.to_a   # 转为二维数组（键和值）
months.to_s   # 先转二维数组，再转字符串
```



## 日期和时间

```ruby
#!/usr/bin/ruby -w
# -*- coding: UTF-8 -*-
 
time1 = Time.new
 
puts "当前时间 : " + time1.inspect
 
# Time.now 功能相同
time2 = Time.now
puts "当前时间 : " + time2.inspect
```



