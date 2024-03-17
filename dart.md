创建 Dart 项目：

```sh
dart create test
```

运行项目：

```sh
dart run
```

执行 Dart 代码：

```sh
dart src.dart
```

Dart 中存在入口函数

```dart
void main() {   // void 可以省略
  print('Hello, World!');
}
```



## 基础表达式

### 变量

变量定义无需显式说明，可以使用 `var` 来定义变量。

```dart
var name = 'Voyager I'; 
String name_ = 'Voyager I';  // 显式说明
var year = 1977;
```

#### final 和 const

`final` 和 `const` 都能用来定义常量

`final`：运行时常量，值在程序运行时才能确定。

`const`：编译时常量，值在编译时就能确定的常量，不是等到运行时才确定。

如下面这两句分别定义了一个运行时常量和编译时常量

```dart
const test3=DateTime.now();	//编译报错,值不是编译期常量
final test4=DateTime.now();	//正确，运行时常量
```

如果 `const` 变量位于类级别，需要标记为 `static const`（静态常量）。



#### 空安全

空安全能够防止意外访问 `null` 的变量而导致的错误。

空安全引入了三个关键更改：

1. 当你为变量、参数或另一个相关组件指定类型时，可以控制该类型是否允许 `null` 。要让一个变量可以为空，你可以在类型声明的末尾添加 `?` 。

    ```dart
    String? name  // Nullable type. Can be `null` or string.
    String name   // Non-nullable type. Cannot be `null` but can be string.
    ```

2. 必须在使用变量之前对其进行初始化。可空变量是默认初始化为 `null` 的。 Dart 不会为非可空类型设置初始值，强制要求设置初始值。 

3. 不能访问可为空类型的表达式的属性或调用方法。同样的异常也适用于 `null` 支持的属性或方法，如 `hashCode` 或 `toString()`。

通过断言判断是否变量为 `null`：

```dart
int? lineCount;
assert(lineCount == null);
```

> 断言只会在开发时起到作用

#### 延迟初始化

顶级变量（与入口函数同等级的变量）和类变量是延迟初始化的，它们会在第一次被使用时再初始化。

```dart
class A{
  A(String str){
    print(str);
  }
}
class B{
    A a = A("3"); // 类变量延迟初始化，不会输出 3
}

A a1 = A("1");    // 顶级变量延迟初始化，不会输出1
void main(){
  A a2 = A("2");  // 正常输出 2
}
```

通常 Dart 的语义分析可以检测非空变量在使用之前是否被赋值，但有时会分析失败。常见的两种情况是在分析顶级变量和实例变量时，Dart 通常无法确定它们是否已设值，因此不会尝试分析。如果确定变量在使用之前已设置，但 Dart 推断错误的话，可以将变量标记为 `late` 来解决这个问题：

```dart
late String description;	// 不加 late 会导致 Dart 推断错误

void main() {
  description = 'Feijoada!';
  print(description);
}
```

当一个 `late` 修饰的变量在声明时就指定了初始化方法，那么内容会在第一次使用变量时运行初始化。这种延迟初始化在以下情况很方便：

- （Dart 推断）可能不需要该变量，并且初始化它的开销很高。
- 正在初始化一个实例变量，它的初始化方法需要调用 `this`。

### 操作符

```dart
c = a>b ? a : b;    // 三元操作符
a != b;			   // 逻辑不等
2/4;		       // 除法
7%4;                // 取余
7~/4;			   // 整除
a is int;		   // 类型测试
a is! int;		   // a 不是 int 类型时为真
a as int;		   // 类型转换
expr1 ?? expr2;	   // 判空操作符，expr1 为空则选择 expr2，类似于shell中的或操作符
a ??= b;		  // 如果 b 为空，则 a 不变。
```

级联操作符

```dart
var paint = Paint()
  ..color = Colors.black
  ..strokeCap = StrokeCap.round
  ..strokeWidth = 5.0;
// 上面这段代码等同于下面这段代码
var paint = Paint();
paint.color = Colors.black;
paint.strokeCap = StrokeCap.round;
paint.strokeWidth = 5.0;
```

如果对象可能为空，则可以在第一个级联操作符之前加上 `?`，这样如果对象为空的话，后续的级联操作都不会进行，如下所示：

```dart
var paint = Paint()
  ?..color = Colors.bla
  ..strokeCap = Stroke
  ..strokeWidth = 5.0;
```

逻辑操作符

| Operator | Meaning                                               |
| -------- | ----------------------------------------------------- |
| `&`      | AND                                                   |
| `|`      | OR                                                    |
| `^`      | XOR                                                   |
| `~expr`  | Unary bitwise complement (0s become 1s; 1s become 0s) |
| `<<`     | Shift left                                            |
| `>>`     | Shift right                                           |
| `>>>`    | Unsigned shift right                                  |

在一个操作符前面加上 `?`，表示操作符针对的对象可以为 null，此时返回的值也为 null，如 `?[]`、`?.`

### 导入

```dart
// Importing core libraries
import 'dart:math';

// Importing libraries from external packages
import 'package:test/test.dart';

// Importing files
import 'path/to/my_other_file.dart';

// 指定库的前缀
import 'package:lib2/lib2.dart' as lib2;
lib2.Element element2 = lib2.Element();

// Import only foo.
import 'package:lib1/lib1.dart' show foo;

// Import all names EXCEPT foo.
import 'package:lib2/lib2.dart' hide foo;

```



## 类型

### 基础类型

- [Numbers](https://dart.cn/language/built-in-types#numbers) (`int`, `double`)
- [Strings](https://dart.cn/language/built-in-types#strings) (`String`)
- [Booleans](https://dart.cn/language/built-in-types#booleans) (`bool`)
- [Records](https://dart.cn/language/records) (`(value1, value2)`)
- [Lists](https://dart.cn/language/collections#lists) (`List`, also known as *arrays*)
- [Sets](https://dart.cn/language/collections#sets) (`Set`)
- [Maps](https://dart.cn/language/collections#maps) (`Map`)
- [Runes](https://dart.cn/language/built-in-types#runes-and-grapheme-clusters) (`Runes`; often replaced by the `characters` API)
- [Symbols](https://dart.cn/language/built-in-types#symbols) (`Symbol`)
- The value `null` (`Null`)

#### 其它类型 与 String 的互转

```dart
// String -> int
int one = int.parse('1');

// String -> double
double onePointOne = double.parse('1.1');

// int -> String
String oneAsString = 1.toString();

// double -> String
String piAsString = 3.14159.toStringAsFixed(2);

// List -> String
List<int> a = [1,2,3];
print(a.join(" "));
```

#### 字符串的操作

```dart
void main() {
  String str = "Hello" + " World";  // 字符串拼接
  print(str.toLowerCase());         // 转小写
  print(str[0]);                    // 字符串索引
  print(str.split(" "));            // 分割
  print(''' Hello
  World
''');                               // 多行字符串
  print(r"Hello \n World");         // 创建原始字符串，主要用于路径和正则表达式
  print(str.substring(2,5));        // 切片
  print(str.length);                // 长度
  print("str: $str");               // 字符串格式化
}
```



#### Runes 和 grapheme clusters

一些特殊字符

```dart
import 'package:characters/characters.dart';

void main() {
  var hi = 'Hi 🇩🇰';
  print(hi);
  print('The end of the string: ${hi.substring(hi.length - 1)}');
  print('The last character: ${hi.characters.last}');
}
```

需要先安装对应的库

```sh
dart pub add characters
```



### 记录（Records）

是一个集合，可以包括许多不同类型的元素，不可变，用括号定义，可以作为函数的返回值来一次返回多个值：

```dart
(int, int) swap((int, int) record) {
  var (a, b) = record;
  return (b, a);
}
```

带类型说明的定义：

```dart
(String, int) record;
record = ("A string", 123);
print(record.$1);		// 访问第一个元素
print(record.$2);	
```

带类型注释的定义：

```dart
({int a, bool b}) record;
record = (a: 123, b: true);
print(record.a);
print(record.b);
```



### 集合（Collections）



#### List

用 `[]` 来定义

```dart
List<int> list = List<int>.generate(10, (index) => index);  // 列表生成式
print(list.length);
print(list.first);
print(list.last);
print(list[2]);
print(list.sublist(2, 5));
list.add(10);       
list.remove(3);     // 指定值删除（第一次出现）
Iterable<int> list_r = list.reversed; // 反转
list.removeLast();
var constantList = const [1, 2, 3];   // const 使列表为常量，不可变（不可添加，删除，修改等）

```



#### Sets

用 `{}` 来定义，无序且不重复

```dart
Set<int> set = {1,2,3,4};
print(set.length);
print(set.first);
print(set.last);
set.add(5);       
set.remove(3);     // 指定值删除
```



#### Maps

字典，`{key: value}`

```dart
var gifts = Map<String, String>();
gifts['first'] = 'partridge';
gifts['second'] = 'turtledoves';
gifts['fifth'] = 'golden rings';
```



#### 操作符

展开语法 `...`

```dart
var list = [1, 2, 3];
var list2 = [0, ...list];
print(list2);		// 1 2 3 4
```

`...?` 如果右边为 null，则不展开，结合上面的例子，如果 list 为 null，那么 list2 为 0。



控制操作符

```dart
var nav = ['Home', 'Furniture', 'Plants', if (promoActive) 'Outlet'];

// if (a case b) 语法，如果 b 是 a 的实例，a 为类型
var nav = ['Home', 'Furniture', 'Plants', if (login case 'Manager') 'Inventory'];

var listOfStrings = ['#0', for (var i in listOfInts) '#$i'];
```



### 泛型（Generics）

泛型可以减少重复代码，下面是一个泛型的例子：

```dart
class A<T>{
  void output(T value){
    print(value);
  }
}
void main() {
  A a = A<String>();
  a.output("Hello");
  // a.output(12);    // 这句会报错
}
```



### 别名（Typedefs）

```dart
typedef IntList = List<int>;
IntList il = [1, 2, 3];
```



## 模式匹配

switch 语句

```dart
void main() {
  const a = 'a';
  const b = 'b';
  var obj = [a, b];
  switch (obj) {
    // List pattern [a, b] matches obj first if obj is a list with two fields,
    // then if its fields match the constant subpatterns 'a' and 'b'.
    case [a, b]:
      print('$a, $b');
  }
}
```

解构

```dart
var numList = [1, 2, 3];
var [a, b, c] = numList;  // a = 1, b = 2, c = 3

switch (list) {
  case ['a' || 'b', var c]:		// 解构两元素列表，匹配第一个元素为 a 或 b，输出第二个元素
    print(c);
}
var (a, [b, c]) = ('str', [1, 2]);
(a, b) = (b, a);	// 交换两个元素
```



### 模式类型

逻辑或模式

```dart
var isPrimary = switch (color) {
  Color.red || Color.yellow || Color.blue => true,
  _ => false
};
```

逻辑与模式，定义的变量不能重复

```dart
switch ((1, 2)) {
  // Error, both subpatterns attempt to bind 'b'.
  case (var a, var b) && (var b, var c): // ...
}
```

关系模式

```dart
String asciiCharType(int char) {
  const space = 32;
  const zero = 48;
  const nine = 57;

  return switch (char) {
    < space => 'control',
    == space => 'space',
    > space && < zero => 'punctuation',
    >= zero && <= nine => 'digit',
    _ => ''
  };
}
```



### 函数

普通函数

```dart
int fibonacci(int n) {
  if (n == 0 || n == 1) return n;
  return fibonacci(n - 1) + fibonacci(n - 2);
}

var result = fibonacci(20);
```

如果函数只包含一个表达式，可以使用短语法：

```dart
bool isNoble(int atomicNumber) => _nobleGases[atomicNumber] != null;
```



对于函数参数，如果没有给定默认值，或者未表明该参数是 `required`，则参数类型必须可以为 null，且默认值为 null：

```dart
void enableFlags({bool? bold, bool? hidden}) {...}
```

调用函数传参时：

```dart
enableFlags(bold: true, hidden: false);
```



表明某个参数是必须的：

```dart
const Scrollbar({super.key, required Widget child});
```



### 匿名函数



匿名函数用于将函数作为参数传递的场合：

```dart
void main() {
  List<int> list = List<int>.generate(10, (index) => index); // 从 0 开始
  Iterable<int> list_bigger_than_5 = list.where((element) => element>5); // 匿名函数
  for (int li in list_bigger_than_5) {
    print(li);
  }
}
```

上面这种写法只支持单条语句，对于多条语句的写法：

```dart
void main() {
  List<int> list = List<int>.generate(10, (index) => index); // 从 0 开始
  Iterable<int> list_bigger_than_5 = list.where(
      (element){ 
          return element>5;
      }
  ); // 匿名函数
  for (int li in list_bigger_than_5) {
    print(li);
  }
}
```



### 生成器

同步生成器

```dart
Iterable<int> naturalsTo(int n) sync* {
  int k = 0;
  while (k < n) yield k++;
}
```

异步生成器

```dart
Stream<int> asynchronousNaturalsTo(int n) async* {
  int k = 0;
  while (k < n) yield k++;
}
```

递归生成器

```dart
Iterable<int> naturalsDownFrom(int n) sync* {
  if (n > 0) {
    yield n;
    yield* naturalsDownFrom(n - 1);
  }
}
```



## 流程控制

### 循环

```dart
for (final object in flybyObjects) {
  print(object);
}

for (int month = 1; month <= 12; month++) {
  print(month);
}

while (!isDone()) {
  doSomething();
}

do {
  printLine();
} while (!atEndOfPage());
```





### 判断

```dart
if (year >= 2001) {
  print('21st century');
} else if (year >= 1901) {
  print('20th century');
}

if (pair case [int x, int y]) return Point(x, y);   // if case 判断值是否匹配类型

var command = 'OPEN';
switch (command) {
  case 'CLOSED':
    executeClosed();
  case 'PENDING':
    executePending();
  case 'APPROVED':
    executeApproved();
  case 'DENIED':
    executeDenied();
  case 'OPEN':
    executeOpen();
  default:
    executeUnknown();
}

// 在使用 switch 语句时，可以使用 when 和 if case 作为保卫子句
switch (something) {
  case somePattern when some || boolean || expression:
    //             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ Guard clause.
    body;
}
switch (10) {
    case (var a) when a > 9 && a<11:
      print(a);
}

// Switch expression:
var value = switch (something) {
  somePattern when some || boolean || expression => body,
  //               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ Guard clause.
}
// If-case statement:
if (something case somePattern when some || boolean || expression) {
  //                           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ Guard clause.
  body;
}

```



## 错误处理

```dart
try {
  breedMoreLlamas();
} on OutOfLlamasException {
  // A specific exception
  buyMoreLlamas();
} on Exception catch (e) {
  // Anything else that is an exception
  print('Unknown exception: $e');
} catch (e) {
  // No specified type, handles all
  print('Something really unknown: $e');
}finally {
  // Always clean up, even if an exception is thrown.
  cleanLlamaStalls();
}
```



## 类和对象

Dart 是一种面向对象的语言，具有类和基于 mix 的继承。



```dart
class Spacecraft {
  String name;
  DateTime? launchDate;		// ? 表示

  // 只读属性
  int? get launchYear => launchDate?.year;

  // 构造函数的语法糖，等价于直接赋值
  Spacecraft(this.name, this.launchDate) {
  }

  // 命名构造函数（也是构造函数，不过使构造函数意义更加丰富），此处调用了默认的构造函数
  Spacecraft.unlaunched(String name) : this(name, null);
  
  // 除了调用默认构造函数，还可以在构造函数体运行之前初始化实例变量。
  Spacecraft.create(String name, DateTime? cDate) : name=name, launchDate=cDate;

  // Method.
  void describe() {
    print('Spacecraft: $name');
    // Type promotion doesn't work on getters.
    var launchDate = this.launchDate;
    if (launchDate != null) {
      int years = DateTime.now().difference(launchDate).inDays ~/ 365;
      print('Launched: $launchYear ($years years ago)');
    } else {
      print('Unlaunched');
    }
  }
}

void main(){
  var voyager = Spacecraft("Voyager Ⅰ", DateTime(1977, 9, 5));
  voyager.describe();

  var voyager3 = Spacecraft.unlaunched('Voyager III');
  voyager3.describe();
}
```

`super` 关键字访问父类，`this` 访问自身。



### 成员方法

#### 实例方法

```dart
import 'dart:math';

class Point {
  final double x;
  final double y;

  Point(this.x, this.y);

  double distanceTo(Point other) {   // distanceTo是一个实例方法，可以访问实例变量 x 和 y
    var dx = x - other.x;
    var dy = y - other.y;
    return sqrt(dx * dx + dy * dy);
  }
}
```





#### 重载运算符

```dart
class Vector {
  final int x, y;

  Vector(this.x, this.y);

  Vector operator +(Vector v) => Vector(x + v.x, y + v.y);
  Vector operator -(Vector v) => Vector(x - v.x, y - v.y);

  @override
  bool operator ==(Object other) =>
      other is Vector && x == other.x && y == other.y;

  @override
  int get hashCode => Object.hash(x, y);   // 重载 hashCode 属性

  @override
  String toString(){					 // 重载 toString 方法
    return "x: $x, y: $y";
  }
}

void main(){
  Vector v1 = Vector(1, 3);
  Vector v2 = Vector(2, 4);
  print(v1 + v2);
}
```



#### Setters 和 Getters

```dart
class Rectangle {
  double left, top, width, height;
  Rectangle(this.left, this.top, this.width, this.height);

  // Define two calculated properties: right and bottom.
  double get right => left + width;
  set right(double value) => left = value - width;
  double get bottom => top + height;
  set bottom(double value) => top = value - height;
}

void main() {
  var rect = Rectangle(3, 4, 20, 15);
  assert(rect.left == 3);	// get
  rect.right = 12;			// set
  assert(rect.left == -8);
}
```



### 继承

使用 `extends` 创建子类，使用 `super` 访问父类

```dart
class Television {
  void turnOn() {
    _illuminateDisplay();
    _activateIrSensor();
  }
  // ···
}

class SmartTelevision extends Television {
  void turnOn() {
    super.turnOn();
    _bootNetworkInterface();
    _initializeMemory();
    _upgradeApps();
  }
  // ···
}
```



### 枚举

枚举的定义

```dart
enum Color { red, green, blue }
```

枚举的使用

```dart
final favoriteColor = Color.blue;
if (favoriteColor == Color.blue) {
  print('Your favorite color is blue!');
}
```

枚举的索引

```dart
assert(Color.red.index == 0);
assert(Color.green.index == 1);
assert(Color.blue.index == 2);

List<Color> colors = Color.values;
assert(colors[2] == Color.blue);
```



### 扩展方法

扩展方法的语法为：

```dart
extension <extension name>? on <type> {
  (<member definition>)*
}
```

下面是一个例子：

```dart
extension NumberParsing on String {
  int parseInt() {
    return int.parse(this);
  }

  double parseDouble() {
    return double.parse(this);
  }
}
void main() {
  print("12".parseInt());			// 使用了扩展方法
  print("12.1".parseDouble());
}
```

实现泛型扩展

```dart
extension MyFancyList<T> on List<T> {
  int get doubleLength => length * 2;
  List<T> operator -() => reversed.toList();
  List<List<T>> split(int at) => [sublist(0, at), sublist(at)];
}
```



## 并发

### 异步

使用 `async` 和 `await` 来实现异步

```dart
Future<void> checkVersion() async {
  var version = await lookUpVersion();
  // Do something with version
}
```

下面是一个文件读取的例子

```dart
const String filename = 'with_keys.json';

void main() async {

  final fileData = await _readFileAsync();
  final jsonData = jsonDecode(fileData);

  print('Number of JSON keys: ${jsonData.length}');
}

Future<String> _readFileAsync() async {
  final file = File(filename);
  final contents = await file.readAsString();
  return contents.trim();
}
```

使用异步方法可以让文件 I/O 操作时，其它代码（如事件处理等）也能继续执行。



Dart 代码并不在多个线程上运行，取而代之的是它们会在 isolate 内运行。每一个 isolate 会有自己的堆内存，从而确保 isolate 之间互相隔离，无法互相访问状态。由于这样的实现并不会共享状态，所以互斥锁和其他锁以及竞争条件不会在 Dart 中出现。也就是说，isolate 并不能完全防止竞争条件。

在使用 isolate 时，你的 Dart 代码可以在同一时刻进行多个独立的任务，并且使用可用的处理器核心。 Isolate 与线程和进程近似，但是每个 isolate 都拥有独立的内存，以及运行事件循环的独立线程。

```dart
const String filename = 'with_keys.json';
Future<Map<String, dynamic>> _readAndParseJson() async {
  final fileData = await File(filename).readAsString();
  final jsonData = jsonDecode(fileData) as Map<String, dynamic>;
  return jsonData;
}

void main() async {
  // Read some data.
  final jsonData = await Isolate.run(_readAndParseJson);

  // Use that data.
  print('Number of JSON keys: ${jsonData.length}');
}
```



## 文件I/O

### 文件读入

```dart
import 'dart:io';

void main() async {
  var file = File("test.txt");		// File 来自 dart:io 包
  var content1 = await file.readAsString(); // 读入字符串
  var content2 = await file.readAsBytes();  // 读入字节
  var content3 = await file.readAsLines();  // 按行读取

  print(content1);
  print(content2);
  print(content3);
}
```

如果遇到大文件，可以使用流方式读入

```dart
import 'dart:io';
import 'dart:convert';

Future<void> main() async {
  var file = File('file.txt');
  Stream<List<int>> inputStream = file.openRead();

  var lines = utf8.decoder
      .bind(inputStream)
      .transform(const LineSplitter());
  try {
    await for (final line in lines) {
      print('Got ${line.length} characters from stream');
    }
    print('file is now closed');
  } catch (e) {
    print(e);
  }
}
```

### 文件写入

与文件读取类似，可以以字符串形式写入，或者以比特流形式写入，写入操作还可以指定模式：

```dart
import 'dart:io';

void main() async {
  var file = File("test.txt");
  file.writeAsString("Hello World", mode: FileMode.append);
  file.writeAsBytes([111,112,113,114,115], mode: FileMode.append);  // 这段程序会覆盖上一段程序写入的数据。
}
```

以流的方式写入

```dart
var logFile = File('log.txt');
var sink = logFile.openWrite(mode: FileMode.append);
sink.write('FILE ACCESSED ${DateTime.now()}\n');
await sink.flush();
await sink.close();
```

