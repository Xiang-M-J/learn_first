
基于 Java 虚拟机的一种语言，可以使用 Intellj community 版本作为编辑器，需要额外安装 Scala 插件（专业版和社区版都需要装）


# 基本知识
## 变量

使用 val 定义不可变变量，var 定义可变变量

```scala
val a = 10
var b = 10
// a = 9   // 此处会报错
b = 9   // 不会报错
```

scala 支持自动推断类型，但是可以指定类型，有两种方式

```scala
val b:Int = 10  
val c:Float = 10.0  
val d:String = "123"

val x = 1_000L // val x: Long = 1000 
val y = 2.2D // val y: Double = 2.2 
val z = 3.3F  // val z: Float = 3.3
```



## 字符串

### 字符串插值

使用 s"${}" 来插值

```scala
val firstName = "John"
val mi = 'C'
val lastName = "Doe"

println(s"Name: $firstName $mi $lastName")   // "Name: John C Doe"
println(s"2 + 2 = ${2 + 2}") // prints "2 + 2 = 4"
```

使用 f"${}" 来格式化插值

```scala
val height = 1.9d
val name = "James"
println(f"$name%s is $height%2.2f meters tall")  // "James is 1.90 meters tall"
```

> [!NOTE]
>
> 如果想要在 f"" 中显示 %，需要重复使用 %，如 `println(f"3/19 is less than 20%%")`

使用 raw 获得原始字符串

```scala
raw"a\nb"   // 等于 a\nb
```

使用字符串生成对象

```scala
extension (sc: StringContext)
  def p(args: Double*): Point = {
    // reuse the `s`-interpolator and then split on ','
    val pts = sc.s(args: _*).split(",", 2).map { _.toDoubleOption.getOrElse(0.0) }
    Point(pts(0), pts(1))
  }

val x=12.0

p"1, -2"        // Point(1.0, -2.0)
p"${x/5}, $x"   // Point(2.4, 12.0)
```



### 多行字符串

```scala
val quote = """The essence of Scala:
               Fusion of functional and object-oriented
               programming in a typed setting."""
```





## 控制和循环

### if / else

```scala
if x < 0 then
  println("negative")
else if x == 0 then
  println("zero")
else
  println("positive")
```

> [!NOTE]
>
> 上面的写法为 Scala3，Scala2 的写法与 C 中的基本相同



### 三元表达式

```scala
val x = if a < b then a else b
```



### for

```scala
val ints = List(1, 2, 3, 4, 5)

for i <- ints do println(i)
```

这里的 `i <- ints` 可以看出是一个生成器，带条件的 for 语句如下

```scala
for
  i <- ints
  if i > 2
do
  println(i)
```

许多情况下，需要迭代一个区间，使用 `a to b` 来生成一个 [a, b] 的范围列表

```scala
for
  i <- 1 to 3
  j <- 'a' to 'c'
  if i == 2
  if j == 'b'
do
  println(s"i = $i, j = $j")   // prints: "i = 2, j = b"
```



除了使用 do，还可以使用 yield 来返回数据

```scala
val doubles = for i <- 1 to 4 yield i * 2
println(doubles)    // Vector(2,4,6,8)
```



遍历字典

```scala
val states = Map(
  "AK" -> "Alaska",
  "AL" -> "Alabama", 
  "AR" -> "Arizona"
)
for (abbrev, fullName) <- states do println(s"$abbrev: $fullName")
```



### match

类似 switch

```scala
val result = i match
case 1 => "one"
case 2 => "two"
case _ => "other"
```



### while

```scala
var x = 1

while
x < 3
do
println(x)
x += 1
```



### try/catch/finally

捕捉错误

```scala
try
writeTextToFile(text)
catch
case ioe: IOException => println("Got an IOException.")
case nfe: NumberFormatException => println("Got a NumberFormatException.")
finally
println("Clean up your resources here.")
```



## 集合

### 列表

可以使用 List 直接创建，还可以使用 a to b by c 的语法创建，索引使用 ()

```scala
val a = List(1, 2, 3)           // a: List[Int] = List(1, 2, 3)
print(a(1))
// Range methods
val b = (1 to 5).toList         // b: List[Int] = List(1, 2, 3, 4, 5)
val c = (1 to 10 by 2).toList   // c: List[Int] = List(1, 3, 5, 7, 9)
val e = (1 until 5).toList      // e: List[Int] = List(1, 2, 3, 4)
val f = List.range(1, 5)        // f: List[Int] = List(1, 2, 3, 4)
val g = List.range(1, 10, 3)    // g: List[Int] = List(1, 4, 7)
```



列表有许多内置方法

```scala
// a sample list
val a = List(10, 20, 30, 40, 10)      // List(10, 20, 30, 40, 10)

a.drop(2)                             // List(30, 40, 10)
a.dropWhile(_ < 25)                   // List(30, 40, 10)
a.filter(_ < 25)                      // List(10, 20, 10)
a.slice(2,4)                          // List(30, 40)
a.tail                                // List(20, 30, 40, 10)
a.take(3)                             // List(10, 20, 30)
a.takeWhile(_ < 30)                   // List(10, 20)

// flatten
val a = List(List(1,2), List(3,4))
a.flatten                             // List(1, 2, 3, 4)

// map, flatMap
val nums = List("one", "two")
nums.map(_.toUpperCase)               // List("ONE", "TWO")
nums.flatMap(_.toUpperCase)           // List('O', 'N', 'E', 'T', 'W', 'O')
```



### 元组

使用括号创建

```scala
val t = (11, "eleven", Person("Eleven"))
print(t(0))
```





## 面向对象编程



### Traits

可以当成简单的 interface，但是类似 class 包含抽象和具体的方法和对象，也有参数。提供了一种将操作组织成小的单元

```scala
trait Speaker:
  def speak(): String  // has no body, so it’s abstract

trait TailWagger:
  def startTail(): Unit = println("tail is wagging")
  def stopTail(): Unit = println("tail is stopped")

trait Runner:
  def startRunning(): Unit = println("I’m running")
  def stopRunning(): Unit = println("Stopped running")

val d = Dog("Rover")
println(d.speak())      // prints "Woof!"

val c = Cat("Morris")
println(c.speak())      // "Meow"
c.startRunning()        // "Yeah ... I don’t run"
c.stopRunning()         // "No need to stop"
```



### Class

```scala
class Person(var firstName: String, var lastName: String):
  def printFullName() = println(s"$firstName $lastName")

val p = Person("John", "Stephens")
println(p.firstName)   // "John"
p.lastName = "Legend"
p.printFullName()      // "John Legend"
```





## 函数编程

### 枚举

```scala
enum CrustSize:
  case Small, Medium, Large

enum CrustType:
  case Thin, Thick, Regular

enum Topping:
  case Cheese, Pepperoni, BlackOlives, GreenOlives, Onions
```



### Product Types

代数数据类型，通过 case 声明

```scala
// define a case class
case class Person(
  name: String,
  vocation: String
)

// create an instance of the case class
val p = Person("Reginald Kenneth Dwight", "Singer")

// a good default toString method
p                // : Person = Person(Reginald Kenneth Dwight,Singer)

// can access its fields, which are immutable
p.name           // "Reginald Kenneth Dwight"
p.name = "Joe"   // error: can’t reassign a val field

// when you need to make a change, use the `copy` method
// to “update as you copy”
val p2 = p.copy(name = "Elton John")
p2    
```



## 函数



### 基本函数

一个完整的定义如下

```scala
def methodName(param1: Type1, param2: Type2): ReturnType =
  // the method body
  // goes here
```

> [!NOTE]
>
> 返回类型不是必需的

下面是一些示例

```scala
def getStackTraceAsString(t: Throwable): String =
  val sw = new StringWriter
  t.printStackTrace(new PrintWriter(sw))
  sw.toString
```

带有默认值的函数

```scala
def makeConnection(url: String, timeout: Int = 5000): Unit =
  println(s"url=$url, timeout=$timeout")
```

如果想要返回多个值，可以用括号包起来

```scala
def getFullName(firstName: String, lastName: String): (String, String) = {
  val fullName = firstName + " " + lastName
  val initials = firstName.charAt(0) + "." + lastName.charAt(0) + "."

  (fullName, initials)
}

val fullname, initial = getFullName("John", "Doe")
```



还可以为某个类型添加函数

```scala
extension (s: String)
  def makeInt(radix: Int): Int = Integer.parseInt(s, radix)
```



### 匿名函数

使用箭头符号定义匿名函数

```scala
var inc = (x:Int) => x + 1
```



```scala
val a = List(1, 2, 3).map(i => double(i))   // List(2,4,6)

val x = nums.filter(_ > 3)
            .filter(_ < 7)
            .map(_ * 10)
```



## 单例对象

### “工具箱”方法

使用 object 创建一个单例对象

```scala
object StringUtils:
  def isNullOrEmpty(s: String): Boolean = s == null || s.trim.isEmpty
  def leftTrim(s: String): String = s.replaceAll("^\\s+", "")
  def rightTrim(s: String): String = s.replaceAll("\\s+$", "")
```

单例对象中的方法可以类似静态方法访问

```scala
val x = StringUtils.isNullOrEmpty("")    // true
```



### 伴生对象

一个伴生类或者伴生对象可以访问被伴生对象的私有成员

```scala
import scala.math.*

class Circle(radius: Double):
  import Circle.*
  def area: Double = calculateArea(radius)

object Circle:
  private def calculateArea(radius: Double): Double =
    Pi * pow(radius, 2.0)

val circle1 = Circle(5.0)
circle1.area   // Double = 78.53981633974483
```

