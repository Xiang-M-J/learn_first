# Html

**HTML（HyperText Markup Language）** 是用于描述网页结构的标记语言。  
一个典型的 HTML 文档由三部分组成：

- **文档类型声明**：指定 HTML 版本。
- **`<head>`**：包含元数据（metadata），如标题、样式、脚本等。
- **`<body>`**：包含网页可见内容。

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>我的第一个网页</title>
</head>
<body>
  <h1>你好，世界！</h1>
</body>
</html>
```

## 常用标签

### 结构性标签

|标签|说明|
|---|---|
|`<html>`|HTML 文档根元素|
|`<head>`|定义文档的元数据|
|`<body>`|定义文档主体内容|
|`<header>`|页面或章节头部（HTML5 新增）|
|`<footer>`|页面或章节底部（HTML5 新增）|
|`<nav>`|导航区域（HTML5 新增）|
|`<main>`|主内容区（HTML5 新增）|
|`<section>`|逻辑分块（HTML5 新增）|
|`<article>`|独立的内容单元，如博客文章|
|`<aside>`|侧边栏信息（HTML5 新增）|
|`<div>`|通用容器（旧版常用，仍广泛使用）|

### 文本与排版标签

| 标签                | 说明           |
| ----------------- | ------------ |
| `<h1>`~`<h6>`     | 标题，h1 最大     |
| `<p>`             | 段落           |
| `<br>`            | 换行（空元素）      |
| `<hr>`            | 水平分隔线        |
| `<b>`, `<strong>` | 加粗，后者语义更强    |
| `<i>`, `<em>`     | 斜体，后者语义更强    |
| `<u>`             | 下划线（不推荐过度使用） |
| `<span>`          | 行内容器         |
| `<pre>`           | 保留空格和换行的文本   |
| `<blockquote>`    | 引用大段文字       |
| `<code>`          | 行内代码片段       |
| `<sup>`, `<sub>`  | 上标、下标        |

### 列表标签

|标签|说明|
|---|---|
|`<ul>`|无序列表|
|`<ol>`|有序列表|
|`<li>`|列表项|

### 超链接与媒体

|标签|说明|
|---|---|
|`<a href="...">`|超链接|
|`<img src="...">`|图片|
|`<audio>`|音频（HTML5 新增）|
|`<video>`|视频（HTML5 新增）|
|`<source>`|媒体资源文件|
|`<iframe>`|内联框架，用于嵌入其他页面|
|`<embed>`|嵌入外部内容（如 Flash，现已过时）|

### 表格标签

|标签|说明|
|---|---|
|`<table>`|表格|
|`<tr>`|行|
|`<th>`|表头单元格|
|`<td>`|表格单元格|
|`<caption>`|表格标题|
|`<thead>`, `<tbody>`, `<tfoot>`|表格分区|

### 表单标签

|标签|说明|
|---|---|
|`<form>`|表单容器|
|`<input>`|输入框（type 决定类型，如 text、password、checkbox）|
|`<textarea>`|多行文本输入|
|`<select>` / `<option>`|下拉选择框|
|`<label>`|输入标签描述|
|`<button>`|按钮|
|`<fieldset>` / `<legend>`|表单分组|


## 引入 CSS 

CSS（Cascading Style Sheets）用于描述网页的外观和样式。

### 行内样式

直接在标签上使用 `style` 属性。

```html
<p style="color: red; font-size: 18px;">红色文字</p>
```

✅ 简单方便  
❌ 不利于维护和复用

### 内部样式表

写在 `<head>` 中的 `<style>` 标签内。

```html
<style>
  p { color: blue; }
</style>
```

✅ 适合单个页面  
❌ 不适合大型项目

### 外部样式表

通过 `<link>` 引入 `.css` 文件。

```html
<link rel="stylesheet" href="styles.css">
```

✅ 推荐方式，可缓存、可复用  
❌ 需额外 HTTP 请求（可用 CDN 或合并优化）

### @import 引入

在 CSS 内部导入另一个样式表。

```css
@import url("reset.css");
```

✅ 灵活  
❌ 性能差于 `<link>`（延迟加载）

## 引入 JavaScript

### 行内脚本

直接在标签内写逻辑：

```html
<button onclick="alert('你好!')">点击我</button>
```

✅ 简单  
❌ 不推荐（不利于维护、安全性差）

### 内部脚本

在 HTML 中使用 `<script>`：

```html
<script>
  console.log("页面加载完毕");
</script>
```

### 外部脚本

通过 `src` 属性引入 `.js` 文件：

```html
<script src="app.js"></script>
```

✅ 推荐做法，可复用、便于调试  
⚠️ 默认同步加载，浏览器在解析html时，遇到`<script>`会立即停止解析html，开始下载并执行 JS 文件，这可能会阻塞html的渲染，可使用 `defer` 或 `async` 优化加载

#### defer

```html
<script src="app.js" defer></script>
```

JS 文件与 HTML 同时并行下载（不阻塞解析），HTML 解析完毕后（即 DOM 构建完成）再执行脚本，若有多个 defer 脚本，会按顺序执行（依 HTML 中出现的顺序）。

#### async

```html
<script src="app.js" async></script>
```

JS 文件与 HTML 并行下载（不阻塞解析），下载完成后，立即中断 HTML 解析并执行该脚本，执行完脚本后再继续解析 HTML，多个 async 脚本的执行顺序不确定（谁先下载完谁先执行）。


> [!Info] 推荐写法
> 对于依赖DOM的主业务逻辑，使用defer
> 对于独立脚本，如广告、统计流量等，使用async



## UI 库

1. [Semantic UI (semantic-ui.com)](https://semantic-ui.com/) ui库
2. [Bootstrap · The most popular HTML, CSS, and JS library in the world. (getbootstrap.com)](https://getbootstrap.com/) ui库
3. [Getting started | Less.js (lesscss.org)](https://lesscss.org/) css预编译库
4. [Amaze UI | 中国首个开源 HTML5 跨屏前端框架 (shopxo.net)](http://amazeui.shopxo.net/) ui库
5. [Introduction to Metro UI :: Popular HTML, CSS and JS library ](https://metroui.org.ua/intro.html) ui库
6. [Layui - 极简模块化前端 UI 组件库(官方文档)](https://layui.dev/) ui 库



# CSS


**CSS（Cascading Style Sheets，层叠样式表）** 用于描述 **HTML 元素的外观样式**，使网页从结构与内容（HTML）中分离出视觉表现部分。

CSS 通过 **选择器（selector）** 绑定到 HTML 元素，再通过 **属性（property）** 设置视觉样式。

| 引入方式               | 示例                                         | 说明                   |
| ------------------ | ------------------------------------------ | -------------------- |
| **行内样式（inline）**   | `<p style="color:red;">文字</p>`             | 直接在标签内写样式，优先级最高，但不推荐 |
| **内部样式（internal）** | `html <style>p{color:blue;}</style>`       | 适合单页面                |
| **外部样式（external）** | `<link rel="stylesheet" href="style.css">` | 推荐方式，可复用与缓存          |

优先级从高到低如下所示

1. !important：无条件优先，覆盖所有其他规则。
2. 内联样式：例如`style="..."`，权重为 1000。
3. ID 选择器：例如`#id`，权重为 100。
4. 类选择器、伪类、属性选择器：例如 `.class`、`:hover`，权重为 10。
5. 标签选择器、伪元素：例如 `div`、`::before`，权重为 1。
6. 通配选择器：例如`*`，权重为 0。

## 选择器

### 基础选择器

|类型|示例|说明|
|---|---|---|
|标签选择器|`p {}`|选择所有 `<p>` 元素|
|类选择器|`.btn {}`|选择 class="btn" 的元素|
|ID 选择器|`#header {}`|选择 id="header" 的元素|
|通配选择器|`* {}`|选择所有元素（不推荐滥用）|


### 层级与关系选择器

|示例|说明|
|---|---|
|`div p`|div 内的所有 p（后代）|
|`div > p`|div 的直接子元素 p|
|`div + p`|紧接在 div 后的第一个 p|
|`div ~ p`|div 后所有兄弟 p|

### 属性选择器

```css
input[type="text"] { color: blue; }
a[target="_blank"] { text-decoration: underline; }
```

### 伪类与伪元素

|类型|示例|用途|
|---|---|---|
|伪类|`a:hover`, `input:focus`, `li:first-child`, `:nth-child(odd)`|根据状态或结构匹配|
|伪元素|`::before`, `::after`, `::first-letter`, `::selection`|为元素添加虚拟内容或修饰|

示例：

```css
button::before {
  content: "👉";
  margin-right: 5px;
}
```

## 常见 CSS 属性

### 文本与字体

```css
p {
  color: #333;
  font-size: 16px;
  font-family: "Microsoft YaHei", sans-serif;
  font-weight: bold;
  line-height: 1.5;
  text-align: center;
  text-decoration: underline;
  text-transform: uppercase;
}
```

### 背景与边框

```css
div {
  background-color: #f0f0f0;
  background-image: url('bg.jpg');
  background-size: cover;
  border: 2px solid #333;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0,0,0,0.2);
}
```


### 尺寸与盒模型

```css
div {
  width: 200px;
  height: 100px;
  padding: 10px;
  margin: 20px;
  box-sizing: border-box; /* 新标准写法 */
}
```

> 📦 `box-sizing: border-box` 让宽高包含 padding 与 border，是现代布局常用方式。

### 定位与浮动

```css
.positioned {
  position: absolute;
  top: 20px;
  left: 50px;
}

.fixed {
  position: fixed;
  bottom: 10px;
  right: 10px;
}
```

|值|说明|
|---|---|
|static|默认（无定位）|
|relative|相对自身偏移|
|absolute|相对最近的定位祖先|
|fixed|相对视口固定|
|sticky|滚动时“粘住”|

### 浮动与清除

```css
img { float: left; margin-right: 10px; }
.clearfix::after { content: ""; display: block; clear: both; }
```

> ⚠️ 虽然 `float` 布局现在被 `flex` 与 `grid` 替代，但在旧网页中仍广泛使用。


## 布局方式

### Flexbox 弹性布局

用于一维布局（行或列）。

```css
.container {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
```

常用属性：

|属性|说明|
|---|---|
|`justify-content`|主轴对齐（如居中）|
|`align-items`|交叉轴对齐|
|`flex-wrap`|是否换行|
|`flex: 1`|弹性伸缩（自动分配空间）|

### Grid 网格布局

用于二维布局（行 + 列）。

```css
.container {
  display: grid;
  grid-template-columns: 1fr 2fr 1fr;
  grid-gap: 10px;
}
```

✅ 支持精确的网格定位：

```css
.item1 { grid-column: 1 / 3; grid-row: 1 / 2; }
```

> 🆕 Grid 是现代布局的核心特性，已被所有主流浏览器支持。

### 传统布局方式

|方式|示例|缺点|
|---|---|---|
|表格布局|`<table><tr><td></td></tr></table>`|不灵活、结构混乱|
|浮动布局|`float: left;`|需要清除浮动，复杂|
|定位布局|`position: absolute;`|不响应式|


## 响应式设计与媒体查询

```css
@media (max-width: 768px) {
  body { font-size: 14px; }
  .sidebar { display: none; }
}
```

✅ 根据屏幕尺寸自动调整布局。  
还可用于主题适配：

```css
@media (prefers-color-scheme: dark) {
  body { background: #111; color: #eee; }
}
```

## CSS 动画与过渡

### 过渡

```css
button {
  background: #09f;
  transition: background 0.3s ease;
}
button:hover {
  background: #06c;
}
```

> 鼠标悬停时平滑过渡。

### 关键帧动画

```css
@keyframes bounce {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-20px); }
}

.ball {
  animation: bounce 1s infinite;
}
```

|属性|说明|
|---|---|
|`animation-name`|动画名称|
|`animation-duration`|持续时间|
|`animation-timing-function`|时间函数（如 ease, linear）|
|`animation-iteration-count`|循环次数|
|`animation-delay`|延迟时间|


# Javascript


## 基本知识

### 索引集合类

在实现层面，JavaScript中实际上将数组当成字典实现，整数索引就是键。


创建数组

```js
const arr1 = new Array(element0, element1, /* … ,*/ elementN);
const arr2 = Array(element0, element1, /* … ,*/ elementN);
const arr3 = [element0, element1, /* … ,*/ elementN];


// 创建空数组
const arr1 = new Array(arrayLength);
const arr2 = Array(arrayLength);
const arr3 = [];
arr3.length = arrayLength;
```


填充数组

直接使用类似字典赋值的方式填充数组，并且数组长度和最后一个整数键有关

```js
const emp = [];
emp[0] = "Casey Jones";
emp[1] = "Phil Lesh";
emp[2] = "August West";
emp[3.2] = "Jee";
emp[30] = "Tom";
console.log(emp[3.2]);
console.log(emp['length']); // 输出31
```

JavaScript中的数组长度可以用来控制数组元素的增加和删除，假如一个数组里面有三个元素，那么将数组长度设置为2，则会删除最后一个元素，如果数组长度设置为2，那么数组会被清空。

遍历数组

JavaScript提供了`forEach`方法来遍历数组元素

```js
const sparseArray = ["first", "second", , "fourth"]; 
sparseArray.forEach((element) => 
{ console.log(element); }
);
```

一些数组方法

```js
arr1 = [1, 2, 3];
arr2 = [4, 5, 6];

arr3 = arr2.concat(arr1); // 连接两个数组
let s_arr = arr1.join("-"); // 格式化字符串
let arr_len1 = arr1.push(4); // 数组末尾添加元素，返回长度
let pop_data = arr1.pop();    // 删除数组末尾元素并返回该元素
let shift_data = arr1.shift();  // 移出数组的第一个元素并返回该元素
let arr_len2 = arr1.unshift(1);   // 在数组开始添加元素，返回长度
```

还有更多方法，

### 带键的集合

Map对象是一个简单的键值对映射集合

```js
const sayings = new Map();
sayings.set("dog", "woof");
sayings.set("cat", "meow");
sayings.set("elephant", "toot");
sayings.size; // 3
sayings.get("dog"); // woof
sayings.get("fox"); // undefined
sayings.has("bird"); // false
sayings.delete("dog");
sayings.has("dog"); // false

for (const [key, value] of sayings) {
  console.log(`${key} goes ${value}`);
}
// "cat goes meow"
// "elephant goes toot"

sayings.clear();
sayings.size; // 0
```

Set是一组唯一值的集合，可以按照添加顺序来遍历。`Set` 中的值只能出现一次；它在集合 `Set` 中是唯一的。

```js
const mySet = new Set();
mySet.add(1);
mySet.add("some text");
mySet.add("foo");

mySet.has(1); // true
mySet.delete("foo");
mySet.size; // 2

for (const item of mySet) {
  console.log(item);
}
// 1
// "some text"


// 数组和Set的转换
Array.from(mySet);
[...mySet2];

mySet2 = new Set([1, 2, 3, 4]);
```

### 对象和类

对象是属性的集合，有点像字典，包含了各种属性和对应的值，也能像字典一样访问。

下面介绍三种创建对象的方法

```js
// 方式1
const myHonda = {
  color: "red",
  wheels: 4,
  engine: { cylinders: 4, size: 2.2 },
};

// 方式2
function Car(make, model, year) {
  this.make = make;
  this.model = model;
  this.year = year;
}
const myCar = new Car("Eagle", "Talon TSi", 1993);


// 方式3，可以无需在定义时传值
const Animal = {
  type: "Invertebrates", // Default value of properties
  displayType() {
    console.log(this.type);
  },
};

const fish = Object.create(Animal); 
fish.type = "Fishes"; 
fish.displayType(); // Logs: Fishes
```

访问对象的属性时可以使用 `obj.x` 或者`obj['x']`这两种方式

遍历对象的所有属性可以使用 `for...in` 或者`Object.keys()`，如下所示

```js
for (const key in car) {
    console.log(key);
}

Object.keys(car).forEach((e) => console.log(e));
```


类使用class声明，可以通过static关键字声明静态方法或属性（直接通过类访问，如`MyClass.s_attr`）

```js
class MyClass {
  // 构造器
  constructor() {
  }
  // 实例属性
  myField = "foo";
  // 实例方法
  myMethod() {
  }
  // 静态属性
  static myStaticField = "bar";
  // 静态方法
  static myStaticMethod() {
  }
  static {
    // 初始化静态属性
  }
  // 用 # 来定义私有属性
  #myPrivateField = "bar";
}

const myInstance = new MyClass(); 
console.log(myInstance.myField); // 'foo' 
myInstance.myMethod();
```

使用 `extends` 关键字实现类的继承，使用`super`函数初始化父类

```js
class Dog extends Animal {
  constructor(name, lang, age) {
    super(name, lang);
    this._age = age;
  }
  dogAge() {
    console.log(`${this._name}今年${this._age}岁了`);
  }
}
```


### Promises

用于处理异步操作，表示一个异步操作的最终结果

首先定义一个返回promise的函数
```js
const doSomething = new Promise((resolve, reject) => {
    setTimeout(
        ()=> {
            const success = false;
            if (success) {
                resolve("success");
            }else{
                reject("fail");
            }
        }, 1000
    );
});
```

然后可以通过下面这种方式来串行处理，并通过catch来捕获错误

```js
doSomething.then(
    (result) => {
        console.log(result); 
        return "process result";
    }
).then(
    (result) => {console.log(result)}
).catch((error) => {
    console.error(error);
});
```


另一种更加推荐的做法是使用`async/await`

```js
async function logIngredients() {
  const url = await doSomething();
  const res = await fetch(url);
  const data = await res.json();
  listOfIngredients.push(data);
  console.log(listOfIngredients);
}
```

如果上述步骤可以并行，那么可以这样写

```js
const [user, posts, profile] = await Promise.all(
[ getUser(), getPosts(), getProfile() ]
);

// 另一种做法
Promise.all([func1(), func2(), func3()]).then(([result1, result2, result3]) => { 
// use result1, result2 and result3 
});
```

### 类型化数组

用来处理原始二进制数据，如音频或者视频等。类型化数组中包含了两个概念：buffer（一组数据）和view（指定数据格式、偏移等信息）。

buffer有两种：[`ArrayBuffer`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/ArrayBuffer) 和 [`SharedArrayBuffer`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/SharedArrayBuffer)
view有许多种，基本上包括了常见的数值类型，如[`Int8Array`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Int8Array)、[`Uint8Array`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Uint8Array)等。

```js
const buffer = new ArrayBuffer(16);  // 初始化一个长度为16的buffer
console.log(buffer.byteLength);

const int32view = new Int32Array(buffer);
console.log(int32view)
```


### 迭代器和生成器

下面这段代码演示了如何创建和遍历迭代器

```js
function makeRangeIterator(start = 0, end = Infinity, step = 1) {
  let nextIndex = start;
  let iterationCount = 0;

  const rangeIterator = {
    next() {
      let result;
      if (nextIndex < end) {
        result = { value: nextIndex, done: false };
        nextIndex += step;
        iterationCount++;
        return result;
      }
      return { value: iterationCount, done: true };
    },
  };
  return rangeIterator;
}

// 遍历迭代器
const iter = makeRangeIterator(1, 10, 2);

let result = iter.next();
while (!result.done) {
  console.log(result.value); // 1 3 5 7 9
  result = iter.next();
}

console.log("Iterated over sequence of size:", result.value); // [5 numbers returned, that took interval in between: 0 to 10]
```

上面创建迭代器的部分比较复杂，可以使用生成器来实现相同的功能，生成器函数用 `function*`来标识。

```js
function* makeRangeIterator(start = 0, end = Infinity, step = 1) {
  let iterationCount = 0;
  for (let i = start; i < end; i += step) {
    iterationCount++;
    yield i;
  }
  return iterationCount;
}
```

在遍历时，可能需要传值到生成过程（有时需要重置生成器）

```js
function* fibonacci() {
  let current = 0;
  let next = 1;
  while (true) {
    const reset = yield current;
    [current, next] = [next, next + current];
    if (reset) {
      current = 0;
      next = 1;
    }
  }
}

const sequence = fibonacci();
console.log(sequence.next().value); // 0
console.log(sequence.next().value); // 1
console.log(sequence.next(true).value); // 0
console.log(sequence.next().value); // 1
```


### 模块

定义一个模块文件，需要导出的变量和函数使用`export`关键字标记

```js
export const sample_rate = 16000;

export function read_audio(audio_path) {
    console.log(`read audio: ${audio_path}`);
}
```

在别的js中导入模块
```js
import { sample_rate, read_audio as ra } from "./audio_utils.js";

console.log(sample_rate);
ra("test.mp3");
```

html中引入该js文件的代码为

```html
<script type="module" src="test_module.js"></script>
```




## 实用功能

### 读取本地文件

```javascript
<script>
  async function fetchText(){
    const response = await fetch(`test.txt`)
    const text = await response.text();
    console.log(text)
  }
  fetchText();
</script>
```



## TypeScript

TypeScript是JavaScript的超集，在JavaScript中加入了语法检查，检查类型错误。

有两种方式可以在项目中引入typescript

1. 使用npm下载 `npm install -g typescript`
2. 下载Visual Studio的TypeScript插件

在npm中安装完typescript后，可以使用`tsc main.ts`来将ts转为js文件，用于html等。

typescript中有interface接口，用于指定一个对象模板，可以看成是一种类型约定，即这种类型的实例需要包含这些属性

```ts
interface Person {
  firstName: string;
  lastName: string;
}
 
function greeter(person: Person) {
  return "Hello, " + person.firstName + " " + person.lastName;
}
 
let user = { firstName: "Jane", lastName: "User" };
 
document.body.textContent = greeter(user);
```


在ts中获取到页面元素后最好将其转为特定的类，否则访问某些属性时会报错

```ts
let btn: HTMLInputElement = document.getElementById("btn") as HTMLInputElement;
btn.onclick = () => {
    let btn_info = document.getElementById("btn_info");
    if (btn_info != null) {
        if (btn.checked) {
            btn_info.innerText = "选中";
        } else {
            btn_info.innerText = "未选中";
        }
    }
}
```


# Node.js

**Node.js** 是一个基于 **Chrome V8 引擎** 的 **JavaScript 运行环境**，它的核心作用是让 JavaScript 不仅能在浏览器中运行，也能在 **服务器端** 运行，即用JavaScript写后端。

Node.js可以用于编写Web服务器、编写实时应用、命令行工具和跨平台应用等。

可以使用`node main.js`直接运行js文件

## 基础操作


### 文件操作

使用fs模块

```js
// import { sample_rate, read_audio } from "./audio_utils.js";

// console.log(sample_rate);

// read_audio("audio.mp3");

import { readFile, writeFile, stat } from 'node:fs';

let data = "hello world";
writeFile("test.txt", data, function(err) {
    if (err) {
        console.log(err);
    }
})

readFile("test.txt", function (err, data) {
    if (err) {
        console.log(err);
    }else{
        const uint8Array = new Uint8Array(data);
        const decoder = new TextDecoder("utf-8");
        console.log(decoder.decode(uint8Array));
    }
})

stat("test.txt", function(err, st){
    if (err) {
        console.log(err);
    }else{
        console.log(st.isFile());
    }
});
```

