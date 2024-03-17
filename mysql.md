

> mysql的用户名：root，用户密码：XMJsql123456

## 基本操作

### 启动或停止mysql服务

需要以**管理员模式**启动cmd

```sh
net start mysql80
net stop mysql80
```
**注意后续一切操作都要先启动mysql服务**


### mysql命令行

1. 在开始菜单中选择MySQL 8.0 Command Line Client - Unicode（Unicode表示支持中文字符），并输入密码。
2. 将D:\Mysql\Server\server添加进环境变量，然后可以在cmd中输入

```shell
mysql [-h 127.0.0.1] [-P 3306] -u root -p
```

### 使用图形化工具
打开MySQL Workbench

![image-20231213144626208](https://img2.imgtp.com/2024/03/08/I6F3H7v1.png)

通过create Schema创建新的schema（数据库），右键schema名选择`Set as Default Schema`设置默认Schema，之后编写或导入sql语句即可向当前默认的schema中添加表。

**mysql的基本概念**

mysql数据库是关系型数据库（建立在关系模型基础上，有多张相互拼接的二维表组成的数据库）。

mysql的数据模型：通过DBMS引擎来操作数据库中的表。



### 从 MySql Workbench 中导出数据表的 sql 文件 

[在MySQL workbench 中导出sql脚本文件_workbench导出sql语句-CSDN博客](https://blog.csdn.net/qq_46186167/article/details/115837638)

菜单栏选择 Server，Data Export 即可打开导出界面。在导出界面中可以选择 export to self-contained file（可以将一个 schema 中的所有表导出为一个 sql 文件）。





## SQL语句

**注释**

```mysql
-- 需要与--隔一个空格
#不需要隔一个空格
/*
这是多行注释
*/
```



### 表的查询、创建与删除

**查询**

查询所有数据库

```sql
show databases;
```

查询当前数据库

```mysql
select database();
```

**创建数据库**

```mysql
create database [if not exists] 数据库名 [default charset 字符集] [collate 排序规则];
```

**删除数据库**

```mysql
drop database [if exists] 数据库名;
```

**使用**

```mysql
use 数据库名;
```

**获得一个数据库内的表的列**

```mysql
SHOW TABLES;
```



**创建表**

```mysql
create table people(
id  int Not null auto_increment,	-- id自增
survived bool not null,
pclass TINYINT null,
sex bool  null,
age TINYINT null,
primary key (id)
) engine=InnoDB;

```

**主键**可以是多个列，如primary key (id, name)

除了主键，还有**外键** FOREIGN KEY (name) REFERENCES 另外一个表名(另外一个表中的列)

详见[【数据库】彻底理解外键的作用_code bean的博客-CSDN博客](https://blog.csdn.net/songhuangong123/article/details/127194673)和

[SQL FOREIGN KEY 约束 | 菜鸟教程 (runoob.com)](https://www.runoob.com/sql/sql-foreignkey.html)

数据类型方面，可以指定字符串长度如char(10)，指定精度如decimal(8,2)指小数为2位，整数为8-2=6位。

对于引擎(engine)：

1. InnoDB是一个可靠的事务处理引擎，它不支持全文本搜索；

2. MEMORY在功能等同于MyISAM，但由于数据存储在内存（不是磁盘）中，速度很快（特别适合于临时表）； 
3. MyISAM是一个性能极高的引擎，它支持全文本搜索，但不支持事务处理。

**描述表**

```mysql
desc 表名;
```

**删除表**

```mysql
drop table 表名;
```

**重命名表**

```mysql
rename table peoplenew to people2;
```


**修改表**

```mysql
alter table 表名  -- 注意没有分号，继续输入
add 列名 类型;	-- 添加列
drop column 列名; -- 删除列
```

> 复杂的表结构更改一般需要手动删除过程，它涉及以下步骤： 
>
> 1. 用新的列布局创建一个新表；
> 2. 使用INSERT SELECT语句，从旧表复制数据到新表。如果有必要，可使用转换函数和计算字段； 
> 3. 检验包含所需数据的新表； 
> 4. 重命名旧表（如果确定，可以删除它）； 
> 5. 用旧表原来的名字重命名新表； 
> 6. 根据需要，重新创建触发器、存储过程、索引和外键。
>
> 小心使用ALTER TABLE使用ALTER TABLE要极为小心，应该在进行改动前做一个完整的备份（模式和数据的备份）。数据库表的更改不能撤销，如果增加了不需要的列，可能不能删除它们。类似地，如果删除了不应该删除的列，可能会丢失该列中的所有数据。



### 检索数据

#### 检索列

**从表中查看列名对应的列**

```mysql
select 列名 from 表名;
select 列名1, 列名2 from 表名; 
```

**检索所有列**

```mysql
select * from people;
```


#### 检索行

**检索不同的值**

```mysql
select distinct pclass from people;
```


#### 限制结果行数

**指定行数**

```mysql
select name from people 
limit 5;
```

**指定开始行和行数**

```mysql
select name from people 
limit 5, 5;
```


#### 完全限定表名

```mysql
select people.name from titanic.people;
```


### 修改数据

#### 插入数据

**一般写法**

```mysql
insert into people 
value
(null, false, 3, true, 22,"tom");   -- 如果第一列是自增的id，直接给null即可
```

**更加安全的写法**

```mysql
insert into people
(survived, pclass, sex, age, name) 
value
(false, 3, true, 22,"tom");  
```

**插入多条数据**

```mysql
insert into people
(survived, pclass, sex, age, name)
values
(false, 1, true, 23,"jack"),
(true, 2, false, 20, "merry");
```

**从另外一个表选择一些插入新表**

```mysql
insert into peoplenew
(survived, pclass, sex, age)
select survived, pclass, sex, age from people;
```



#### 更新和删除数据

**更新数据**

> 不加分号时需要在行尾加空格

```mysql
update people 
set age = 25 
where name = "jack";	-- 告诉应该更新哪一行
```

**更新多个列**

```mysql
update people 
set age = 25,
pclass = 2
where name = "jack";
```

**IGNORE关键字**：如果用 UPDATE 语句更新多行，并且在更新这些行中的一行或多行时出一个错误，则整个 UPDATE 操作被取消（错误发生前更新的所有行被恢复到它们原来的值）。为即使是发生错误，也继续进行更新，可使用 IGNORE 关键字：`UPDATE IGNORE people`


**更新列名**

```mysql
alter table people2
rename column pclass to class;
```



**为了删除某个列的值，可设置它为NULL（假如表定义允许NULL值）**

```mysql
update people 
set name  = NULL
where id = 1;
```



**删除行**

```mysql
delete from people 
where id = 1;
```

> DELETE不需要列名或通配符，DELETE删除整行而不是删除列。为了删除指定的列，请使用UPDATE语句。



**删除所有行**

相当于删除原来的表，新建了一个空表

```mysql
TRUNCATE TABLE 表名
```



> 1. 除非确实打算更新和删除每一行，否则绝对不要使用不带WHERE子句的UPDATE或DELETE语句。
> 2. 保证每个表都有主键，尽可能像WHERE子句那样使用它（可以指定各主键、多个值或值的范围）。 
> 3. 在对UPDATE或DELETE语句使用WHERE子句前，应该先用SELECT进行测试，保证它过滤的是正确的记录，以防编写的WHERE子句不正确。 
> 4. 使用强制实施引用完整性的数据库，这样MySQL将不允许删除具有与其他表相关联的数据的行。



### 排序检索数据

#### 排序数据

**单列排序**

从小到大排

```mysql
select blen from sp 
order by blen;
```

**多列排序**

```mysql
select species, blen, flen from sp 
order by blen, flen;
```

**指定排序方向**

使用desc关键字，从大到小排

```mysql
select species, blen from sp 
order by blen desc;
```

多个列排序

```mysql
select species, blen from sp 
order by blen desc, flen;
```

DESC关键字只应用到直接位于其前面的列名。如果想在多个列上进行降序排序，必须对每个列指定DESC关键字。

#### 找出最大

```mysql
select species, blen from sp 
order by blen desc 
limit 1;
```

在给出ORDER BY子句时，应该保证它位于FROM子句之后。如果使用LIMIT，它必须位于ORDER BY 之后。

### 过滤数据

基本句式

```mysql
select ... from ... 
where 子句
```

在同时使用ORDER BY和WHERE子句时，应该让ORDER BY位于WHERE之后，否则将会产生错误

#### where子句操作符

| 操作符          | 说明                 |
| --------------- | -------------------- |
| =               | 等于                 |
| <>              | 不等于               |
| !=              | 不等于               |
| <               | 小于                 |
| <=              | 小于等于             |
| >               | 大于                 |
| >=              | 大于等于             |
| between a and b | 在指定两个值a和b之间 |

```mysql
select blen from sp 
where blen between 40 and 45;
```



#### 空值检查

```mysql
select blen from sp 
where blen is NULL;
```

这条语句返回所有为空的blen



#### 组合where子句

sql中有and和or操作符，为了避免优先级的问题，可以加上括号来标识，如

```mysql
select prod_name, prod_price 
from products 
where (vend_id = 1002 OR vend_id = 1003) AND prod_price >= 10;
```



IN操作符用来指定条件范围，范围中的每个条件都可以进行匹配。

```mysql
SELECT prod_name，prod_price FROM products
WHERE vend_id IN (1002,1003) ORDER BY prod_name;
```



NOT操作符用来否定它之后所跟的任何条件。

```mysql
select blen from sp 
where blen is not null;
```



#### 通配符

**百分号（%）通配符**

%表示任何字符出现任意次数，为了找出所有以词 jet 起头的产品，可使用以下 SELECT 语句：

```mysql
select prod_id, prod_name 
from products 
where prod_name like "jet%";
```

在执行这条子句时，将检索任意以 jet 起头的词。%告诉 MySQL 接受 jet 之后的任意字符，不管它有多少字符。



通配符可在搜索模式中任意位置使用，并且可以使用多个通配符。

```
SELECT prod_id, prod_name FROM products 
WHERE prod_name LIKE  '%anvil%';
```

搜索模式'%anvil%'表示匹配任何位置包含文本anvil的值，而不论它之前或之后出现什么字符。

's%e'表示匹配以s起头以e结尾的所有产品；

%还能匹配0个字符。%代表搜索模式中给定位置的0个、1个或多个字符。

尾空格可能会干扰通配符匹配。例如，在保存词 anvil 时，如果它后面有一个或多个空格，则子句WHERE prod_name LIKE '%anvil'将不会匹配它们，因为在最后的 1 后有多余的字符。解决这个问题的一个简单的办法是在搜索模式最后附加一个%。一个更好的办法是使用函数去掉首尾空格。需要注意 % 通配符不能匹配NULL。



**下划线（_）通配符**

下划线的用途与%一样，但下划线只匹配单个字符而不是多个字符。

如"_ ton anvil"可以匹配到"1 ton anvil"，但不能匹配到".5 ton anvil"。

> 1. 不要过度使用通配符。如果其他操作符能达到相同的目的，应该使用其他操作符。
> 2. 在确实需要使用通配符时，除非绝对有必要，否则不要把它们用在搜索模式的开始处。把通配符置于搜索模式的开始处，搜索起来是最慢的。
> 3. 仔细注意通配符的位置。如果放错地方，可能不会返回想要的数据。



#### 正则表达式

**测试正则表达式**

```mysql
select 'hello' regexp '[0-9]';
```

1表示匹配，0表示不匹配

**基本字符匹配**

```mysql
select prod_name from products 
where prod_name REGEXP '1000' 
order by prod_name;
```



```mysql
where prod_name regexp '.000'
```

这里使用了正则表达式.000。.是正则表达式语言中一个特殊的字符。它表示匹配任意一个字符，因此，1000和2000都匹配且返回。



**LIKE与REGEXP的区别**

LIKE匹配整个列。如果被匹配的文本在列值中出现，LIKE将不会找到它，相应的行也不被返回（除非使用通配符）。而REGEXP在列值内进行匹配，如果被匹配的文本在列值中出现，REGEXP将会找到它，相应的行将被返回。这是一个非常重要的差别。

MySQL中的正则表达式匹配不区分大小写（即大写和小写都匹配）。为区分大小写，可使用BINARY关键字，如WHERE prod_name REGEXP BINARY 'JetPack .000'。



**进行OR匹配**

```mysql
select prod_name from products  
where prod_name REGEXP '1000|2000'  
order by prod_name;
```

正则表达式1000|2000。|为正则表达式的OR操作符。它表示匹配其中之一，因此1000和2000都匹配并返回。



**匹配几个字符之一**

正则表达式"[123] Ton"。[123]定义一组字符，它的意思是匹配1或2或3，因此，1 ton、2 ton和3 ton都可以匹配且返回（如果有的话）。

与"1|2|3 ton"的区别，"1|2|3 ton"会视为对'1'或 '2'或'3 ton'进行匹配。

[123]匹配字符1、2或3，但$[$^123$]$却匹配除这些字符外的任何东西。



**匹配范围**

[0-9]表示匹配0到9这十个数字

[a-z]匹配任意字母字符

```mysql
select prod_name FROM products 
where prod_name regexp '[1-5] Ton';
```

[1-5]定义了一个范围，这个表达式意思是匹配1到5，因此返回3个匹配行。由于5 ton匹配， 所以返回.5 ton。



**匹配特殊字符**

```mysql
SELECT vend_name FROM vendors
WHERE vend_name REGEXP '\\.'  
ORDER BY vend_name;
```

∖∖.匹配.，所以只检索出一行。这种处理就是所谓的转义（escaping），正则表达式内具有特殊意义的所有字符都必须以这种方式转义。这包括.、|、[]以及迄今为止使用过的其他特殊字符。



空白元字符

| 元字符 | 说明     |
| ------ | -------- |
| \\\f   | 换页     |
| \\\n   | 换行     |
| \\\r   | 回车     |
| \\\t   | 制表     |
| \\\v   | 纵向制表 |

**匹配字符类**

| 类         | 说明                                                   |
| ---------- | ------------------------------------------------------ |
| [:alnum:]  | 任意字母和数字（同[a-zA-Z0-9]）                        |
| [:alpha:]  | 任意字符（同[a-zA-Z）                                  |
| [:blank:]  | 空格和制表（同[\\\t]）                                 |
| [:cntrl:]  | ASCII控制字符（ASCII 0到31和127）                      |
| [:digit:]  | 任意数字（同[0-9]）                                    |
| [:graph:]  | 与[:print:]相同，但不包括空格                          |
| [:lower:]  | 任意小写字母（同[a-z]）                                |
| [:print:]  | 任意可打印字符                                         |
| [:punct:]  | 既不在[:alnum:]又不在[:cntrl:]中的任意字符             |
| [:space:]  | 包括空格在内的任意空白字符（同[\\\f\\\n\\\r\\\t\\\v]） |
| [:upper:]  | 任意大写字母（同[A-Z]）                                |
| [:xdigit:] | 任意十六进制数字（同[a-fA-F0-9]                        |

**匹配多个实例**

重复元字符

| 元字符 | 说明                         |
| ------ | ---------------------------- |
| *      | 0个或多个匹配                |
| +      | 1个或多个匹配（等于{1,}）    |
| ?      | 0个或1个匹配（等于{0,1}）    |
| {n}    | 指定数目的匹配               |
| {n,}   | 不少于指定数目的匹配         |
| {n,m}  | 匹配数目的范围（m不超过255） |



```mysql
select prod_name from products 
where prod_name regexp "\\([0-9] sticks?\\)";
```

正则表达式\\\\([0-9] sticks?\\\\)需要解说一下。"\\\\("匹配"("， [0-9]匹配任意数字（这个例子中为1和5），sticks? 匹配 stick 和 sticks（s后的?使s可选，因为?匹配它前面的任何字符的0次或1次出现），"\\\\)"匹配")"。没有?，匹配stick和sticks会非常困难。

正则表达式"[[:digit:]]{4}"表示匹配4位数字。



**定位符**

定位元字符

| 元字符  | 说明       |
| ------- | ---------- |
| ^       | 文本的开始 |
| $       | 文本的结尾 |
| [[:<:]] | 词的开始   |
| [[:>:]] | 词的结尾   |

**举例**：`^`匹配串的开始。因此，`^[0-9\\.]` 只在 . 或任意数字为串中第一个字符时才匹配它们。

**使 REGEXP 起类似 LIKE 的作用**，前面提到过，LIKE 和 REGEXP 的不同在于，LIKE 匹配整个串而 REGEXP 匹配子串。利用定位符，通过用 ^ 开始每个表达式，用 $ 结束每个表达式，可以使 REGEXP 的作用与 LIKE 一样。



### 数据的处理

#### 创建计算字段

字段（field）基本上与列（column）的意思相同，经常互换使用，不过数据库列一般称为列，而术语字段通常用在计算字段的连接上。

**拼接字段**

Mysql中使用concat()函数拼接两个列

```mysql
select concat(blen, ' (', flen, ')') 
from sp 
order by blen;
```

RTrim() 函数可以用于删除数据右边所有的空格；

LTrim() 函数可以用于删除数据左边所有的空格；

Trim() 函数去除数据左右两边的空格。

使用别名来对拼接后的列重新命名，关键字为 AS

```mysql
select concat(blen, ' (', flen, ')') as len2 
from sp 
order by blen;
```

**执行算术计算**

```mysql
select blen, flen, blen * flen as lens 
from sp 
where blen between 40 and 45;
```

+：加，-：减，*：乘，/：除。



#### 文本处理函数

| 函数        | 说明              |
| ----------- | ----------------- |
| Left()      | 返回串左边的字符  |
| Length()    | 返回串的长度      |
| Locate()    | 找出串的一个子串  |
| Lower()     | 将串转换成小写    |
| LTrim()     | 去掉串左边的空格  |
| Right()     | 返回串右边的字符  |
| RTrim()     | 返回串右边的字符  |
| Soundex()   | 返回串的SOUNDEX值 |
| SubString() | 返回子串的字符    |
| Upper()     | 将串转换成大写    |

对于 Soundex 函数，计算 SOUNDEX 值用于找到发音相似的但值不同的数据。

```mysql
select cust_name, cust_contact 
from customers 
where  Soundex(cust_contact) = Soundex("Y Lie");
```

这样可以找到读音类似的数据

```mysql
select soundex("Lie");	-- 结果为 L000
select soundex("Lee");	-- 结果为 L000
```



#### 日期和时间处理函数

| 函数          | 说明                           |
| ------------- | ------------------------------ |
| AddDate()     | 增加一个日期（天、周等）       |
| AddTime()     | 增加一个时间（时、分等）       |
| CurDate()     | 返回当前日期                   |
| CurTime()     | 返回当前时间                   |
| Date()        | 返回日期时间的日期部分         |
| DateDiff()    | 计算两个日期之差               |
| Date_Add()    | 高度灵活的日期运算函数         |
| Date_Format() | 返回一个格式化的日期或时间串   |
| Day()         | 返回一个日期的天数部分         |
| DayOfWeek()   | 对于一个日期，返回对应的星期几 |
| Hour()        | 返回一个时间的小时部分         |
| Minute()      | 返回一个时间的分钟部分         |
| Month()       | 返回一个日期的月份部分         |
| Now()         | 返回当前日期和时间             |
| Second()      | 返回一个时间的秒部分           |
| Time()        | 返回一个日期时间的时间部分     |
| Year()        | 返回一个日期的年份部分         |

当比较日期时，使用Date()函数如：

```mysql
select cust_id, order_num from orders 
where Date(order_date) = '2005-09-01';
```



#### 数值处理函数

| 函数   | 说明                    |
| ------ | ----------------------- |
| Abs()  | 返回绝对值              |
| Cos()  | 返回余弦                |
| Exp()  | 返回指数值              |
| Mod()  | 返回余数                |
| Pi()   | 返回圆周率              |
| Rand() | 返回一个[0,1]中的随机数 |
| Sin()  | 返回正弦                |
| Sqrt() | 返回平方根              |
| Tan()  | 返回正切                |



#### 聚集函数

| 函数    | 说明             |
| ------- | ---------------- |
| AVG()   | 返回某列的平均值 |
| COUNT() | 返回某列的行数   |
| MAX()   | 返回某列的最大值 |
| MIN()   | 返回某列的最小值 |
| SUM()   | 返回某列值之和   |

上述函数均忽略值为NULL的行，对于Count函数，如果使用Count(*)，则会对所有行（包括值为NULL的行）进行计数，如

```mysql
select count(*) from sp;
```



**聚集不同值**

使用distinct参数可以让聚集函数只聚集不同的数据，如

```mysql
select avg(distinct price) as avg_price from products 
where id = 1003; 
```



**组合聚集函数**

可能需要包含多个聚集函数，中间由逗号分隔。

```mysql
select min(blen), max(blen), avg(blen) from sp;
```



#### 创建分组

group by 列名

```mysql
select species, Count(*) as sp_num from specie 
group by species;
```

对species列进行分组并计算每组个数。

使用WITH ROLLUP关键字，可以得到每个分组以及每个分组汇总级别（针对每个分组）的值。如

```mysql
select id, count(*) as num 
from products 
group by id with rollup;
```



**过滤分组**

使用having子句来过滤分组，支持所有WHERE操作符，只是关键字有区别。

```mysql
SELECT cust_id，COUNT(*） AS orders FROM orders 
GROUP BY cust_id 
HAVING COUNT(*) >= 2;
```

可以这样理解：WHERE在数据分组前进行过滤，HAVING在数据分组后进行过滤。



**分组和排序**

虽然GROUP BY和ORDER BY经常完成相同的工作，但它们是非常不同的。（注意在 mysql8 中group by不再隐式排序，所以必须使用order by进行排序）。

| order by                                     | group by                                                 |
| -------------------------------------------- | -------------------------------------------------------- |
| 排序产生的输出                               | 分组行。但输出可能不是分组的顺序                         |
| 任意列都可以使用（甚至非选择的列也可以使用） | 只可能使用选择列或表达式列，而且必须使用每个选择列表达式 |
| 不一定需要                                   | 如果与聚集函数一起使用列（或表达式），则必须使用         |

一般在使用GROUP BY子句时，应该也给出ORDER BY子句。这是保证数据正确排序的唯一方法。千万不要仅依赖GROUP BY排序数据。

```mysql
SELECT order_num，SUM(quantity*item_price)  As ordertotal FROM orderitems 
GROUP BY order_num 
HAVING SUM(quantity*item_price) >= 50 
ORDER BY ordertotal;
```



**select 子句顺序**

| 子句     | 说明               | 是否必须使用           |
| -------- | ------------------ | ---------------------- |
| select   | 要返回的列或表达式 | 是                     |
| from     | 从中检索数据的表   | 仅在从表选择数据时使用 |
| where    | 行级过滤           | 否                     |
| group by | 分组说明           | 仅在按组计算聚集时使用 |
| having   | 组级过滤           | 否                     |
| order by | 输出排序顺序       | 否                     |
| limit    | 要检索的行数       | 否                     |



### 数据查询

#### 使用子查询

**作为计算字段使用子查询**

```mysql
SELECT cust_name, cust_state, 
(SELECT COUNT(*) FROM orders 
 WHERE orders.cust_id = customers.cust_id)  AS orders 
FROM customers
ORDER BY cust_name;
```



#### 联结表

**外键**：外键为某个表中的一列，它包含另一个表的主键值，定义了两个表之间的关系。

这样做的好处如下：

1. 供应商信息不重复，从而不浪费时间和空间；

2. 如果供应商信息变动，可以只更新vendors表中的单个记录，相 关表中的数据不用改动；

3. 由于数据无重复，显然数据是一致的，这使得处理数据更简单。

总之，关系数据可以有效地存储和方便地处理。因此，关系数据库的**可伸缩性**远比非关系数据库要好。

**可伸缩性**：能够适应不断增加的工作量而不失败。设计良好的数据库或应用程序称之为可伸缩性好（scale well）。



**创建联结**

```mysql
SELECT vend_name, prod_name, prod_price 
FROM vendors, products	-- 从两张表中查询数据
WHERE vendors.vend_id = products.vend_id 	-- 声明关联
ORDER BY vend_name, prod_name;
```

在引用的列可能出现二义性时，必须使用**完全限定列名**（用一个点分隔的表名和列名）。如果引用一个没有用表名限制的具有二义性的列名，MySQL将返回错误。

如果没有下面这句话，返回的是两张表的笛卡尔积，检索出的行的数目将是第一个表中的行数乘以第二个表中的行数。

```mysql
WHERE vendors.vend_id = products.vend_id
```

详见原书



**内部联结**

目前为止所用的联结称为等值联结（equijoin），它基于两个表之间的相等测试。这种联结也称为内部联结。其实，对于这种联结可以使用稍微不同的语法来明确指定联结的类型。

```mysql
select vend_name, prod_name, prod_price 
from vendors inner join products 
on vendors.vend_id = products.vend_id;
```



**联结多个表**

SQL对一条SELECT语句中可以联结的表的数目没有限制。创建联结的基本规则也相同，首先列出所有表，然后定义表之间的关系。

```mysql
SELECT prod_name, vend_name, prod_price, quantity FROM orderitems, products, vendors 
WHERE products.vend_id = vendors.vend_id 
AND orderitems.prod_id = products.prod_id 
AND order_num = 20005;
```

MySQL在运行时关联指定的每个表以处理联结。这种处理可能是非常耗费资源的，因此应该仔细，不要联结不必要的表。联结的表越多，性能下降越厉害。



#### 创建高级联结

迄今为止，我们使用的只是称为内部联结或等值联结（equijoin）的简单联结。现在来看3种其他联结，它们分别是自联结、自然联结和外部联结。

**自联结**

查找生产id是DTNTR的供货商生产的其它商品id。

```mysql
select p1.prod_id, p1.prod_name 
from products as p1,  products as p2 
where p1.vend_id = p2.vend_id 
and p2.prod_id = 'DTNTR';
```

该语句等同于

```mysql
SELECT prod_id, prod_name FROM products 
WHERE vend_id = ( SELECT vend_id 
				FROM products
				WHERE prod_id = 'DTNTR ');
```

自联结通常作为外部语句用来替代 从相同表中检索数据时使用的子查询语句。虽然最终的结果是相同的，但有时候处理联结远比处理子查询快得多。应该试一下两种方法，以确定哪一种的性能更好。



**自然联结**

无论何时对表进行联结，应该至少有一个列出现在不止一个表中（被联结的列）。标准的联结（前一章中介绍的内部联结）返回所有数据，甚至相同的列多次出现。自然联结排除多次出现，使每个列只返回一次。事实上，迄今为止我们建立的每个内部联结都是自然联结，很可能 我们永远都不会用到不是自然联结的内部联结。



**外部联结**

许多联结将一个表中的行与另一个表中的行相关联。但有时候会需要包含没有关联行的那些行。

```mysql
select customers.cust_id, orders.order_num 
from customers left outer join orders  
on customers.cust_id = orders.cust_id;
```

这条SELECT语句使用了关键字OUTER JOIN来指定联结的类型（而不是在WHERE子句中指定）。但是，与内部联结关联两个表中的行不同的是，外部联结还包括没有关联行的行。在使用OUTER JOIN语法时，必须使用RIGHT或LEFT关键字指定包括其所有行的表（RIGHT指出的是OUTER JOIN右边的表，而LEFT指出的是OUTER JOIN左边的表）。上面的例子使用LEFT OUTER JOIN从FROM子句的左边表（customers表）中选择所有行。为了从右边的表中选择所有行，应该使用RIGHT OUTER JOIN。



**使用带聚集函数的联结**

使用count函数检索所有客户及每个客户所下的订单数

```mysql
SELECT 	customers.cust_name,  
		customers.cust_id, 
		COUNT(orders.order_num)  AS num_ord 
FROM customers INNER JOIN orders 
ON customers.cust_id = orders.cust_id 
GROUP BY customers.cust_id;
```

使用INNER JOIN将 customers 和 orders 表互相关联。 GROUP BY 子句按客户分组数据，因此，函数调用 COUNT(orders.order_num) 对每个客户的订单计数，将它作为 num_ord 返回。



**使用联结和连接条件**

1. 注意所使用的联结类型。一般我们使用内部联结，但使用外部联结也是有效的。
2. 保证使用正确的联结条件，否则将返回不正确的数据。
3. 应该总是提供联结条件，否则会得出笛卡儿积。
4. 在一个联结中可以包含多个表，甚至对于每个联结可以采用不同的联结类型。虽然这样做是合法的，一般也很有用，但应该在一起测试它们前，分别测试每个联结。这将使故障排除更为简单。

#### 组合查询

**创建组合查询**

UNION关键字可以组合多条SQL查询，将这些结果组合成单个结果集。

```mysql
 select pi() union select rand();
```

UNION的一些规则：

1. UNION中的每个查询必须包含相同的列、表达式或聚集函数（不过各个列不需要以相同的次序列出）。
2. 列数据类型必须兼容：类型不必完全相同，但必须是DBMS可以隐含地转换的类型（例如，不同的数值类型或不同的日期类型）。

UNION会自动去除重复的行，如果想要返回所有匹配行，可以使用 UNION ALL。

SELECT语句的输出用ORDER BY子句排序。在用UNION组合查询时，只能使用一条 ORDER BY 子句，它必须出现在最后一条 SELECT 语句之后。对于结果集，不存在用一种方式排序一部分，而又用另一种方式排序另一部分的情况，因此不允许使用多条 ORDER BY 子句。



#### 全文本搜索

MyISAM引擎支持全文本搜索，而InnoDB不支持全文本搜索。

```mysql
CREATE TABLE productnotes(
note_id int NOT NULL  UTO_INCREMENT, 
prod_id char(10)  NOT NULL, 
note_date datetime NOT NULL, 
note_text text NULL, 
PRIMARY KEY(note_id), 
FULLTEXT (note_text)
) ENGINE=MyISAM;
```

这些列中有一个名为note_text的列，为了进行全文本搜索， MySQL根据子句 FULLTEXT(note_text) 的指示对它进行索引。这里的FULLTEXT索引单个列，如果需要也可以指定多个列。

**不要在导入数据时使用FULLTEXT**：更新索引要花时间，虽然不是很多，但毕竟要花时间。如果正在导入数据到一个新表，此时不应该启用FULLTEXT索引。应该首先导入所有数据，然后再修改表，定义FULLTEXT。这样有助于更快地导入数据（而且使索引数据的总时间小于在导入每行时分别进行索引所需的总时间）。

使用两个函数Match()和Against()执行全文本搜索，其中Match()指定被搜索的列，Against()指定要使用的搜索表达式。

```mysql
SELECT note_text FROM productnotes 
WHERE Match(note_text)  Against( 'rabbit' );
```

传递给Match()的值必须与FULLTEXT()定义中的相同。如果指定多个列，则必须列出它们（而且次序正确）。

除非使用BINARY方式，否则全文本搜索不区分大小写。

上面的搜索语句等同于

```mysql
SELECT note_text 
FROM productnotes 
WHERE note_text LIKE '%rabbit%';
```

但是两者返回结果可能不同，全文本搜索的一个重要部分就是对结果排序。具有较高等级的行先返回（因为这些行很可能是你真正想要的行）。

```mysql
select note_text, Match(note_text) Against("rabbit") as rank 
from productnotes;
```

这段语句会输出带有rabbit的text和对应的rank。



**使用查询扩展**

查询扩展用来设法放宽所返回的全文本搜索结果的范围。考虑下面的情况，你想找出所有提到anvils的注释。只有一个注释包含词anvils，但你还想找出可能与你的搜索有关的所有其他行，即使它们不包含词anvils。

这也是查询扩展的一项任务。在使用查询扩展时，MySQL对数据和索引进行两遍扫描来完成搜索：

1. 首先，进行一个基本的全文本搜索，找出与搜索条件匹配的所有行；

2. 其次，MySQL检查这些匹配行并选择所有有用的词（我们将会简要地解释MySQL如何断定什么有用，什么无用）。
3. 再其次，MySQL再次进行全文本搜索，这次不仅使用原来的条件，而且还使用所有有用的词。

```mysql
select note_text 
from productnotes 
where match(note_text) against('anvils' with query expansion);
```



**布尔文本搜索**

MySQL支持全文本搜索的另外一种形式，称为布尔方式（boolean mode）。以布尔方式，可以提供关于如下内容的细节：

1. 要匹配的词；
2. 要排斥的词（如果某行包含这个词，则不返回该行，即使它包含其他指定的词也是如此）；
3. 排列提示（指定某些词比其他词更重要，更重要的词等级更高）；
4. 表达式分组；
5. 另外一些内容。

布尔方式不同于迄今为止使用的全文本搜索语法的地方在于，即使没有定义FULLTEXT索引，也可以使用它。但这是一种非常缓慢的操作（其性能将随着数据量的增加而降低）。

```mysql
select note_text 
from productnotes 
where match(note_text) against("heavy" in boolean mode);
```

为了匹配包含heavy但不包含任意以rope开始的词的行，可以使用"heavy -rope*"。

**全文本布尔操作符**

| 布尔操作符 | 说明                                                         |
| ---------- | ------------------------------------------------------------ |
| +          | 包含，词必须存在                                             |
| -          | 排除，词必须不出现                                           |
| >          | 包含，而且增加等级值                                         |
| <          | 包含，且减少等级值                                           |
| ()         | 把词组成子表达式（允许这些子表达式作为一个组被包含、排除、排列等） |
| ~          | 取消一个词的排序值                                           |
| *          | 词尾的通配符                                                 |
| ""         | 词尾的通配符定义一个短语（与单个词的列表不一样，它匹配整个短语以便包含或排除这个短语） |

'+rabbit +bait'：包含词rabbit和bait

'rabbit bait'：包含词rabbit和bait中的至少一个

'"rabbit bait"'：包含短语"rabbit bait"

'>rabbit <carrot'：匹配rabbit和carrot，增加前者的等级，降低后者的等级。

'+safe +(<combination)'：搜索匹配词safe和combination，降低后者的等级。



**使用说明**

1. 在索引全文本数据时，短词被忽略且从索引中排除。短词定义为那些具有3个或3个以下字符的词（如果需要，这个数目可以更改）。
2. MySQL带有一个内建的非用词（stopword）列表，这些词在索引全文本数据时总是被忽略。如果需要，可以覆盖这个列表（请参阅MySQL文档以了解如何完成此工作）。
3. 许多词出现的频率很高，搜索它们没有用处（返回太多的结果）。因此，MySQL规定了一条50%规则，如果一个词出现在50%以上的行中，则将它作为一个非用词忽略。50%规则不用于IN BOOLEAN MODE。
4. 如果表中的行数少于3行，则全文本搜索不返回结果（因为每个词或者不出现，或者至少出现在50%的行中）。
5. 忽略词中的单引号，例如，don't索引为dont。 
6. 不具有词分隔符（包括日语和汉语）的语言不能恰当地返回全文本搜索结果。
7. 如前所述，仅在MyISAM数据库引擎中支持全文本搜索。

### 视图

```mysql
 select cust_name, cust_contact from customers, orders, orderitems 
 where customers.cust_id = orders.cust_id 
 and orderitems.order_num = orders.order_num 
 and prod_id = 'TNT2';
```

可以将上面的代码转成下面的代码：

```mysql
SELECT cust_name，cust_contact FROM productcustomers 
WHERE prod_id = 'TNT2';
```

这里的productcustomers便是一个视图，可以方便我们简化操作，重用SQL语句，使用表的组成部分而不是整个表；可以保护数据，可以给用户授予表的特定部分的访问权限而不是整个表的访问权限；更改数据格式和表示，视图可返回与底层表的表示和格式不同的数据。

因为视图不包含数据，所以每次使用视图时，都必须处理查询执行时所需的任一个检索。如果你用多个联结和过滤创建了复杂的视图或者嵌套了视图，可能会发现性能下降得很厉害。因此，在部署使用了大量视图的应用前，应该进行测试。

#### 创建视图

使用`create view`语句创建，

使用`SHOW CREATE VIEW 视图名;`来查看创建视图的语句

使用`drop view 视图名;`来删除视图

更新视图时，可以先用DROP再用CREATE，也可以直接用CREATE OR REPLACE VIEW。如果要更新的视图不存在，则第2条更新语句会创建一个视图；如果要更新的视图存在，则第2条更新语句会替换原有视图。

**创建视图**

```mysql
create view productcustomers as 
select cust_name, cust_contact, prod_id 
from customers, orders, orderitems 
where customers.cust_id = orders.cust_id 
and orderitems.order_num = orders.order_num;
```

这条语句创建一个名为productcustomers的视图，它联结三个表，以返回已订购了任意产品的所有客户的列表。如果执行SELECT * FROM productcustomers，将列出订购了任意产品的客户。

```mysql
select cust_name, cust_contact from productcustomers 
where prod_id = 'TNT2';
```

**用视图重新格式化检索出的数据**

```mysql
CREATE VIEw vendorlocations AS 
SELECT Concat(RTrim(vend_name), '(', RTrim(vend_country), ')') 
As vend_title FROM vendors 
ORDER BY vend_name;
```

使用where子句筛选想要的数据，视图也可和计算字段一起使用。



#### 更新视图

通常，视图是可更新的（可以对它们使用INSERT、UPDATE和DELETE）。更新一个视图将更新其基表（可以回忆一下，视图本身没有数据）。如果你对视图增加或删除行，实际上是对其基表增加或删除行。

但是，并非所有视图都是可更新的。基本上可以说，如果MySQL不能正确地确定被更新的基数据，则不允许更新（包括插入和删除）。这实际上意味着，如果视图定义中有以下操作，则不能进行视图的更新：

1. 分组（使用GROUP BY和HAVING）；
2. 联结；
3. 子查询；
4. 并；
5. 聚集函数（Min()、Count()、Sum()等）；
6. DISTINCT;
7. 导出（计算）列。

上述限制只针对mysql 5，针对mysql 8参见[25.5.3 可更新和可插入视图_MySQL 8.0 参考手册](https://mysql.net.cn/doc/refman/8.0/en/view-updatability.html)。

一般来说，视图用于数据检索。



### 存储过程

存储过程简单来说，就是为以后的使用而保存一条或多条MySQL语句的集合，可将其视为批文件，虽然它们的作用不仅限于批处理。

使用存储过程有3个主要的好处，即简单、安全、高性能。

存在一些缺陷：编写复杂，可能没有创建存储过程的安全访问权限。

#### 执行存储过程

类似于其它语言中的函数

```mysql
call productpricing(@pricelow, @pricehigh, @priceaverage); 
```



#### 创建存储过程

一个返回产品平均价格的存储过程

```mysql
CREATE PROCEDURE productpricing() 
BEGIN 
SELECT Avg(prod_price) AS priceaverage 
FROM products; 
END;
```

BEGIN和END语句用来限定存储过程体，过程体本身仅是一个简单的SELECT语句。

> **mysql命令行客户机的分隔符** 如果使用的是mysql命令行实用程序，应该仔细阅读此说明。
>
> 默认的MySQL语句分隔符为';'。mysql命令行实用程序也使用';'作为语句分隔符。如果命令行实用程序要解释存储过程自身内的';'字符，则它们最终不会成为存储过程的成分，这会使存储过程中的SQL出现句法错误。解决办法是临时更改命令行实用程序的语句分隔符，如下所示：
>
> ```mysql
> DELIMITER // 
> CREATE PROCEDURE productpricing() 
> BEGIN
> SELECT Avg(prod_price) AS priceaverage 
> FROM products;
> END //
> DELIMITER ;
> ```
>
> DELIMITER // 告诉命令行实用程序使用//作为新的语句结束分隔符，除\符号外，任何字符都可以用作语句分隔符。

#### 删除存储过程

```mysql
drop procedure productpricing;
```

当过程存在想删除它时（如果过程不存在也不产生错误）可使用DROP PROCEDURE IF EXISTS。



#### 使用参数

```mysql
DELIMITER //
CREATE PROCEDURE productpricing(
	OUT pl DECIMAL(8,2), 
	OUT ph DECIMAL(8,2), 
    OUT pa DECIMAL(8,2)
    ) 
BEGIN
	SELECT Min(prod_price) INTO pl
	FROM products;
	SELECT Max(prod_price) INTO ph
	FROM products;
	SELECT Avg(prod_price) INTO pa
	FROM products; 
END//
DELIMITER ;
```

此存储过程接受3个参数：pl存储产品最低价格，ph存储产品最高价格，pa存储产品平均价格。每个参数必须具有指定的类型，这里使用十进制值。关键字OUT指出相应的参数用来从存储过程传出 一个值（返回给调用者）。MySQL支持IN（传递给存储过程）、OUT（从存储过程传出，如这里所用）和INOUT（对存储过程传入和传出）类型的参数。存储过程的代码位于BEGIN和END语句内，如前所见，它们是一系列SELECT语句，用来检索值，然后保存到相应的变量（通过指定INTO关键字）。返回值的处理与matlab有些相似，都是在一开始指定返回的参数。

**执行函数**

```mysql
set @pl = 0;
set @ph = 0;
set @pa = 0;
call learn.productpricing(@pl, @ph, @pa);
select @pl, @ph, @pa;
```



**使用IN和OUT参数**

```mysql
DELIMITER //
CREATE PROCEDURE ordertotal(
	IN onumber INT,
	OUT ototal DECIMAL(8,2)
)
BEGIN
	SELECT Sum(item_price*quantity) 
	FROM orderitems 
	WHERE order_num = onumber INTO ototal;
END//
DELIMITER ;
```

使用时调用

```mysql
call ordertotal(20005, @total);
select @total;
```



#### 建立智能存储过程

完成下列事情：

1. 获得合计（与以前一样）；
2. 把营业税有条件地添加到合计；
3. 返回合计（带或不带税）。

```mysql
-- Name: ordertotal
-- 	Parameters: onumber = order number
-- 				taxable = 0 if not taxable, 1 if taxable
--				ototal = order total variable 
DELIMITER //
CREATE PROCEDURE smart_ordertotal(
	IN onumber INT,
	IN taxable BOOLEAN ,
	OUT ototal DECIMAL(8,2)
) COMMENT'Obtain order total，optionally adding tax' 
BEGIN
	-- Declare variable for total 
	DECLARE total DECIMAL(8,2);
	-- Declare tax percentage
	DECLARE taxrate INT DEFAULT 6;
	-- Get the order total
	SELECT Sum(item_price * quantity) 
    FROM orderitems 
	WHERE order_num = onumber INTO total;
    
	-- Is this taxable?
    IF taxable THEN
		-- Yes，so add taxrate to the total
		SELECT total + (total / 100 * taxrate) INTO total;
	END IF;
	-- And finally，save to out variable
    SELECT total INTO ototal;
END// 
DELIMITER ;
```

此存储过程有很大的变动。首先，增加了注释（前面放置--）。在存储过程复杂性增加时，这样做特别重要。添加了另外一个参数taxable，它是一个布尔值（如果要增加税则为真，否则为假）。在 存储过程体中，用DECLARE语句定义了两个局部变量。DECLARE要求指定变量名和数据类型，它也支持可选的默认值（这个例子中的taxrate的默认被设置为6%）。SELECT语句已经改变，因此其结果存储到total（局部变量）而不是ototal。IF语句检查taxable是否为真，如果为真，则用另一 SELECT 语句增加营业税到局部变量 total。最后，用另一SELECT语句将total（它增加或许不增加营业税）保存到ototal。



#### 检查存储过程

为显示用来创建一个存储过程的CREATE语句，使用SHOW CREATE PROCEDURE语句

```mysql
show create procedure smart_ordertotal;
```

为了获得包括何时、由谁创建等详细信息的存储过程列表，使用`SHOW PROCEDURE STATUS`。

SHOW PROCEDURE STATUS列出所有存储过程。为限制其输出，可使用LIKE指定一个过滤模式，如

```mysql
show procedure status LIKE 'smart_ordertotal';
```



### 游标

游标（cursor）是一个存储在MySQL服务器上的数据库查询，它不是一条SELECT语句，而是被该语句检索出来的结果集。在存储了游标之后，应用程序可以根据需要滚动或浏览其中的数据。不像多数DBMS，MySQL游标只能用于存储过程（和函数）。

使用游标涉及几个明确的步骤。

1. 在能够使用游标前，必须声明（定义）它。这个过程实际上没有检索数据，它只是定义要使用的SELECT语句。
2. 一旦声明后，必须打开游标以供使用。这个过程用前面定义的SELECT语句把数据实际检索出来。
3. 对于填有数据的游标，根据需要取出（检索）各行。
4. 在结束游标使用时，必须关闭游标。

在声明游标后，可根据需要频繁地打开和关闭游标。在游标打开后，可根据需要频繁地执行取操作。

#### 创建游标

```mysql
DELIMITER //
CREATE PROCEDURE processorders()
BEGIN
	DECLARE ordernumbers CURSOR 
	FOR
	SELECT order_num FROM orders;
END//
DELIMITER ;
```

这个存储过程并没有做很多事情，DECLARE语句用来定义和命名游标，这里为ordernumbers。存储过程处理完成后，游标就消失（因为它局限于存储过程）。



#### 打开和关闭游标

`open ordernumbers`：打开游标

`close ordernumbers`：关闭游标

如果你不明确关闭游标，MySQL将会在到达END语句时自动关闭它，使用时在存储过程的内部使用。

```mysql
DELIMITER //
CREATE PROCEDURE processorders()
BEGIN
	DECLARE ordernumbers CURSOR 
	FOR
	SELECT order_num FROM orders;
    
    -- open the cursor 
    open ordernumbers;
	-- close the cursor
    close ordernumbers;
    
END//
DELIMITER ;
```



#### 使用游标数据

在一个游标被打开后，可以使用 FETCH 语句分别访问它的每一行。FETCH 指定检索什么数据（所需的列），检索出来的数据存储在什么地方。它还向前移动游标中的内部行指针，使下一条 FETCH 语句检索下一行（不重复读取同一行）。

```mysql
DELIMITER //
CREATE PROCEDURE processorders()
BEGIN
	-- Declare local varibles
    DECLARE o INT;
	DECLARE ordernumbers CURSOR 
	FOR
	SELECT order_num FROM orders;
    
    -- open the cursor 
    open ordernumbers;
    -- Get order number
    FETCH ordernumbers INTO o;
	-- close the cursor
    close ordernumbers;
END//
DELIMITER ;
```

其中FETCH用来检索当前行的 order_num 列（将自动从第一行开始）到一个名为 o 的局部声明的变量中。对检索出的数据不做任何处理。

使用REPEAT来循环检索数据，从第一行到最后一行

```mysql
DELIMITER //
CREATE PROCEDURE processorders()
BEGIN
	-- Declare local varibles
    DECLARE done BOOLEAN DEFAULT 0;
    DECLARE o INT;
	DECLARE ordernumbers CURSOR 
	FOR
	SELECT order_num FROM orders;
    -- Declare continue handler
	DECLARE CONTINUE HANDLER FOR SQLSTATE '02000' SET done=1;
    
    -- open the cursor 
    open ordernumbers;
    -- loop through all rows
    REPEAT 
		FETCH ordernumbers INTO o;
	UNTIL done END REPEAT;
    SELECT o;
	-- close the cursor
    close ordernumbers;
END//
DELIMITER ;
```

使用FETCH检索当前order_num到声明的名为o的变量中。但与前一个例子不一样的是，这个例子中的FETCH是在REPEAT内，因此它反复执行直到done为真（由`UNTIL done END REPEAT;`规定）。为使它起作用，用一个`DEFAULT 0`（假，不结 束）定义变量done。定义了一个CONTINUE  HANDLER，它是在条件出现时被执行的代码。这里，它指出当SQLSTATE '02000'出现时，SET done=1。SQLSTATE '02000' 是一个未找到条件，当REPEAT由于没有更多的行供循环而不能继续时，出现这个条件。

mysql的错误代码参见：[MySQL :: MySQL 8.2 Reference Manual :: B Error Messages and Common Problems](https://dev.mysql.com/doc/refman/8.2/en/error-handling.html)

一个完整的游程示例如下：

```mysql
DELIMITER //
CREATE PROCEDURE fullprocessorders()
BEGIN
	-- Declare local variab1es
	DECLARE done BOOLEAN DEFAULT 0;
    DECLARE o INT;
	DECLARE t DECIMAL(8,2);
	-- Declare the cursor
	DECLARE ordernumbers CURSOR FOR
	SELECT order_num FROM orders;
    -- Declare continue handler
	DECLARE CONTINUE HANDLER FOR SQLSTATE '02000' SET done=1;
	-- Create a table to store the results
	CREATE TABLE IF NOT EXISTS ordertotals
	(order_num INT, total DECIMAL(8,2));
	-- Open the cursor
	OPEN ordernumbers;
	-- Loop through all rows
    REPEAT
		-- Get order number
		FETCH ordernumbers INTO o;
		-- Get the total for this order
		CALL smart_ordertotal(o, 1, t);
		-- Insert order and total into ordertotals
		INSERT INTO ordertotals(order_num, total) VALUES(o, t);
	-- End of loop
	UNTIL done END REPEAT;
    
	-- close the cursor
	CLOSE ordernumbers;
END//
DELIMITER ;

```

在这个例子中，我们增加了另一个名为 t 的变量（存储每个订单的合计）。此存储过程还在运行中创建了一个新表（如果它不存在的话），名为ordertotals。这个表将保存存储过程生成的结果。FETCH像以前一样取每个order_num，然后用CALL执行另一个存储过程来计算每个订单的带税的合计（结果存储到 t ）。最后，用INSER保存每个订单的订单号和合计。



### 触发器

触发器是MySQL响应以下任意语句而自动执行的一条MySQL语句（或位于BEGIN和END语句之间的一组语句）：

1. DELETE
2. INSERT
3. UPDATE

其他MySQL语句不支持触发器。

在创建触发器时，需要给出4条信息：

1. 唯一的触发器名
2. 触发器关联的表
3. 触发器应该响应的活动（DELETE、INSERT或UPDATE）
4. 触发器何时执行（处理之前或之后）

在MySQL 5中，触发器名必须在每个表中唯一，但不是在每个数据库中唯一。这表示同一数据库中的两个表可具有相同名字的触发器。这在其他每个数据库触发器名必须唯一的DBMS中是不允许的，而且以后的MySQL版本很可能会使命名规则更为严格。因此，现在最好是在数据库范围内使用唯一的触发器名。

#### 创建触发器

```mysql
create trigger newproduct after insert on products 
for each row select 'Product added' into @message; -- 存入信息中
-- 插入新商品
INSERT INTO learn.products
(prod_id, vend_id, prod_name, prod_price, prod_desc)
VALUES ("test1", '1003', 'Test', 2, "product for test");

select @message;	-- message为Product added.
```

CREATE TRIGGER用来创建名为 newproduct 的新触发器。触发器可在一个操作发生之前或之后执行，这里给出了AFTER INSERT，所以此触发器将在 INSERT 语句成功执行后执行。这个触发器还指定 FOR EACH ROW，因此代码对每个插入行执行。在这个例子中，文本 Product added 将对每个插入的行显示一次。

使用 INSERT 语句添加一行或多行到 products 中，你将看到对每个成功的插入，显示 Product added 消息。

只有表才支持触发器，视图不支持（临时表也不支持）。触发器按每个表每个事件每次地定义，每个表每个事件每次只允许一个触发器。因此，每个表最多支持6个触发器（每条INSERT、UPDATE 和DELETE的之前和之后）。单一触发器不能与多个事件或多个表关联，所以，如果你需要一个对INSERT和UPDATE操作执行的触发器，则应该定义两个触发器。

如果BEFORE触发器失败，则MySQL将不执行请求的操作。此外，如果BEFORE触发器或语句本身失败，MySQL将不执行AFTER触发器（如果有的话）。



#### 删除触发器

```mysql
drop trigger newproduct;
```

触发器不能更新或覆盖。为了修改一个触发器，必须先删除它，然后再重新创建。



#### INSERT触发器

```mysql
create trigger neworder after insert on orders 
for each row select new.order_num into @ordernum;

INSERT INTO orders(order_date, cust_id) VALUES(Now(),10001);
select @ordernum;
```

注意这里通过new.order_num获得新创建的一行中的order_num。通常，将BEFORE用于数据验证和净化（目的是保证插入表中的数据确实是需要的数据）。本提示也适用于UPDATE触发器。



#### DELETE触发器

先来创建一个用于存档的表（这里的语句直接通过MySQL Workbench提供的复制创建声明的功能）

```mysql
CREATE TABLE `archive_orders` (
  `order_num` int NOT NULL AUTO_INCREMENT,
  `order_date` datetime NOT NULL,
  `cust_id` int NOT NULL,
  PRIMARY KEY (`order_num`),
  KEY `archive_orders_customers` (`cust_id`),
  CONSTRAINT `archive_orders_customers` FOREIGN KEY (`cust_id`) REFERENCES `customers` (`cust_id`)
) ENGINE=InnoDB AUTO_INCREMENT=20011 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

```

现在看看DELETE触发器的一个例子：

```mysql
DELIMITER //
CREATE TRIGGER deleteorder BEFORE DELETE ON orders 
FOR EACH row 
BEGIN
	INSERT INTO archive_orders(order_num, order_date, cust_id) 
	VALUES(OLD.order_num, OLD.order_date, OLD.cust_id);
END//
DELIMITER ;

delete from learn.orders where order_num = 20010;
```

执行完这段指令后，archive_orders会插入刚刚删除的数据。正如所见，触发器deleteorder使用BEGIN和END语句标记触发器体。这在此例子中并不是必需的，不过也没有害处。使用BEGIN END块的好处是触发器能容纳多条SQL语句（在BEGIN END块中一条挨着一条）



#### UPDATE触发器

UPDATE触发器在UPDATE语句执行之前或之后执行。需要知道以下几点：

1. 在 UPDATE 触发器代码中，你可以引用一个名为 OLD 的虚拟表访问以前（UPDATE语句前）的值，引用一个名为 NEW 的虚拟表访问新更新的值；
2. 在 BEFORE UPDATE 触发器中，NEW 中的值可能也被更新（允许更改将要用于 UPDATE 语句中的值）；
3. OLD 中的值全都是只读的，不能更新。

```mysql
create TRIGGER updatevendor BEFORE UPDATE ON vendors 
FOR EACH ROW SET NEW.vend_state = upper(NEW.vend_state);
```

这段指令保证 vend_state 总是大写的。

1. 与其他 DBMS 相比，MySQL 5中支持的触发器相当初级。未来的 MySQL 版本中有一些改进和增强触发器支持的计划。 
2. 创建触发器可能需要特殊的安全访问权限，但是，触发器的执行是自动的。如果INSERT、UPDATE或DELETE语句能够执行，则相关的触发器也能执行。
3. 应该用触发器来保证数据的一致性（大小写、格式等）。在触发器中执行这种类型的处理的优点是它总是进行这种处理，而且是透明地进行，与客户机应用无关。
4. 触发器的一种非常有意义的使用是创建审计跟踪。使用触发器把更改（如果需要，甚至还有之前和之后的状态）记录到另一个表非常容易。
5. 遗憾的是，MySQL触发器中不支持CALL语句。这表示不能从触发器内调用存储过程。所需的存储过程代码需要复制到触发器内。



### 管理事务处理

MyISAM前者不支持明确的事务处理管理，InnoDB支持事务处理管理。

事务处理可以用来维护数据库的完整性，它保证成批的MySQL操作要么完全执行，要么完全不执行。

事务处理是一种机制，用来管理必须成批执行的MySQL操作，以保证数据库不包含不完整的操作结果。利用事务处理，可以保证一组操作不会中途停止，它们或者作为整体执行，或者完全不执行（除非明确指示）。如果没有错误发生，整组语句提交给（写到）数据库表。如果发生错误，则进行回退（撤销）以恢复数据库到某个已知且安全的状态。

这个例子展示了一个过程如何工作：

(1) 检查数据库中是否存在相应的客户，如果不存在，添加他/她。

(2) 提交客户信息。

(3) 检索客户的ID。

(4) 添加一行到orders表。

(5) 如果在添加行到orders表时出现故障，回退。

(6) 检索orders表中赋予的新订单ID。

(7) 对于订购的每项物品，添加新行到orderitems表。

(8) 如果在添加新行到orderitems时出现故障，回退所有添加的orderitems行和orders行。

(9) 提交订单信息。

在这些过程中包含的几个关键词汇：

**事务**：一组SQL语句；

**回退**：撤销指定SQL语句的过程；

**提交**：将未存储的SQL语句结果写入数据库表；

**保留点**：指事务处理中设置的临时占位符（placeholder），你可以对它发布回退（与回退整个事务处理不同）。

事务的开始使用下面的语句：



#### 使用ROLLBACK

使用ROLLBACK回退操作（在mysql 8中需要先关闭safe update模式）

```mysql
SELECT * from ordertotals; 
START TRANSACTION;
DELETE FROM ordertotals;
SELECT * FROM ordertotals;
ROLLBACK;
SELECT * FROM ordertotals;
```

这个例子从显示 ordertotals 表的内容开始。首先执行一条 SELECT 以显示该表不为空。然后开始一个事务处理，用一条 DELETE 语句删除 ordertotals 中的所有行。另一条 SELECT 语句验证 ordertotals 确实为空。这时用一条 ROLLBACK 语句回退 START TRANSACTION 之后的所有语句，最后一条 SELECT 语句显示该表不为空。显然，ROLLBACK 只能在一个事务处理内使用（在执行一条 START TRANSACTION 命令之后）。事务处理用来管理 INSERT、UPDATE 和 DELETE 语句。你不能回退 SELECT 语句（没有意义），你不能回退CREATE或DROP操作。事务处理块中可以使用这两条语句，但如果你执行回退，它们不会被撤销。



#### 使用COMMIT

一般的MySQL语句都是直接针对数据库表执行和编写的。这就是所谓的隐含提交（implicit commit），即提交（写或保存）操作是自动进行的。 但是，在事务处理块中，提交不会隐含地进行。为进行明确的提交，使用COMMIT语句。

```mysql
START TRANSACTION;
DELETE FROM orderitems WHERE order_num = 20010;
DELETE FROM orders WHERE order_num = 20010;
COMMIT;
```

在这个例子中，从系统中完全删除订单20010。因为涉及更新两个数据库表 orders 和 orderItems，所以使用事务处理块来保证订单不被部分删除。最后的COMMIT语句仅在不出错时写出更改。如果第一条DELETE起作用，但第二条失败，则DELETE不会提交（实际上，它是被自动撤销的）

在这个例子中，从系统中完全删除订单20010。因为涉及更新两个数据库表 orders 和 orderItems，所以使用事务处理块来保证订单不被部分删除。最后的COMMIT语句仅在不出错时写出更改。如果第一条DELETE起作用，但第二条失败，则DELETE不会提交（实际上，它是被自动撤销的）



#### 使用保留点

为了支持回退部分事务处理，必须能在事务处理块中合适的位置放 置占位符。这样，如果需要回退，可以回退到某个占位符。 这些占位符称为保留点。为了创建占位符，可如下使用SAVEPOINT 语句：

```mysql
savepoint delete1;
```

回退到保留点：

```mysql
ROLLBACK TO delete1;
```

明确释放保留点（保留点在事务处理完成（执行一条ROLLBACK或COMMIT）后自动释放。）

```mysql
RELEASE delete1;
```



#### 更改默认的提交行为

默认的MySQL行为是自动提交所有更改。换句话说，任何时候你执行一条MySQL语句，该语句实际上都是针对表执行的，而且所做的更改立即生效。为指示MySQL不自动提交更改，需要使用以下语句：

```mysql
SET autocommit = 0;
```

autocommit标志决定是否自动提交更改，不管有没有COMMIT语句。设置autocommit为0（假）指示MySQL不自动提交更改（直到autocommit被设置为真为止）。autocommit标志是针对每个连接而不是服务器的。



### 其它

#### 全球化和本地化

数据库表被用来存储和检索数据。不同的语言和字符集需要以不同的方式存储和检索。因此，MySQL需要适应不同的字符集（不同的字母和字符），适应不同的排序和检索数据的方法。 在讨论多种语言和字符集时，将会遇到以下重要术语：

1. 字符集为字母和符号的集合；
2. 编码为某个字符集成员的内部表示；
3. 校对为规定字符如何比较的指令。

**查看可用字符集**

```mysql
SHOW CHARACTER SET;
```

**查看所支持校对的完整列表**

```mysql
SHOW COLLATION;
```

有的字符集具有不止一种校对。例如，latin1对不同的欧洲语言有几种校对，而且许多校对出现两次，一次区分大小写（由\_cs 表示），一次不区分大小写（由\_ci表示）。

字符集和校对可以在创建表的时候指定，除了对表，还支持对列指定字符集和校对，如下：

```mysql
CREATE TABLE mytable(
columnn1 INT, 
columnn2 VARCHAR(10), 
column3 VARCHAR(10) CHARACTER SET latin1 COLLATE latin1_general_ci
)DEFAULT CHARACTER SET hebrew COLLATE hebrew_general_ci;
```

还可以在排序的时候指定，如

```mysql
SELECT * FROM customers 
ORDER BY lastname, firstname COLLATE latinal_general_cs;
```

COLLATE还可以用于GROUP BY、HAVING、聚集函数、别名等。最后，值得注意的是，如果绝对需要，串可以在字符集之间进行转换。为此，使用 Cast() 或 Convert() 函数。



#### 安全管理

MySQL用户账号和信息存储在名为mysql的MySQL数据库中。一般不需要直接访问mysql数据库和表（你稍后会明白这一点），但有时需要直接访问。需要直接访问它的时机之一是在需要获得所有用户账号列表时。为此，可使用以下代码：

```mysql
use mysql;
select user from user;
```



**创建用户**

使用create user语句，

```mysql
create user xmj IDENTIFIED by 'password'; -- 创建用户并设置密码为password
create user xmj;		-- 创建时可以无口令
```

**重命名用户**

```mysql
rename user xmj to xmj03;
```

**删除用户**

```mysql
drop user xmj;
```

**设置访问权限**

在创建用户账号后，必须接着分配访问权限。新创建的用户账号没有访问权限。它们能登录MySQL，但不能看到数据，不能执行任何数据库操作。

使用`SHOW GRANTS FOR`，如下：

```mysql
show grants for root;
```

为设置权限，使用GRANT语句。GRANT要求你至少给出以下信息：

1. 要授予的权限；
2. 被授予访问权限的数据库或表；
3. 用户名。

```mysql
grant select on learn.* to xmj;
```

此GRANT允许用户在learn.*（learn数据库的所有表）上使用SELECT。通过只授予SELECT访问权限，用户xmj对learn数据库中的所有数据具有只读访问权限。

反操作为REVOKE用于撤销特定权限，如：

```mysql
revoke select on learn.* from xmj;
```

GRANT和REVOKE可在几个层次上控制访问权限：

1. 整个服务器，使用GRANT ALL和REVOKE ALL；
2. 整个数据库，使用ON database.*；
3. 特定的表，使用ON database.table；
4. 特定的列；
5. 特定的存储过程。

具体可供操作的权限参见：[MySQL :: MySQL 8.0 Reference Manual :: 6.2.2 Privileges Provided by MySQL](https://dev.mysql.com/doc/refman/8.0/en/privileges-provided.html)



**更改密码**

```mysql
set password for xmj = Password("xmj123456");
```

用来设置当前登录用户的口令

```mysql
set password = Password("xmj123456");
```



#### 数据库维护

**备份数据**

像所有数据一样，MySQL的数据也必须经常备份。由于MySQL数据库是基于磁盘的文件，普通的备份系统和例程就能备份MySQL的数据。但是，由于这些文件总是处于打开和使用状态，普通的文件副本备份不一定总是有效。 下面列出这个问题的可能解决方案。 

1. 使用命令行实用程序 mysqldump 转储所有数据库内容到某个外部文件。在进行常规备份前这个实用程序应该正常运行，以便能正确地备份转储文件。
2. 可用命令行实用程序 mysqlhotcopy 从一个数据库复制所有数据（并非所有数据库引擎都支持这个实用程序）。
3. 可以使用MySQL的BACKUP TABLE或SELECT INTO OUTFILE转储所有数据到某个外部文件。这两条语句都接受将要创建的系统文件名，此系统文件必须不存在，否则会出错。数据可以用RESTORE TABLE来复原。



**进行数据库维护**

使用`ANALYZE TABLE`检查表键是否正确

```mysql
analyze table learn.orders;
```

`CHECK TABLE`用来针对许多问题对表进行检查。在MyISAM表上还对索引进行检查。CHECK TABLE支持一系列的用于MyISAM表的方式。CHANGED检查自最后一次检查以来改动过的表。EXTENDED执行最 彻底的检查，FAST只检查未正常关闭的表，MEDIUM检查所有被删除的链接并进行键检验，QUICK只进行快速扫描。如下所示，CHECK TABLE发现和修复问题：

```mysql
check table orders, orderitems;
```

如果MyISAM表访问产生不正确和不一致的结果，可能需要用`REPAIR TABLE`来修复相应的表。这条语句不应该经常使用，如果需要经常使用，可能会有更大的问题要解决。

如果从一个表中删除大量数据，应该使用`OPTIMIZE TABLE`来收回所用的空间，从而优化表的性能。



**诊断启动问题**

MySQL服务器自身通过在命令行上执行mysqld启动。下面是几个重要的mysqld命令行选项：

1. --help显示帮助——一个选项列表；
2. --safe-mode装载减去某些最佳配置的服务器；
3. --verbose显示全文本消息（为获得更详细的帮助消息与--help 联合使用）；
4. --version显示版本信息然后退出

**查看日志文件**

1. 错误日志，它包含启动和关闭问题以及任意关键错误的细节。此日志通常名为hostname.err，位于data目录中。此日志名可用--log-error命令行选项更改。
2. 查询日志，它记录所有MySQL活动，在诊断问题时非常有用。此日志文件可能会很快地变得非常大，因此不应该长期使用它。此日志通常名为hostname.log，位于data目录中。此名字可以用 --log命令行选项更改。
3. 二进制日志，它记录更新过数据（或者可能更新过数据）的所有语句。此日志通常名为hostname-bin，位于data目录内。此名字可以用--log-bin命令行选项更改。注意，这个日志文件是MySQL 5中添加的，以前的MySQL版本中使用的是更新日志。 
4. 缓慢查询日志，顾名思义，此日志记录执行缓慢的任何查询。这个日志在确定数据库何处需要优化很有用。此日志通常名为 hostname-slow.log ，位于data目录中。此名字可以用--log-slow-queries命令行选项更改。

在使用日志时，可用FLUSH LOGS语句来刷新和重新开始所有日志文件。



#### 改善性能

MySQL是用一系列的默认设置预先配置的，从这些设置开始通常是很好的。但过一段时间后你可能需要调整内存分配、缓冲区大小等。为查看当前设置，可使用SHOW VARIABLES;和SHOW STATUS;。

MySQL是一个多用户多线程的DBMS，换言之，它经常同时执行多个任务。如果这些任务中的某一个执行缓慢，则所有请求都会执行缓慢。如果你遇到显著的性能不良，可使用SHOW PROCESSLIST显示所有活动进程（以及它们的线程ID和执行时间）。你还可以用KILL命令终结某个特定的进程（使用这个命令需要作为管理员登录）。

更多参考官方文档[MySQL :: MySQL Documentation](https://dev.mysql.com/doc/)。

## 实战

### 参考资料

> [MySQL :: MySQL Connector/Python Developer Guide :: 5 Connector/Python Coding Examples](https://dev.mysql.com/doc/connector-python/en/connector-python-examples.html)



### 插入数据

将[penguins.csv](https://github.com/mwaskom/seaborn-data/blob/master/penguins.csv)中数据转入数据库中，需要先创建penguins数据库

python代码：

```python
import mysql.connector
from mysql.connector import errorcode
import pandas as pd
import numpy as np

cnx = mysql.connector.connect(user='root', password='XMJsql123456',
                              host='127.0.0.1',
                              database='penguins')
specie = (
    "create table specie("
    "`id`  int Not null auto_increment,"
    "`species` char(32) not null,"
    "`island` char(32) not null,"
    "`blen` decimal(4,1) null,"
    "`bdep` decimal(4,1) null,"
    "`flen` SMALLINT null,"
    "`mass` SMALLINT null,"
    "`sex` bool null,"
    "primary key (id)"
    ") engine=InnoDB"
)
add_sp = "insert into specie (species, island, blen, bdep, flen, mass, sex) VALUES "

data = pd.read_csv("penguins.csv")

data = np.array(data)
data[data == "MALE"] = 1
data[data == "FEMALE"] = 0
data = data.tolist()

for item in data:
    sp = "("
    for it in item:
        if type(it) == float and np.isnan(it):
            sp += "null,"
        else:
            sp += f"'{it}',"
    sp = sp[:-1] + "),"
    add_sp += sp
add_sp = add_sp[:-1] + ";"

cursor = cnx.cursor()

# 创建表
try:
    cursor.execute(specie)
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("already exists.")
    else:
        print(err.msg)
else:
     print("OK")

# 插入数据
try:
    cursor.execute(add_sp)
except mysql.connector.Error as err:
    print(err.msg)
else:
     print("OK")
cnx.commit()        # 提交数据到数据库
cursor.close()
cnx.close()
```

