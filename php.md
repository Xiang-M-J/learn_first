# PHP

## 基础环境的搭建

>一种简单的方法：下载vscode插件PHP-Server来运行php文件

**参考教程**：https://www.cnblogs.com/wwjchina/p/9804576.html

### 配置php

进入php文件夹，找到`php.ini-development`，复制重命名为`php.ini`。

搜索`extension_dir`找到配置项，把该配置项设置成php目录下ext的绝对路径（最好是绝对路径，也可以是相对路径"./ext"，这一步不确定是否必要）

```ini
; On windows:
extension_dir = "ext"
```

搜索`cgi.fix_pathinfo`找到配置项，取消注释并将其设置为1。

```ini
; https://php.net/cgi.fix-pathinfo
cgi.fix_pathinfo=1
```

`cgi.fix_pathinfo`是用来设置在cgi模式下PHP是否提供PATH_INFO信息。因为nginx默认不会设置PATH_INFO的值，所以需要通过上面的方法来提供。

### 配置nginx

打开nginx文件夹，修改`conf/nginx.conf`配置文件为（已删除默认注释的配置）

```nginx
worker_processes  1;
events {
    worker_connections  1024;
}
http {
    include       mime.types;
    default_type  application/octet-stream;
    sendfile        on;
    keepalive_timeout  65;
    server {
        listen       80;		# 默认端口为80
        server_name  localhost;  # 默认地址为127.0.0.1
        location / {
            root   D:\postgraduateLearn\first\programming\php;	
            # 网站根目录（存放php文件的文件夹）
            index  index.html;
        }
        error_page   500 502 503 504  /50x.html;
        location = /50x.html {
            root   html;
        }
        location ~ \.php$ {
            root           D:\postgraduateLearn\first\programming\php;
            fastcgi_pass   127.0.0.1:9000;	# 默认端口为9000
            fastcgi_index  index.php;
            # 此处将/script$fastcgi_script_name修改为$document_root$fastcgi_script_name
            # $document_root就是上面的root
            fastcgi_param  SCRIPT_FILENAME  $document_root$fastcgi_script_name;
            include        fastcgi_params;
        }
    }
}
```

### 开启php-cgi和nginx

1. 打开nginx
2. **打开php-cgi**（`-b`指定地址和端口（需要和上面设置的端口对应）`-c`指定配置文件），php-cgi需要一直运行，否则访问php文件时只会下载不会解析。

```cmd
D:\php-8.3.0\php-cgi.exe -b 127.0.0.1:9000 -c D:\php-8.3.0\php.ini
```

在`D:\postgraduateLearn\first\programming\php`文件夹创建`phpinfo.php`为

```php
<?php 
	phpinfo();
```

在浏览器打开`127.0.0.1/phpinfo.php`，即可看到下面的页面

<img src="D:\TyporaImages\image-20231207210141978.png" alt="image-20231207210141978" style="zoom:67%;" />

> 如果端口号对上了，但是浏览器访问php文件，只下载并没有解析，可以尝试重启电脑，注意重启ngnix并没有用。

### 自动化操作

```cmd
@echo off
tasklist|findstr /i "nginx.exe">nul &&taskkill /F /IM nginx.exe
echo start nginx...
set path=%cd%
cd /D D:/nginx-1.24.0
start nginx
set php_conf=D:/php-8.3.0/php.ini
cd %path%
echo start php-cgi.exe port:127.0.0.1:9000 conf path: %php_conf%
D:\php-8.3.0\php-cgi.exe -b 127.0.0.1:9000 -c%php_conf%
```


### debug

下载Xdebug，直接按照提示一步一步来就行了，[Xdebug: Support — Tailored Installation Instructions](https://xdebug.org/wizard)


## PHP语言学习

### 基础语法

#### PHP标记

当解析一个文件时，PHP会寻找起始和结束标记，即`<?php`和`?>`，这告诉PHP开始和停止解析二者之间的代码。此种解析方式使得 PHP可以被嵌入到各种不同的文档中去，而任何起始和结束标记之外的部分都会被 PHP 解析器忽略。

PHP有一个echo标记简写为`<?=`，它是更完整的 `<?php echo` 的简写形式。

**示例 PHP 开始和结束标记**

```php
1.  <?php echo 'if you want to serve PHP code in XHTML or XML documents,  use these tags'; ?>
2.  You can use the short echo tag to <?= 'print this string' ?>.    
    It's equivalent to <?php echo 'print this string' ?>.
3.  <? echo 'this code is within short tags, but will only work '.  'if short_open_tag is enabled'; ?>
```

短标记（第三个例子）是被默认开启的，但是可以通过`pip.ini`中的short_open_tag来直接禁用。如果 PHP 在被安装时使用了 **--disable-short-tags** 的配置，该功能则是被默认禁用的。

> **注意**:
>
> 因为短标记可以被禁用，所以建议使用普通标记 (`<?php ?>` 和 `<?= ?>`) 来最大化兼容性。

如果文件内容仅仅包含PHP代码，最好在文件末尾**删除PHP结束标记**。这可以避免在PHP结束标记之后万一意外加入了空格或者换行符，会导致 PHP 开始输出这些空白，而脚本中此时并无输出的意图。

```php
<?php
    echo "hello world";
	// more
	echo "last";
// 无结束标记防止输出空白
```

#### 从HTML中分离

凡是在一对开始和结束标记之外的内容都会被 PHP 解析器忽略，这使得 PHP 文件可以具备混合内容。 可以使 PHP 嵌入到 HTML 文档中去，如下例所示。

```php+HTML
<p>This is going to be ignored by PHP and displayed by the browser.</p>
<?php echo 'While this is going to be parsed.'; ?>
<p>This will also be ignored by PHP and displayed by the browser.</p>
```

这将如预期中的运行，因为当 PHP 解释器碰到`?>`结束标记时就简单地将其后内容原样输出（除非马上紧接换行-见[指令分隔符](https://www.php.net/manual/zh/language.basic-syntax.instruction-separation.php)）直到碰到下一个开始标记；例外是处于条件语句中间时，此时 PHP 解释器会根据条件判断来决定哪些输出，哪些跳过。见下例。

**示例：使用条件的高级分离**

```php
<?php if ($expression == true): ?>
  This will show if the expression is true.
<?php else: ?>
  Otherwise this will show.
<?php endif; ?>
```

#### 指令分隔符

PHP需要在每个语句后用分号结束指令。一段PHP代码中的结束标记隐含表示了一个分号；在一个PHP代码段中的最后一行可以不用分号结束。如果后面还有新行，则代码段的结束标记包含了行结束。

**示例：包含末尾换行符的结束标记**

```php
<?php echo "Some text"; ?>
No newline
<?= "But newline now" ?>
```

进入和退出PHP解析的例子

```php
<?php echo 'This is a test';?>
<?php echo 'This is a test' ?>
<?php echo 'We omitted the last closing tag';
```

> **注意**:文件末尾的 PHP 代码段结束标记可以不要，有些情况下当使用[include](https://www.php.net/manual/zh/function.include.php)或者[require](https://www.php.net/manual/zh/function.require.php)时省略掉会更好些，这样不期望的空白符就不会出现在文件末尾，之后仍然可以输出响应标头。在使用输出缓冲时也很便利，就不会看到由包含文件生成的不期望的空白符。

#### 注释

```php
<?php  
    // 单行注释
    /*
    多行注释
    */
    /*不要嵌套
    /*可能会出问题*/
    */
?>
```

### 类型

PHP 是动态类型语言，这意味着默认不需要指定变量的类型，因为会在运行时确定。然而，可以通过使用类型声明对语言的一些方面进行类型静态化。类型限制了可以对其执行的操作。然而，如果使用的表达式/变量不支持该操作，PHP 将尝试将该值类型转换为操作支持的类型。此过程取决于使用该值的上下文。

> 在类型转换时可以参考[PHP: PHP 类型比较表 - Manual](https://www.php.net/manual/zh/types.comparisons.php)，除了强制将表达式的值转换成某种类型，还可以使用`settype()`函数就地对变量进行类型转换。

使用`var_dump()`函数检查表达式的值和类型，使用`get_debug_type()`检索表达式的值和类型，使用`is_type`（这是一类函数，包括`is_string()`、`is_bool()`等）检查表达式是否属于某种类型。

```php
<?php
$a_bool = true;   // a bool
$a_str  = "foo";  // a string
$a_str2 = 'foo';  // a string
$an_int = 12;     // an int
echo get_debug_type($a_bool), "\n";
echo get_debug_type($a_str), "\n";

// 如果是整型，就加上 4
if (is_int($an_int)) {
    $an_int += 4;
}
var_dump($an_int);

// 如果 $a_bool 是字符串，就打印出来
if (is_string($a_bool)) {
    echo "String: $a_bool";  // 如果想要打印$，需要加上\
}
?>
```



#### 类型系统

**原子类型**：内置类型，跟语言紧密集成，不能用用户定义类型重现

可以将多个原子类型组合为**复合类型**。PHP 允许使用以下方式组合类型：

- 类类型（接口和类名）的交集。
- 类型联合。

**交集类型**接受满足多个类类型声明的值，而不是单个值。交集类型中的每个类型由`&`符号连接。因此，类型`T`、`U`和`V`组成的交集类型将写成`T&U&V`。

**联合类型**接受多个不同类型的值，而不是单个类型。联合类型中的每个类型由 `|` 符号连接。因此类型 `T`、`U`和`V`的联合类型写成`T|U|V`。如果其中一种类型是交集类型，需要使用括号括起来，在DNF中写成：`T|(X&Y)`。

PHP 支持两种类型别名：mixed和iterable，分别对应`object|resource|array|string|float|int|bool|null`和`Traversable|array`的联合类型。

> **注意**: PHP 不支持用户定义类型别名。

#### NULL

null类型是PHP的原子类型，也就是说，它仅有一个值null。未定义和`unset()`的变量都将解析为值null，使用`is_null()`判断是否为null。

```php
<?php
$a = 10;
if (! is_null($a)) {
    echo "not null";
}

unset($a);
if (is_null($a)) {
    echo "null";
}
?>
```



#### Boolean

bool仅有两个值，true和false（不区分大小写），强制转换：`(bool)`

#### Integer

```php
$a = 1_234_567	// 也是整数数值
```

整型数int的字长和平台有关，尽管通常最大值是大约二十亿（32 位有符号）。64 位平台下的最大值通常是大约 9E18。 PHP 不支持无符号的 int。int 值的字长可以用常量`PHP_INT_SIZE`来表示， 最大值可以用常量 `PHP_INT_MAX`来表示， 最小值可以用常量`PHP_INT_MIN`表示。PHP没有int除法取整运算符，要使用[intdiv()](https://www.php.net/manual/zh/function.intdiv.php) 实现。`1/2`的结果为float`0.5`。值可以舍弃小数部分，强制转换为int，或者使用[round()](https://www.php.net/manual/zh/function.round.php)函数可以更好地进行四舍五入。

> 绝不要将未知的分数强制转换为 int，这样有时会导致不可预料的结果。
>
> ```php
> <?php
> echo (int) ((0.1 +0.7) * 10);		// 7
> echo ((int) (0.1*10)) + (int) (0.7*10) ; // 8
> ?>
> ```

#### Float

浮点数的精度有限。尽管取决于系统，PHP 通常使用 IEEE 754 双精度格式，则由于取整而导致的最大相对误差为 1.11e-16。非基本数学运算可能会给出更大误差，并且要考虑到进行复合运算时的误差传递。所以永远不要相信浮点数结果精确到了最后一位，也永远不要比较两个浮点数是否相等。如果确实需要更高的精度，应该使用[任意精度数学函数](https://www.php.net/manual/zh/ref.bc.php)或者 [gmp 函数](https://www.php.net/manual/zh/ref.gmp.php)。

#### String

一个字符串 string 就是由一系列的字符组成，其中每个字符等同于一个字节。这意味着 PHP 只能支持 256 的字符集，因此不支持 Unicode 。详见[字符串类型详解](https://www.php.net/manual/zh/language.types.string.php#language.types.string.details)。

除了单引号和双引号，PHP中还有Heredoc结构（支持空格和制表符）

```php
echo <<<END
    sjaksja /*
sajska // sa
   sajsa */
END;
// 输出为
/*
    sjaksja /*
sajska // sa
   sajsa */
*/
$values = [<<<END
a
  b
    c
END, 'd e f'];
var_dump($values);
/*
array(2) {
  [0] =>
  string(11) "a
  b
    c"
  [1] =>
  string(5) "d e f"
}
*/
```

Nowdoc结构

```php
echo <<<'EOD'
Example of string spanning multiple lines
using nowdoc syntax. Backslashes are always treated literally,
e.g. \\ and \'.
EOD;
```

##### 字符串的索引

**负数索引（与python类似）**

```php
$string = 'string';
echo "The character at index -2 is $string[-2].", PHP_EOL;  
// The character at index -2 is n.
```

##### 字符串格式化

```php
$great = 'fantastic';
// 输出：this is fantastic
echo "this is $great", PHP_EOL;
// 无效，输出：This is { fantastic}
echo "This is { $great}", PHP_EOL;
// 有效，输出： This is fantastic
echo "This is {$great}", PHP_EOL;
```

如果只是单个变量，可以直接在字符串中输出，但是如果有`$arr[0]`、`$arr->value`等变量，则必须加上`{}`，且`$`需要紧挨着`{`。

##### 字符串的操作

`strlen()`：获取字符串的长度

`$str1 . $str2`：字符串拼接

`(string)`或`strval`：转成字符串

`substr($str, a, b)`：字符串切片，相当于python中的`str[a:b]`

`strpos($str, $findstr, $offset=0)`：查找`$findstr`在`$str`中第一次出现的位置

`strcmp($str1, $str2)`：比较字符串（区分大小写）

[PHP: 字符串 函数 - Manual](https://www.php.net/manual/zh/ref.strings.php)



#### 数字字符串

```php
var_dump("0D1" == "000"); // false, "0D1" 不是科学计数法
var_dump("0E1" == "000"); // true, "0E1" is 0 * (10 ^ 1), or 0
var_dump("2E1" == "020"); // true, "2E1" is 2 * (10 ^ 1), or 20
```

自PHP8.0.0起，前导数字的数字字符串如"10 apples"可以被转成10，但是后导数字如"apples 10"+10则会引发错误。

#### Array数组

PHP 中的 array 实际上是一个有序映射。映射是一种把 *values* 关联到 *keys* 的类型。此类型针对多种不同用途进行了优化； 它可以被视为数组、列表（向量）、哈希表（映射的实现）、字典、集合、堆栈、队列等等。 由于 array 的值可以是其它 array 所以树形结构和多维 array 也是允许的。

```php
$array = array(
    "foo" => "bar",  // key => value
    "bar" => "foo",
);
// 使用短数组语法
$array = [
    "foo" => "bar",
    "bar" => "foo",
];
```

key 可以是 integer 或者 string。value 可以是任意类型。如果在数组定义时多个元素都使用相同键名，那么只有最后一个会被使用，其它的元素都会被覆盖（注意键值会有强制转换）。key 为可选项。如果未指定，PHP 将自动使用之前用过的最大 int 键名加上 1 作为新的键名。

##### 数组解包

```php
$source_array = ['foo', 'bar', 'baz'];
[$foo, $bar, $baz] = $source_array;

// 在foreach中使用
$source_array = [
    [1, 'John'],
    [2, 'Jane'],
];
foreach ($source_array as [$id, $name]) {
    // 这里是 $id 和 $name 的逻辑
}

// 解包关联数组
$source_array = ['foo' => 1, 'bar' => 2, 'baz' => 3];
// 将索引 'baz' 处的元素分配给变量 $three
['baz' => $three] = $source_array;

// 用于变量交换
[$b, $a] = [$a, $b];

// ...用于解包
$arr1 = [1, 2, 3];
$arr3 = [0, ...$arr1]; //[0, 1, 2, 3]
```



##### 数组操作

`sort`：排序

`array_push($arr, $v)`：元素入栈（注意PHP中数组的一些常见操作如map，filter，pop，sum等都有`array_`的前缀）

[PHP: 数组 函数 - Manual](https://www.php.net/manual/zh/ref.array.php)



#### object对象

要创建一个新的对象 object，使用 `new` 语句实例化一个类：

```php
class User
{
    public int $id;
    public ?string $name;

    public function __construct(int $id, ?string $name)
    {
        $this->id = $id;
        $this->name = $name;
    }
    public function printUser(){
        echo $this->id, " ", $this->name, PHP_EOL;
    }
}
$user = new User(1234, "tom");
echo $user->id, PHP_EOL;
$user->printUser();
```

[PHP: 类与对象 - Manual](https://www.php.net/manual/zh/language.oop5.php)

PHP中有静态属性（用`static`标识），静态方法不需要通过对象即可调用，所以`$this`在静态方法中不可用，静态属性使用`::`来访问。

PHP中也有抽象类，定义为抽象的类不能被实例化。任何一个类，如果它里面至少有一个方法是被声明为抽象的，那么这个类就必须被声明为抽象的。被定义为抽象的方法只是声明了其调用方式（参数），不能定义其具体的功能实现。继承一个抽象类的时候，子类必须定义父类中的所有抽象方法， 并遵循常规的 [继承](https://www.php.net/manual/zh/language.oop5.inheritance.php) [签名兼容性](https://www.php.net/manual/zh/language.oop5.basic.php#language.oop.lsp) 规则。

```php
// 抽象类示例
abstract class AbstractClass
{
 // 强制要求子类定义这些方法
    abstract protected function getValue();
    abstract protected function prefixValue($prefix);

    // 普通方法（非抽象方法）
    public function printOut() {
        print $this->getValue() . "\n";
    }
}
class ConcreteClass1 extends AbstractClass
{
    protected function getValue() {
        return "ConcreteClass1";
    }

    public function prefixValue($prefix) {
        return "{$prefix}ConcreteClass1";
    }
}
```

#### Enum枚举

枚举是在类、类常量基础上的约束层， 目标是提供一种能力：定义包含可能值的封闭集合类型。

```php
enum Suit
{
    case Hearts;
    case Diamonds;
    case Clubs;
    case Spades;
}
function do_stuff(Suit $s)
{
    // ...
}
do_stuff(Suit::Spades);
```

#### Resource资源类型

资源 resource 是一种特殊变量，保存了到外部资源的一个引用。资源是通过专门的函数来建立和使用的。所有这些函数及其相应资源类型见[附录](https://www.php.net/manual/zh/resource.php)。

`is_resource()`：判断是否是资源

`get_resource_type()`：返回资源的类型

引用计数系统是 Zend 引擎的一部分，可以自动检测到一个资源不再被引用了（和 Java 一样）。这种情况下此资源使用的所有外部资源都会被垃圾回收系统释放。因此，很少需要手工释放内存。

> **注意**: 持久数据库连接比较特殊，它们*不会*被垃圾回收系统销毁。参见[数据库永久连接](https://www.php.net/manual/zh/features.persistent-connections.php)一章。



#### callback类型

回调可以通过 [callable](https://www.php.net/manual/zh/language.types.callable.php) 类型声明来表示。一些函数如 [call_user_func()](https://www.php.net/manual/zh/function.call-user-func.php) 或 [usort()](https://www.php.net/manual/zh/function.usort.php) 可以接受用户自定义的回调函数作为参数。回调函数不止可以是简单函数，还可以是对象的方法，包括静态类方法。

```php
// 闭包
$double = function($a) {
    return $a * 2;
};

// 这是数字范围
$numbers = range(1, 5);

// 这里使用闭包作为回调，
// 将范围内的每个元素数值翻倍
$new_numbers = array_map($double, $numbers);

print implode(' ', $new_numbers);	// 用字符串连接数组元素
```



#### Mixed/Void/Never

[mixed](https://www.php.net/manual/zh/language.types.declarations.php#language.types.declarations.mixed) 类型接受每个值。等同于[联合类型](https://www.php.net/manual/zh/language.types.type-system.php#language.types.type-system.composite.union) `object|resource|array|string|float|int|bool|null`。自 PHP 8.0.0 起可用。在类型理论中，[mixed](https://www.php.net/manual/zh/language.types.declarations.php#language.types.declarations.mixed) 是顶级类型。这意味着其它所有类型都是它的子类型。

void 是仅用于返回类型，表示函数不返回值，但该函数仍可能会终止。因此，它不能成为[联合类型](https://www.php.net/manual/zh/language.types.type-system.php#language.types.type-system.composite.union)声明的一部分。自 PHP 7.1.0 起可用。

never 是仅用于返回的类型，表示函数不会终止。这意味着它要么调用 [exit()](https://www.php.net/manual/zh/function.exit.php)，要么抛出异常，要么无限循环。因此，它不能是[联合类型](https://www.php.net/manual/zh/language.types.type-system.php#language.types.type-system.composite.union)声明的一部分。自 PHP 8.1.0 起可用。never 是类型理论中的最底层类型。这意味着它是其它所有类型的子类型，并在可以在继承期间替换其它任何返回类型。



#### 可迭代类型

```php
function gen(): iterable {
    yield 1;
    yield 2;
    yield 3;
}
$new_numbers = gen();
foreach ($new_numbers as $value) {
    echo $value, PHP_EOL;
}
```

#### 类型转换

[PHP: 类型转换 - Manual](https://www.php.net/manual/zh/language.types.type-juggling.php)



### 变量

#### 基础

PHP中的变量名可以用中文，可以以下划线开头，但不可以以数字开头。

PHP中的引用

```php
$foo = 'Bob';              // 将 'Bob' 赋给 $foo
$bar = &$foo;              // 通过 $bar 引用 $foo
$bar = "My name is $bar";  // 修改 $bar 变量
echo $bar, PHP_EOL;
echo $foo, PHP_EOL;                 // $foo 的值也被修改
function change_bar(&$bar){         // 通过引用传递，值的修改可以传递到函数外
    $bar = "$bar is change with &";
}
function can_not_change_bar($bar){
    $bar = "can not change \$bar outside";
    echo $bar, PHP_EOL;             // 内部改变
}
change_bar($bar);
echo $bar, PHP_EOL;                 // 值会被修改
echo $foo, PHP_EOL;                 // 值会被修改
can_not_change_bar($bar);
echo $bar, PHP_EOL;                 // 值不会被修改
echo $foo, PHP_EOL;                 // 值不会被修改
```

输出为：

```text
My name is Bob
My name is Bob
My name is Bob is change with &
My name is Bob is change with &
can not change $bar outside
My name is Bob is change with &
My name is Bob is change with &
```



#### 预定义变量

PHP 提供了大量的预定义变量。由于许多变量依赖于运行的服务器的版本和设置，及其它因素，所以并没有详细的说明文档。一些预定义变量在 PHP 以[命令行](https://www.php.net/manual/zh/features.commandline.php)形式运行时并不生效。 详细参阅[预定义变量](https://www.php.net/manual/zh/reserved.variables.php)一章。



#### 变量范围

变量的范围即它定义的上下文背景（也就是它的生效范围）。大部分的 PHP 变量只有一个单独的范围。这个单独的范围跨度同样包含了 include 和 require 引入的文件。例如：

```php
<?php
$a = 1;			// 变量$a将会在包含文件b.inc中生效。
include 'b.inc';
?>
```

##### 全局变量

在用户自定义函数中，一个局部函数范围将被引入。任何用于函数内部的变量按缺省情况将被限制在局部函数范围内。例如：

```php
<?php
$a = 1; /* global scope */
function Test()
{
    echo $a; /* reference to local scope variable */
}
Test();
?>
```

如果想要使用全局变量，必须在函数中声明`global`：

```php
$a = 1;
$b = 2;
function Sum()
{
    global $a, $b;
    $b = $a + $b;
}
Sum();
echo $b;	// 3
```

除了使用`global`声明，还可以使用`$GLOBALS`数组

```php
$a = 1;
$b = 2;
function Sum()
{
    $GLOBALS['b'] = $GLOBALS['a'] + $GLOBALS['b'];
}
Sum();
echo $b;
```

[$GLOBALS](https://www.php.net/manual/zh/reserved.variables.globals.php) 是一个关联数组，每一个变量为一个元素，键名对应变量名，值对应变量的内容。[$GLOBALS](https://www.php.net/manual/zh/reserved.variables.globals.php) 之所以在全局范围内存在，是因为`$GLOBALS`是一个[超全局变量](https://www.php.net/manual/zh/language.variables.superglobals.php)。

##### 静态变量

变量范围的另一个重要特性是*静态变量*（static variable）。静态变量仅在局部函数域中存在，但当程序执行离开此作用域时，其值并不丢失。

```php
function test()
{
    static $a = 0;
    echo $a, PHP_EOL;
    $a++;
}

test();		// a=0
test();		// a=1
```

变量`$a`仅在第一次调用`test()`函数时被初始化，之后每次调用`test()`函数都会输出`$a`的值并加一。静态变量可以在递归函数中使用，如下面的例子

```php
function test()
{
    static $count = 0;

    $count++;
    if ($count < 10) {
        test();
    }
    echo $count, " ";
    $count--;
}
test();   // 输出10 9 8 7 6 5 4 3 2 1 
```

常量表达式的结果可以赋值给静态变量，但是动态表达式（比如函数调用）会导致解析错误。从 PHP 8.1.0 开始，当继承（不是覆盖）使用有静态变量的方法时，继承的方法将会跟父级方法共享静态变量。这意味着方法中的静态变量现在跟静态属性有相同的行为。

##### 全局和静态变量的引用

对于变量的 [static](https://www.php.net/manual/zh/language.variables.scope.php#language.variables.scope.static) 和 [global](https://www.php.net/manual/zh/language.variables.scope.php#language.variables.scope.global) 定义是以[引用](https://www.php.net/manual/zh/language.references.php)的方式实现的。例如，在一个函数域内部用 `global` 语句导入的一个真正的全局变量实际上是建立了一个到全局变量的引用。这有可能导致预料之外的行为。



#### 可变变量

有时候使用可变变量名是很方便的。就是说，一个变量的变量名可以动态的设置和使用。一个普通的变量通过声明来设置，例如：

```php
$a = "hello";
$$a = "world";  // 可变变量
echo "$a {$$a}\n";  // hello world
echo "$a $hello";   // hello world
```

```php
$Bar = "a";
$Foo = "Bar";
$World = "Foo";
$Hello = "World";
$a = "Hello";

echo $a; //Returns Hello
echo $$a; //Returns World
echo $$$a; //Returns Foo
echo $$$$a; //Returns Bar
echo $$$$$a; //Returns a
```

#### 来自PHP之外的变量

##### 表单

当一个表单提交给 PHP 脚本时，表单中的信息会自动在脚本中可用。有几个方法访问此信息，例如：

**示例：一个简单的HTML表单**

```html
<form action="foo.php" method="POST">
    Name:  <input type="text" name="username"><br />
    Email: <input type="text" name="email"><br />
    <input type="submit" name="submit" value="Submit me!" />
</form>
```

只有两种方法可以访问 HTML 表单中的数据。 以下列出了当前有效的方法：

**示例：从一个简单的 POST HTML 表单访问数据**

```php
<?php
echo $_POST['username'];
echo $_REQUEST['username'];
?>
```

> 变量名中的点和空格被转换成下划线。例如 `<input name="a.b" />` 变成了 `$_REQUEST["a_b"]`。

**示例：更复杂的表单变量**

```php+HTML
<?php
if (isset($_POST['action']) && $_POST['action'] == 'submitted') {
    echo '<pre>';

    print_r($_POST);
    echo '<a href="'. $_SERVER['PHP_SELF'] .'">Please try again</a>';

    echo '</pre>';
} else {
?>
<form action="<?php echo $_SERVER['PHP_SELF']; ?>" method="post">
    Name:  <input type="text" name="personal[name]"><br />
    Email: <input type="text" name="personal[email]"><br />
    Beer: <br>
    <select multiple name="beer[]">
        <option value="warthog">Warthog</option>
        <option value="guinness">Guinness</option>
        <option value="stuttgarter">Stuttgarter Schwabenbr</option>
    </select><br />
    <input type="hidden" name="action" value="submitted" />
    <input type="submit" name="submit" value="submit me!" />
</form>
<?php
}
?>
```

##### HTTP Cookies

```php
<?php
  setcookie("MyCookie[foo]", 'Testing 1', time()+3600);
  setcookie("MyCookie[bar]", 'Testing 2', time()+3600);
?>
```

这将会建立两个单独的 cookie，尽管 MyCookie 在脚本中是一个单一的数组。如果想在仅仅一个 cookie 中设定多个值，考虑先在值上使用 [serialize()](https://www.php.net/manual/zh/function.serialize.php) 或 [explode()](https://www.php.net/manual/zh/function.explode.php)。注意在浏览器中一个 cookie 会替换掉上一个同名的 cookie，除非路径或者域不同。



### 常量

常量名和变量遵循同样的命名规则。可以通过`define`来定义常量，但是不推荐。

```php
define("FOO",     "something");
```

#### 语法

常量可以用`constant`或`define`来定义，常量和变量有如下不同：

- 常量前面没有美元符号（`$`）；
- 常量可以不用理会变量的作用域而在任何地方定义和访问；
- 常量一旦定义就不能被重新定义或者取消定义；
- 常量只能计算标量值或数组。

```php
const CONSTANT = 'Hello World';
const ANIMALS = array('dog', 'cat', 'bird');
echo ANIMALS[1]; // 将输出 "cat"

// 常量数组
define('ANIMALS', array(
    'dog',
    'cat',
    'bird'
));
echo ANIMALS[1]; // 将输出 "cat"
?>
```

**注意**:

> 和使用 [define()](https://www.php.net/manual/zh/function.define.php) 来定义常量相反的是，使用`const`关键字定义常量必须处于最顶端的作用域，因为用此方法是在编译时定义的。这就意味着不能在函数内，循环内以及`if`或`try`/`catch`语句之内用`const`来定义常量。

#### 预定义常量

PHP 向它运行的任何脚本提供了大量的[预定义常量](https://www.php.net/manual/zh/reserved.constants.php)。不过很多常量都是由不同的扩展库定义的，只有在加载了这些扩展库时才会出现，或者动态加载后，或者在编译时已经包括进去了。

#### 魔术常量

有九个魔术常量它们的值随着它们在代码中的位置改变而改变。例如 **`__LINE__`** 的值就依赖于它在脚本中所处的行来决定。这些特殊的常量不区分大小写，如下：

| 名字               | 说明                                                         |
| :----------------- | :----------------------------------------------------------- |
| `__LINE__`         | 文件中的当前行号。                                           |
| `__FILE__`         | 文件的完整路径和文件名。如果用在被包含文件中，则返回被包含的文件名。 |
| `__DIR__`          | 文件所在的目录。如果用在被包括文件中，则返回被包括的文件所在的目录。它等价于 `dirname(__FILE__)`。除非是根目录，否则目录中名不包括末尾的斜杠。 |
| `__FUNCTION__`     | 当前函数的名称。匿名函数则为 `{closure}`。                   |
| `__CLASS__`        | 当前类的名称。类名包括其被声明的作用域（例如 `Foo\Bar`）。当用在 trait 方法中时，`__CLASS__`是调用 trait 方法的类的名字。 |
| `__TRAIT__`        | Trait 的名字。Trait 名包括其被声明的作用域（例如 `Foo\Bar`）。 |
| `__METHOD__`       | 类的方法名。                                                 |
| `__NAMESPACE__`    | 当前命名空间的名称。                                         |
| `ClassName::class` | 完整的类名。                                                 |



### 表达式

有递增（`++`）和递减（`--`）操作符，与c中的定义相似

比较表达式：支持 >（大于）、>=（大于等于）、==（等于）、!=（不等于）、<（小于）、<= (小于等于)。PHP 还支持全等运算符 ===（值和类型均相同）和非全等运算符 !==（值或者类型不同）。



### 运算符

#### 运算符优先级

没有结合的相同优先级的运算符不能连在一起使用，例如 `1 < 2 > 1` 在PHP是不合法的。

[PHP: 运算符优先级 - Manual](https://www.php.net/manual/zh/language.operators.precedence.php)

三元运算符：`? :`



#### 算术运算符

`/`：除法，`%`：取余，`**`：幂，`intdiv()`：整除



#### 赋值运算符

```php
$a = ($b = 4) + 5; // $a 现在成了 9，而 $b 成了 4。
$a = 3;
$a += 5; // 设置 $a 为 8 ，之前说过： $a = $a + 5;
$b = "Hello ";
$b .= "There!"; // 设置 $b 为 "Hello There!"，就像 $b = $b . "There!";
```

#### 位运算符

| 例子           | 名称                | 结果                                                     |
| :------------- | :------------------ | :------------------------------------------------------- |
| **`$a & $b`**  | And（按位与）       | 将把`$a` 和`$b`中都为 1 的位设为 1。                     |
| **`$a | $b`**  | Or（按位或）        | 将把`$a` 和`$b`中任何一个为 1 的位设为 1。               |
| **`$a ^ $b`**  | Xor（按位异或）     | 将把`$a`和`$b`中一个为 1 另一个为 0 的位设为 1。         |
| **`~ $a`**     | Not（按位取反）     | 将`$a`中为 0 的位设为 1，反之亦然。                      |
| **`$a << $b`** | Shift left（左移）  | 将`$a`中的位向左移动`$b`次（每一次移动都表示“乘以 2”）。 |
| **`$a >> $b`** | Shift right（右移） | 将`$a`中的位向右移动`$b`次（每一次移动都表示“除以 2”）。 |

#### 比较运算符

其他的无需说明，仅说明下面两个运算符
`$a <> $b`：不等，与`$a != $b`相同
`$a <=> $b`：太空船运算符（组合比较符），当`$a`小于、等于、大于`$b`时分别返回一个小于、等于、大于0的 int 值。

#### 错误控制运算符
PHP 支持一个错误控制运算符：`@`。当将其放置在一个 PHP 表达式之前，该表达式可能产生的任何错误诊断都被抑制。
> **注意**: `@` 运算符只对 [表达式](https://www.php.net/manual/zh/language.expressions.php) 有效。 对新手来说一个简单的规则就是：如果能从某处获得值，就能在它前面加上 `@` 运算符。例如，可以把它放在变量，函数调用，某些语言构造调用（例如 [include](https://www.php.net/manual/zh/function.include.php) ）等等之前。 不能把它放在函数或类的定义之前，也不能用于条件结构例如 `if` 和 [foreach](https://www.php.net/manual/zh/control-structures.foreach.php) 等。

日志函数：[PHP: syslog - Manual](https://www.php.net/manual/zh/function.syslog.php)

#### 执行运算符
PHP 支持一个执行运算符：反引号&#96; &#96;。PHP 将尝试将反引号&#96; &#96;中的内容作为 shell 命令来执行，并将其输出信息返回（可以赋给一个变量而不是简单地丢弃到标准输出）。使用反引号运算符的效果与函数 [shell_exec()](https://www.php.net/manual/zh/function.shell-exec.php) 相同。
```php
$output = `ls -al`;
echo "<pre>$output</pre>";
```

#### 逻辑运算符

| 例子      | 名称            | 结果                                                      |
| :-------- | :-------------- | :-------------------------------------------------------- |
| `$a` and `$b` | And（逻辑与）   | `true`，如果 `$a` 和 `$b` 都为 `true`               |
| `$a` or `$b`  | Or（逻辑或）    | `true`，如果 `$a` 或 `$b` 任一为 `true`             |
| `$a` xor `$b` | Xor（逻辑异或） | 如果 `$a` 或 `$b`不同为真，相同为假 |
| !`$a`   | Not（逻辑非）   | `true`，如果 `$a` 不为 **`true`**。                     |
| `$a` && `$b`  | And（逻辑与）   | `true`，如果 `$a` 和 `$b` 都为 `true`。               |
| `$a` || `$b`  | Or（逻辑或）    | `true`，如果 `$a` 或 `$b` 任一为 `true`。             |

“与”和“或”有两种不同形式运算符的原因是它们运算的优先级不同（见[运算符优先级](https://www.php.net/manual/zh/language.operators.precedence.php)）。

#### 数组运算符

| 例子          | 名称   | 结果                                                         |
| :------------ | :----- | :----------------------------------------------------------- |
| `$a` + `$b`   | 联合   | `$a` 和`$b`的联合。                                          |
| `$a` == `$b`  | 相等   | 如果`$a`和`$b`具有相同的键／值对则为`true`。                 |
| `$a` === `$b` | 全等   | 如果 `$a` 和 `$b` 具有相同的键／值对并且顺序和类型都相同则为`true`。 |
| `$a` != `$b`  | 不等   | 如果 `$a` 不等于`$b` 则为`true`。                            |
| `$a` <> `$b`  | 不等   | 如果`$a`不等于`$b`则为`true`。                               |
| `$a` !== `$b` | 不全等 | 如果`$a`不全等于`$b`则为`true`。                             |

#### 类型运算符
`instanceof` 用于确定一个 PHP 变量是否属于某一类 [class](https://www.php.net/manual/zh/language.oop5.basic.php#language.oop5.basic.class) 的实例：

### 流程控制
#### if
```php
if ($a > $b) {  
echo "a is bigger than b";  
} elseif ($a == $b) {  
echo "a is equal to b";  
} else {  
echo "a is smaller than b";  
}
```

#### 流程控制的替代语法
PHP 提供了一些流程控制的替代语法，包括 `if`，`while`，`for`，`foreach` 和 `switch`。替代语法的基本形式是把左花括号（{）换成冒号（:），把右花括号（}）分别换成 `endif;`，`endwhile;`，`endfor;`，`endforeach;` 以及 `endswitch;`。
```php
<?php
$a =5;
if ($a == 5) {
    echo "A is equal to 5";
}
```
等同于
```php
<?php  $a =5; ?>
<?php if ($a == 5): ?>  
A is equal to 5  
<?php endif; ?>
```

#### while
```php
$i = 1;  
while ($i <= 10) {  
echo $i++; /* 在自增前（后自增）打印的值将会是 $i */  
}  

$i = 1;  
while ($i <= 10):  
print $i;  
$i++;  
endwhile;
```

#### do-while
```php
$i = 0;  
do {  
echo $i;  
} while ($i > 0);
```

#### for/foreach
```php
for ($i = 1; $i <= 10; $i++) {  
	echo $i;  
}

$arr = array(1, 2, 3, 4);  
foreach ($arr as &$value) {  
	$value = $value * 2;  
}
// 现在 $arr 是 array(2, 4, 6, 8)  
unset($value); // 最后取消掉引用
```
>由于在循环使用了引用，数组最后一个元素的 `$value` 引用在 `foreach` 循环之后仍会保留。建议使用 [unset()](https://www.php.net/manual/zh/function.unset.php) 来将其销毁。否则，将会遇到下面的情况
```php
<?php  
$arr = array(1, 2, 3, 4);  
foreach ($arr as &$value) {  
$value = $value * 2;  
}  
// 现在 $arr 是 array(2, 4, 6, 8)  
  
// 未使用 unset($value) 时，$value 仍然引用到最后一项 $arr[3]  
  
foreach ($arr as $key => $value) {  
// $arr[3] 会被 $arr 的每一项值更新掉…  
echo "{$key} => {$value} ";  
print_r($arr);  
}  
// 直到最终倒数第二个值被复制到最后一个值  
  
// output:  
// 0 => 2 Array ( [0] => 2, [1] => 4, [2] => 6, [3] => 2 )  
// 1 => 4 Array ( [0] => 2, [1] => 4, [2] => 6, [3] => 4 )  
// 2 => 6 Array ( [0] => 2, [1] => 4, [2] => 6, [3] => 6 )  
// 3 => 6 Array ( [0] => 2, [1] => 4, [2] => 6, [3] => 6 )  
?>
```

#### break/continue
具体功能与其它语言类似，break可以带参数（默认为1），`break 2`表示跳出2层循环。

#### switch
```php
switch ($i) {  
	case 0:  
		echo "i equals 0";  
		break;  
	case 1:  
		echo "i equals 1";  
		break;  
	case 2:  
		echo "i equals 2";  
		break;  
	default:  
		echo "i is not equal to 0, 1 or 2";  
}
```

#### match
`match` 表达式基于值的一致性进行分支计算。 `match`表达式和 `switch` 语句类似， 都有一个表达式主体，可以和多个可选项进行比较。 与 `switch` 不同点是，它会像三元表达式一样求值。 与 `switch` 另一个不同点，它的比较是严格比较（ `===`）而不是松散比较（`==`）。 Match 表达式从 PHP 8.0.0 起可用。
```php
$food = 'cake';  
$return_value = match ($food) {  
	'apple' => 'This food is an apple',  
	'bar' => 'This food is a bar',  
	'cake' => 'This food is a cake',  
};  
```
> **注意**: `match` 表达式_必须_使用分号 `;` 结尾。

`match` 表达式跟 `switch` 语句相似，但是有以下关键区别：
- `match` 比较分支值，使用了严格比较 (`===`)， 而 switch 语句使用了松散比较。
- `match` 表达式会返回一个值。
- `match` 的分支不会像 `switch` 语句一样， 落空时执行下个 case。
- `match` 表达式必须彻底列举所有情况。

#### declare
`declare` 结构用来设定一段代码的执行指令。
##### ticks
Tick（时钟周期）是一个在 `declare` 代码段中解释器每执行 N 条可计时的低级语句就会发生的事件。N 的值是在 `declare` 中的 `directive` 部分用 `ticks=N` 来指定的。不是所有语句都可计时。通常条件表达式和参数表达式都不可计时。在每个 tick 中出现的事件是由 [register_tick_function()](https://www.php.net/manual/zh/function.register-tick-function.php) 来指定的。更多细节见下面的例子。注意每个 tick 中可以出现多个事件。
```php
declare(ticks=1);  
  
// 每次 tick 事件都会调用该函数  
function tick_handler()  
{  
echo "tick_handler() called\n";  
}  
  
register_tick_function('tick_handler'); // 引起 tick 事件  
  
$a = 1; // 引起 tick 事件  
  
if ($a > 0) {  
$a += 2; // 引起 tick 事件  
print($a); // 引起 tick 事件  
}
```
注销每个 tick 上需要执行的函数：`unregister_tick_function()`

##### Encoding
可以用 `encoding` 指令来对每段脚本指定其编码方式。
```php
declare(encoding='ISO-8859-1');
```

#### include
`include` 表达式包含并运行指定文件。被包含文件先按参数给出的路径寻找，如果没有给出目录（只有文件名）时则按照 [include_path](https://www.php.net/manual/zh/ini.core.php#ini.include-path) 指定的目录寻找。如果在 [include_path](https://www.php.net/manual/zh/ini.core.php#ini.include-path) 下没找到该文件则 `include` 最后才在调用脚本文件所在的目录和当前工作目录下寻找。如果最后仍未找到文件则 `include` 结构会发出一条 **`E_WARNING`** ；这一点和 [require](https://www.php.net/manual/zh/function.require.php) 不同，后者会发出一个 **`E_ERROR`** 。
`vars.php`
```php
<?php  
$color = 'green';  
$fruit = 'apple';  
?>
```
`test.php`
```php
<?php  
echo "A $color $fruit"; // A  
include 'vars.php';  
echo "A $color $fruit"; // A green apple  
?>
```
#### include_once
`include_once` 语句在脚本执行期间包含并运行指定文件。此行为和 [include](https://www.php.net/manual/zh/function.include.php) 语句类似，唯一区别是如果该文件中已经被包含过，则不会再次包含，且 include_once 会返回 **`true`**。 顾名思义，require_once，文件仅仅包含（require）一次。`include_once` 可以用于在脚本执行期间同一个文件有可能被包含超过一次的情况下，想确保它只被包含一次以避免函数重定义，变量重新赋值等问题。

#### goto
`goto` 操作符可以用来跳转到程序中的另一位置。该目标位置可以用 _区分大小写_ 的目标名称加上冒号来标记，而跳转指令是 `goto` 之后接上目标位置的标记。PHP 中的 `goto` 有一定限制，目标位置只能位于同一个文件和作用域，也就是说无法跳出一个函数或类方法，也无法跳入到另一个函数。也无法跳入到任何循环或者 switch 结构中。可以跳出循环或者 switch，通常的用法是用 `goto` 代替多层的 `break`。

### 函数
函数的定义没有什么新意，默认参数可以通过`$a=1`或者`$a:1`来表示。

#### 可变函数
PHP 支持可变函数的概念。这意味着如果一个变量名后有圆括号，PHP 将寻找与变量的值同名的函数，并且尝试执行它。可变函数可以用来实现包括回调函数，函数表在内的一些用途。
```php
function foo() {
    echo "In foo()<br />\n";
}
function bar($arg = '')
{
    echo "In bar(); argument was '$arg'.<br />\n";
}
// 使用 echo 的包装函数
function echoit($string)
{
    echo $string;
}
$func = 'foo';
$func();        // 调用 foo()

$func = 'bar';
$func('test');  // 调用 bar()

$func = 'echoit';
$func('test');  // 调用 echoit()
```
也可以用可变函数的语法来调用一个对象的方法。

#### 内部（内置）函数
PHP 有很多标准的函数和结构。还有一些函数需要和特定地 PHP 扩展模块一起编译，否则在使用它们的时候就会得到一个致命的“未定义函数”错误。例如，要使用 [image](https://www.php.net/manual/zh/ref.image.php) 函数中的 [imagecreatetruecolor()](https://www.php.net/manual/zh/function.imagecreatetruecolor.php)，需要在编译 PHP 的时候加上 GD 的支持。或者，要使用 [mysqli_connect()](https://www.php.net/manual/zh/function.mysqli-connect.php) 函数，就需要在编译 PHP 的时候加上 [MySQLi](https://www.php.net/manual/zh/book.mysqli.php) 支持。有很多核心函数已包含在每个版本的 PHP 中如[字符串](https://www.php.net/manual/zh/ref.strings.php)和[变量](https://www.php.net/manual/zh/ref.var.php)函数。调用 [phpinfo()](https://www.php.net/manual/zh/function.phpinfo.php) 或者 [get_loaded_extensions()](https://www.php.net/manual/zh/function.get-loaded-extensions.php) 可以得知 PHP 加载了那些扩展库。同时还应该注意，很多扩展库默认就是有效的。PHP 手册按照不同的扩展库组织了它们的文档。请参阅[配置](https://www.php.net/manual/zh/configuration.php)，[安装](https://www.php.net/manual/zh/install.php)以及各自的扩展库章节以获取有关如何设置 PHP 的信息。

#### 匿名函数
匿名函数（Anonymous functions），也叫闭包函数（`closures`），允许 临时创建一个没有指定名称的函数。最经常用作回调函数 [callable](https://www.php.net/manual/zh/language.types.callable.php)参数的值。当然，也有其它应用的情况。类似于JavaScript的回调函数定义。
```php
echo preg_replace_callback('~-([a-z])~', function ($match) {  
return strtoupper($match[1]);  
}, 'hello-world');
// 输出 helloWorld
```
闭包函数也可以作为变量的值来使用。PHP 会自动把此种表达式转换成内置类 [Closure](https://www.php.net/manual/zh/class.closure.php) 的对象实例。把一个 closure 对象赋值给一个变量的方式与普通变量赋值的语法是一样的，最后也要加上分号：
```php
$greet = function($name) {  
printf("Hello %s\r\n", $name);  
};  
  
$greet('World');  
$greet('PHP');
```
闭包可以从父作用域中继承变量。 任何此类变量都应该用 `use` 语言结构传递进去。 PHP 7.1 起，不能传入此类变量： [superglobals](https://www.php.net/manual/zh/language.variables.predefined.php)、 $this 或者和参数重名。 返回类型声明必须放在 `use` 子句的后面。
```php
$message = 'hello';  
  
// 没有 "use"  
$example = function () {  
var_dump($message);  
};  
$example();  // 会报warning，$message为NULL
// 继承 $message  
$example = function () use ($message) {  
var_dump($message);  
};  
$example();  // 继承了$message
```

#### 箭头函数
是一种更简洁的匿名函数写法。箭头函数的基本语法为 `fn (argument_list) => expr`。箭头函数支持与 [匿名函数](https://www.php.net/manual/zh/functions.anonymous.php) 相同的功能，只是其父作用域的变量总是自动的。
```php
<?php  
  
$y = 1;  
  
$fn1 = fn($x) => $x + $y;  
// 相当于通过 value 使用 $y：  
$fn2 = function ($x) use ($y) {  
return $x + $y;  
};  
  
var_export($fn1(3));  
?>
```

#### First class callable syntax
从回调函数创建匿名函数的一种方式，它使用字符串和数组取代现有的可调用语法。这种语法的优点是可以对静态分析进行访问，并在获取可调用性时使用作用域。

### 类与对象
相比[PHP: Object 对象 - Manual](https://www.php.net/manual/zh/language.types.object.php)，[PHP: 类与对象 - Manual](https://www.php.net/manual/zh/language.oop5.php)有更加丰富的内容。

### 命名空间
#### 概述
在 PHP 中，命名空间用来解决在编写类库或应用程序时创建可重用的代码如类或函数时碰到的两类问题：
1. 用户编写的代码与PHP内部的类/函数/常量或第三方类/函数/常量之间的名字冲突。
2. 为很长的标识符名称(通常是为了缓解第一类问题而定义的)创建一个别名（或简短）的名称，提高源代码的可读性。

#### 定义命名空间
虽然任意合法的 PHP 代码都可以包含在命名空间中，但只有以下类型的代码受命名空间的影响，它们是：类（包括抽象类和 trait）、接口、函数和常量。命名空间通过关键字 `namespace` 来声明。如果一个文件中包含命名空间，它必须在其它所有代码之前声明命名空间，除了一个以外：[declare](https://www.php.net/manual/zh/control-structures.declare.php)关键字。
```php
<?php  
namespace MyProject;  
const CONNECT_OK = 1;  
class Connection { /* ... */ }  
function connect() { /* ... */ }  
?>
```
> **注意**: 完全限定名称（就是以反斜杠开头的名称）不能用于命名空间的声明。 因为该结构会解析成相对命名空间表达式。

在声明命名空间之前唯一合法的代码是用于定义源文件编码方式的 `declare` 语句。另外，所有非 PHP 代码包括空白符都不能出现在命名空间的声明之前。

#### 定义子命名空间
与目录和文件的关系很象，PHP 命名空间也允许指定层次化的命名空间的名称。因此，命名空间的名字可以使用分层次的方式定义：
```php
<?php  
namespace MyProject\Sub\Level;  
  
const CONNECT_OK = 1;  
class Connection { /* ... */ }  
function connect() { /* ... */ }  
  
?>
```

#### 在同一个文件中定义多个命名空间
在单个文件定义多个命名空间时，建议使用大括号来包括一个命名空间的代码。
```php
namespace MyProject {  
  
const CONNECT_OK = 1;  
class Connection { /* ... */ }  
function connect() { /* ... */ }  
}  
  
namespace AnotherProject {  
  
const CONNECT_OK = 1;  
class Connection { /* ... */ }  
function connect() { /* ... */ }  
}
```
在实际的编程实践中，非常不提倡在同一个文件中定义多个命名空间。这种方式的主要用于将多个 PHP 脚本合并在同一个文件中。
```php
<?php  
declare(encoding='UTF-8');  
namespace MyProject {  
  
const CONNECT_OK = 1;  
class Connection { /* ... */ }  
function connect() { /* ... */ }  
}  
  
namespace { // 全局代码  
session_start();  
$a = MyProject\connect();  
echo MyProject\Connection::start();  
}  
?>
```

#### 使用命名空间：基础
`file.php`
```php
<?php  
namespace Foo\Bar\subnamespace;  
  
const FOO = 1;  
function foo() {}  
class foo  
{  
static function staticmethod() {}  
}  
?>
```
`file2.php`
```php
<?php  
namespace Foo\Bar;  
include 'file1.php';  
  
const FOO = 2;  
function foo() {}  
class foo  
{  
static function staticmethod() {}  
}  
  
/* 非限定名称 */  
foo(); // 解析为函数 Foo\Bar\foo  
foo::staticmethod(); // 解析为类 Foo\Bar\foo 的静态方法 staticmethod  
echo FOO; // 解析为常量 Foo\Bar\FOO  
  
/* 限定名称 */  
subnamespace\foo(); // 解析为函数 Foo\Bar\subnamespace\foo  
subnamespace\foo::staticmethod(); // 解析为类 Foo\Bar\subnamespace\foo,  
// 以及类的方法 staticmethod  
echo subnamespace\FOO; // 解析为常量 Foo\Bar\subnamespace\FOO  
  
/* 完全限定名称 */  
\Foo\Bar\foo(); // 解析为函数 Foo\Bar\foo  
\Foo\Bar\foo::staticmethod(); // 解析为类 Foo\Bar\foo, 以及类的方法 staticmethod  
echo \Foo\Bar\FOO; // 解析为常量 Foo\Bar\FOO  
?>
```

#### 使用命名空间：别名/导入
允许通过别名引用或导入外部的完全限定名称，是命名空间的一个重要特征。这有点类似于在类 unix 文件系统中可以创建对其它的文件或目录的符号连接。PHP 可以为这些项目导入或设置别名： 常量、函数、类、接口、trait、枚举和命名空间。
```php
<?php  
namespace foo;  
use My\Full\Classname as Another;   // 别名
  
// 下面的例子与 use My\Full\NSname as NSname 相同  
use My\Full\NSname;  

// use My\Full\Classname as Another, My\Full\NSname; 上面两行代码可以一行导入
  
// 导入一个全局类  
use ArrayObject;  
  
// 导入函数  
use function My\Full\functionName;  
  
// 为函数设置别名  
use function My\Full\functionName as func;  
  
// 导入常量  
use const My\Full\CONSTANT;  
  
$obj = new namespace\Another; // 实例化 foo\Another 对象  
$obj = new Another; // 实例化 My\Full\Classname　对象  
NSname\subns\func(); // 调用函数 My\Full\NSname\subns\func  
$a = new ArrayObject(array(1)); // 实例化 ArrayObject 对象  
// 如果不使用 "use \ArrayObject" ，则实例化一个 foo\ArrayObject 对象  
func(); // 调用函数 My\Full\functionName  
echo CONSTANT; // 输出 My\Full\CONSTANT 的值  
?>
```
`use` 关键词必须在文件最外层范围 （全局作用域）或在命名空间声明内。 由于导入发生在编译时，而不是运行时，所以不能放入块作用域。

### 枚举
更详细的枚举介绍：[PHP: 枚举 - Manual](https://www.php.net/manual/zh/language.enumerations.php)
```php
enum Suit
{
    case Hearts;
    case Diamonds;
    case Clubs;
    case Spades;
}
$val = Suit::Diamonds;
```

### 错误

```php
try{
    $a = 1/0;
}catch(DivisionByZeroError $e){
    echo "divsion by 0";
}finally{
    echo "catch finally";
}
```

[PHP: 预定义异常 - Manual](https://www.php.net/manual/zh/reserved.exceptions.php)

SPL标准异常：[PHP: 异常 - Manual](https://www.php.net/manual/zh/spl.exceptions.php)



### 纤程



纤程（fiber）表示一组有完整栈、可中断的功能。 纤程可以在调用堆栈中的任何位置被挂起，在纤程内暂停执行，直到稍后恢复。

纤程可以暂停整个执行堆栈，所以该函数的直接调用者不需要改变调用这个函数的方式。

你可以在调用堆栈的任意地方使用 [Fiber::suspend()](https://www.php.net/manual/zh/fiber.suspend.php) 中断执行（也就是说，[Fiber::suspend()](https://www.php.net/manual/zh/fiber.suspend.php) 的调用位置可以在一个深度嵌套的函数中，甚至可以不存在）。

与无栈的 [Generator](https://www.php.net/manual/zh/class.generator.php) 不同, 每一个 [Fiber](https://www.php.net/manual/zh/class.fiber.php) 拥有自己的调用栈，并允许在一个深度前度的函数调用中将它们暂停。 声明了中断（interruption）点的函数（即调用 [Fiber::suspend()](https://www.php.net/manual/zh/fiber.suspend.php)） 不需要改变自己的返回类型，不像使用 [yield](https://www.php.net/manual/zh/language.generators.syntax.php#control-structures.yield) 一样需要返回一个 [Generator](https://www.php.net/manual/zh/class.generator.php) 实例。

纤程可以在任意函数调用中被暂停，包括那些在 PHP VM 中被调用的函数。 例如被用于 [array_map()](https://www.php.net/manual/zh/function.array-map.php) 的函数或者提供 [Iterator](https://www.php.net/manual/zh/class.iterator.php) 对象以被 [foreach](https://www.php.net/manual/zh/control-structures.foreach.php) 调用的方法。

纤程一旦被暂停，可以使用 [Fiber::resume()](https://www.php.net/manual/zh/fiber.resume.php) 传递任意值、或者使用 [Fiber::throw()](https://www.php.net/manual/zh/fiber.throw.php) 向纤程抛出一个异常以恢复运行。这个值或者异常将会在 [Fiber::suspend()](https://www.php.net/manual/zh/fiber.suspend.php) 中被返回（抛出）。

> **注意**: 由于当前限制，不能在对象的析构函数中打开或关闭纤程。

```php
$fiber = new Fiber(function (): void {
    $parm = Fiber::suspend('fiber');
    echo "Value used to resume fiber: ", $parm, PHP_EOL;
});

$value = $fiber->start();
echo "Value from fiber suspending: ", $value, PHP_EOL;
$fiber->resume('test');
```

### 生成器总览
生成器提供了一种更容易的方法来实现简单的[对象迭代](https://www.php.net/manual/zh/language.oop5.iterations.php)，相比较定义类实现 [Iterator](https://www.php.net/manual/zh/class.iterator.php) 接口的方式，性能开销和复杂性大大降低。生成器允许你在 [foreach](https://www.php.net/manual/zh/control-structures.foreach.php) 代码块中写代码来迭代一组数据而不需要在内存中创建一个数组, 可以写一个生成器函数，就像一个普通的自定义[函数](https://www.php.net/manual/zh/functions.user-defined.php)一样, 和普通函数只[返回](https://www.php.net/manual/zh/functions.returning-values.php)一次不同的是, 生成器可以根据需要 [yield](https://www.php.net/manual/zh/language.generators.syntax.php#control-structures.yield) 多次，以便生成需要迭代的值。
一个简单的例子就是使用生成器来重新实现 [range()](https://www.php.net/manual/zh/function.range.php) 函数。 标准的 [range()](https://www.php.net/manual/zh/function.range.php) 函数需要在内存中生成一个数组包含每一个在它范围内的值，然后返回该数组, 结果就是会产生多个很大的数组。 比如，调用`range(0, 1000000)`将导致内存占用超过 100 MB。
作为替代，可以实现一个`xrange()`生成器，只需要足够的内存来创建 [Iterator](https://www.php.net/manual/zh/class.iterator.php) 对象并在内部跟踪生成器的当前状态，这样只需要不到1K字节的内存。
```php
function xrange($start, $limit, $step = 1) {  
    if ($start <= $limit) {  
        if ($step <= 0) {  
            throw new LogicException('Step must be positive');  
        }
        for ($i = $start; $i <= $limit; $i += $step) {  
            yield $i;  
        }  
    }
    else {  
        if ($step >= 0) {  
            throw new LogicException('Step must be negative');  
        }  
        for ($i = $start; $i >= $limit; $i += $step) {  
            yield $i;  
        }  
    }  
}
echo 'Single digit odd numbers from range(): ';  
foreach (range(1, 9, 2) as $number) {  
    echo "$number ";  
}  
echo "\n";  
echo 'Single digit odd numbers from xrange(): ';  
foreach (xrange(1, 9, 2) as $number) {  
    echo "$number ";  
}
```

#### 生成器语法
生成器函数看起来像普通函数——不同的是普通函数返回一个值，而生成器可以 [yield](https://www.php.net/manual/zh/language.generators.syntax.php#control-structures.yield) 生成多个想要的值。 任何包含 [yield](https://www.php.net/manual/zh/language.generators.syntax.php#control-structures.yield) 的函数都是一个生成器函数。
当一个生成器被调用的时候，它返回一个可以被遍历的对象.当你遍历这个对象的时候(例如通过一个[foreach](https://www.php.net/manual/zh/control-structures.foreach.php)循环)，PHP 将会在每次需要值的时候调用对象的遍历方法，并在产生一个值之后保存生成器的状态，这样它就可以在需要产生下一个值的时候恢复调用状态。
一旦不再需要产生更多的值，生成器可以简单退出，而调用生成器的代码还可以继续执行，就像一个数组已经被遍历完了。
除了生成一个值，还可以指定键名来生成值
```php
function input_parser($input) {  
	foreach (explode("\n", $input) as $line) {  
		$fields = explode(';', $line);  
		$id = array_shift($fields);   
		yield $id => $fields;  
	}  
}
// 调用时
foreach (input_parser($input) as $id => $fields){
//...
}
```
生成函数可以像使用值一样来使用引用生成。这个和[从函数返回一个引用](https://www.php.net/manual/zh/functions.returning-values.php)一样：通过在函数名前面加一个引用符号。
```php
function &gen_reference() {  
	$value = 3;  
	while ($value > 0) {  
		yield $value;  
	}  
}  
/*  
* 我们可以在循环中修改 $number 的值，而生成器是使用的引用值来生成，所以 gen_reference() 内部的 $value 值也会跟着变化。  
*/
foreach (gen_reference() as &$number) {  
	echo (--$number).'... ';  
}
```

生成器委托允许使用`yield from`关键字从另外一个生成器、 [Traversable](https://www.php.net/manual/zh/class.traversable.php) 对象、array 通过生成值。 外部生成器将从内部生成器、object、array 中生成所有的值，直到它们不再有效， 之后将在外部生成器中继续执行。

#### 生成器与Iterator对象的比较
生成器最主要的优点是简洁。和实现一个 [Iterator](https://www.php.net/manual/zh/class.iterator.php) 类相较而言， 同样的功能，用生成器可以编写更少的代码，可读性也更强。 举例，下面的类和函数是相等的：

```php
<?php
function getLinesFromFile($fileName) {
    if (!$fileHandle = fopen($fileName, 'r')) {
        return;
    }

    while (false !== $line = fgets($fileHandle)) {
        yield $line;
    }

    fclose($fileHandle);
}

// 比较下...

class LineIterator implements Iterator {
    protected $fileHandle;

    protected $line;
    protected $i;

    public function __construct($fileName) {
        if (!$this->fileHandle = fopen($fileName, 'r')) {
            throw new RuntimeException('Couldn\'t open file "' . $fileName . '"');
        }
    }

    public function rewind() {
        fseek($this->fileHandle, 0);
        $this->line = fgets($this->fileHandle);
        $this->i = 0;
    }

    public function valid() {
        return false !== $this->line;
    }

    public function current() {
        return $this->line;
    }

    public function key() {
        return $this->i;
    }

    public function next() {
        if (false !== $this->line) {
            $this->line = fgets($this->fileHandle);
            $this->i++;
        }
    }
    
    public function __destruct() {
        fclose($this->fileHandle);
    }
}
?>
```

不过，这也付出了灵活性的代价： 生成器是一个只能向前的迭代器，一旦开始遍历就无法后退。 意思也就是说，同样的生成器无法遍历多次：要么再次调用生成器函数，重新生成后再遍历。

### 注解
看起来是比较高级的用法

### 引用的解释
#### 取消引用
```php
$a = 1;  
$b =& $a;  
unset($a);
```

### 预定义变量
- [超全局变量](https://www.php.net/manual/zh/language.variables.superglobals.php) — 在全部作用域中始终可用的内置变量
- [$GLOBALS](https://www.php.net/manual/zh/reserved.variables.globals.php) — 引用全局作用域中可用的全部变量
- [$_SERVER](https://www.php.net/manual/zh/reserved.variables.server.php) — 服务器和执行环境信息
- [$_GET](https://www.php.net/manual/zh/reserved.variables.get.php) — HTTP GET 变量
- [$_POST](https://www.php.net/manual/zh/reserved.variables.post.php) — HTTP POST 变量
- [$_FILES](https://www.php.net/manual/zh/reserved.variables.files.php) — HTTP 文件上传变量
- [$_REQUEST](https://www.php.net/manual/zh/reserved.variables.request.php) — HTTP Request 变量
- [$_SESSION](https://www.php.net/manual/zh/reserved.variables.session.php) — Session 变量
- [$_ENV](https://www.php.net/manual/zh/reserved.variables.environment.php) — 环境变量
- [$_COOKIE](https://www.php.net/manual/zh/reserved.variables.cookies.php) — HTTP Cookies
- [$php_errormsg](https://www.php.net/manual/zh/reserved.variables.phperrormsg.php) — 前一个错误信息
- [$http_response_header](https://www.php.net/manual/zh/reserved.variables.httpresponseheader.php) — HTTP 响应头
- [$argc](https://www.php.net/manual/zh/reserved.variables.argc.php) — 传递给脚本的参数数目
- [$argv](https://www.php.net/manual/zh/reserved.variables.argv.php) — 传递给脚本的参数数组



### 预定义接口和类

- [Traversable](https://www.php.net/manual/zh/class.traversable.php) — 检测一个类是否可以使用 [foreach](https://www.php.net/manual/zh/control-structures.foreach.php) 进行遍历的接口。
- [Iterator](https://www.php.net/manual/zh/class.iterator.php) — 可在内部迭代自己的外部迭代器或类的接口。
- [IteratorAggregate](https://www.php.net/manual/zh/class.iteratoraggregate.php) — 创建外部迭代器的接口。
- [InternalIterator](https://www.php.net/manual/zh/class.internaliterator.php) — 类来简化为内部类实现 IteratorAgge 的工作。
- [Throwable](https://www.php.net/manual/zh/class.throwable.php) — 能被 [`throw`](https://www.php.net/manual/zh/language.exceptions.php) 语句抛出的最基本的接口
- [ArrayAccess](https://www.php.net/manual/zh/class.arrayaccess.php) — 提供像访问数组一样访问对象的能力的接口。
- [Serializable](https://www.php.net/manual/zh/class.serializable.php) — 自定义序列化的接口。
- [Closure](https://www.php.net/manual/zh/class.closure.php) — 用于代表 [匿名函数](https://www.php.net/manual/zh/functions.anonymous.php) 的类.
- [stdClass](https://www.php.net/manual/zh/class.stdclass.php) — 具有动态属性的通用空类。
- [Generator](https://www.php.net/manual/zh/class.generator.php) — **Generator** 对象是从 [generators](https://www.php.net/manual/zh/language.generators.php)返回的.
- [Fiber](https://www.php.net/manual/zh/class.fiber.php) — 纤程
- [WeakReference](https://www.php.net/manual/zh/class.weakreference.php) — 弱引用
- [WeakMap](https://www.php.net/manual/zh/class.weakmap.php) — 将对象作为 key 来访问的 map
- [Stringable](https://www.php.net/manual/zh/class.stringable.php) — 表示拥有 [__toString()](https://www.php.net/manual/zh/language.oop5.magic.php#object.tostring) 方法的类
- [UnitEnum](https://www.php.net/manual/zh/class.unitenum.php) — 引擎会自动应用 **UnitEnum** 接口到所有枚举
- [BackedEnum](https://www.php.net/manual/zh/class.backedenum.php) — 引擎会自动应用 **BackedEnum** 接口到回退枚举
- [SensitiveParameterValue](https://www.php.net/manual/zh/class.sensitiveparametervalue.php) — 敏感参数值类允许包装敏感值，以防止意外暴露。



### 上下文（Context）选项和参数
PHP 提供了多种上下文选项和参数，可用于所有的文件系统或数据流封装协议。上下文（Context）由 [stream_context_create()](https://www.php.net/manual/zh/function.stream-context-create.php) 创建。选项可通过 [stream_context_set_option()](https://www.php.net/manual/zh/function.stream-context-set-option.php) 设置，参数可通过 [stream_context_set_params()](https://www.php.net/manual/zh/function.stream-context-set-params.php) 设置。

- [套接字上下文选项](https://www.php.net/manual/zh/context.socket.php) — 套接字上下文选项列表
- [HTTP context 选项](https://www.php.net/manual/zh/context.http.php) — HTTP context 的选项列表
- [FTP 上下文选项](https://www.php.net/manual/zh/context.ftp.php) — FTP 上下文选项列表
- [SSL 上下文选项](https://www.php.net/manual/zh/context.ssl.php) — SSL 上下文选项清单
- [Phar 上下文（context）选项](https://www.php.net/manual/zh/context.phar.php) — Phar 上下文（context）选项列表
- [Context 参数](https://www.php.net/manual/zh/context.params.php) — Context 参数列表
- [Zip 上下文选项](https://www.php.net/manual/zh/context.zip.php) — Zip 上下文选项列表
- [Zlib 上下文选项](https://www.php.net/manual/zh/context.zlib.php) — Zlib 上下文选项列表



### 支持的协议和封装协议 

PHP 带有很多内置 URL 风格的封装协议，可用于类似 [fopen()](https://www.php.net/manual/zh/function.fopen.php)、 [copy()](https://www.php.net/manual/zh/function.copy.php)、 [file_exists()](https://www.php.net/manual/zh/function.file-exists.php) 和 [filesize()](https://www.php.net/manual/zh/function.filesize.php) 的文件系统函数。 除了这些封装协议，还能通过 [stream_wrapper_register()](https://www.php.net/manual/zh/function.stream-wrapper-register.php) 来注册自定义的封装协议。

- [file://](https://www.php.net/manual/zh/wrappers.file.php) — 访问本地文件系统
- [http://](https://www.php.net/manual/zh/wrappers.http.php) — 访问 HTTP(s) 网址
- [ftp://](https://www.php.net/manual/zh/wrappers.ftp.php) — 访问 FTP(s) URLs
- [php://](https://www.php.net/manual/zh/wrappers.php.php) — 访问各个输入/输出流（I/O streams）
- [zlib://](https://www.php.net/manual/zh/wrappers.compression.php) — 压缩流
- [data://](https://www.php.net/manual/zh/wrappers.data.php) — 数据（RFC 2397）
- [glob://](https://www.php.net/manual/zh/wrappers.glob.php) — 查找匹配的文件路径模式
- [phar://](https://www.php.net/manual/zh/wrappers.phar.php) — PHP 归档
- [ssh2://](https://www.php.net/manual/zh/wrappers.ssh2.php) — 安全外壳协议 2
- [rar://](https://www.php.net/manual/zh/wrappers.rar.php) — RAR
- [ogg://](https://www.php.net/manual/zh/wrappers.audio.php) — 音频流
- [expect://](https://www.php.net/manual/zh/wrappers.expect.php) — 处理交互式的流



## PHP实战

### 连接Mysql

在`php.ini`中加上

```ini
extension=php_pdo_mysql.dll
```

php查询Mysql中的数据库

```php
$pdo = new PDO("mysql:host=localhost;dbname=learn", 'root', 'XMJsql123456');
$pdo->setAttribute(PDO::MYSQL_ATTR_USE_BUFFERED_QUERY, false);
$unbufferedResult = $pdo->query("SELECT cust_name FROM customers");
foreach ($unbufferedResult as $row) {
    echo $row['cust_name'] . PHP_EOL;
}
```

另外一种方案

在`php.ini`中加上

```ini
extension=php_mysqli.dll
```

php测试Mysql的连接

```php
$servername = "localhost";
$username = "root";
$password = "XMJsql123456";
$conn = new mysqli($servername, $username, $password);
if ($conn->connect_error) {
    die("连接失败: " . $conn->connect_error);
} 
echo "连接成功";
```

