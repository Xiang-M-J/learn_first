## 创建React项目

>npm create vite@latest my-app -- --template react-ts

> create-vite 项目名 --template react   (更快、更轻)

> create-react 项目名

## React目录

**主目录：**

- index.html —网页
- package.json —npm包相关信息
- vite.config.js — vite的配置

**public — 静态资源文件夹：**
- favicon.icon — 网站偏爱图标
- logo192.png — logo图
- logo512 — logo图
- manifest.json — 应用加壳的配置文件
- robots.txt — 爬虫协议文件

**src — 源码文件夹：**

- App.css — App组件的样式
- App.jsx — App组件 （重要）
- index.css — 样式
- main.jsx — 入口文件 （重要）



## 基本语法

### 描述UI

React中创建组件直接通过编写函数return出来即可，再在其他函数中作为标签使用。

```jsx
function Square() {
	return (
	<button>hello</button>
	)
}

default function main(){
    return (
    <Square></Square>
    )
}
```

html片段可以通过[HTML to JSX (transform.tools)](https://transform.tools/html-to-jsx) 或者 [HTML to JSX (reactjs.net)](https://magic.reactjs.net/htmltojsx.htm)转为JSX。



> 组件应该是纯粹的，即对于相同的输入，React 组件必须总是返回相同的 JSX。需要保证只使用，而不是改写外部变量

#### 通过大括号使用JavaScript

React中使用引号传递字符串，使用单大括号传递动态属性，使用双大括号传递对象。因为对象本来的表示形式为

```jsx
obj = {
    name: "Hedy Lamarr", 
    inventions: 5 
}
```

所以在引用时再加上一层大括号来传递对象，即双大括号传递对象。

> 内联 `style` 属性 使用驼峰命名法编写。例如，HTML `<ul style="background-color: black">` 在你的组件里应该写成 `<ul style={{ backgroundColor: 'black' }}>`。

#### 将Props传递给组件

React 组件使用 *props* 来互相通信。每个父组件都可以提供 props 给它的子组件，从而将一些信息传递给它。

首先，将一些 props 传递给 `Avatar`。例如，让我们传递两个 props：`person`（一个对象）和 `size`（一个数字）

```jsx
export default function Profile() {
  return (
    <Avatar
      person={{ name: 'Lin Lanying', imageId: '1bX5QH6' }}
      size={100}
    />
  );
}
```

通过在 `function Avatar` 之后直接列出它们的名字 `person, size` 来读取这些 props。这些 props 在 `({` 和 `})` 之间，并由逗号分隔。这样，你可以在 `Avatar` 的代码中使用它们，就像使用变量一样。

```jsx
function Avatar({ person, size }) {
  // 在这里 person 和 size 是可访问的
}
function Avatar({ person, size=100 }) {  // 可设置默认值
}
```

更加简洁的展开

```jsx
function Profile(props) {
  return (
    <div className="card">
      <Avatar {...props} />
    </div>
  );
}
```

当子组件需要使用父组件的一个数据，但是两种之间存在较多的层级关系，可以使用context深层传递参数。

首先，你需要创建这个 context，并 **将其从一个文件中导出**，这样你的组件才可以使用它：

```jsx
// LevelContext.js
import { createContext } from 'react';
export const LevelContext = createContext(1);
```

从 React 中引入 `useContext` Hook 以及你刚刚创建的 context:

```jsx
// 
import { useContext } from 'react';
import { LevelContext } from './LevelContext.js';
```

从刚刚引入的 `LevelContext` 中读取值：

```jsx
// heading.js
import { useContext } from 'react';
import { LevelContext } from './LevelContext.js';

export default function Heading({ children }) {
  const level = useContext(LevelContext);
  switch (level) {
    case 1:
      return <h1>{children}</h1>;
    case 2:
      return <h2>{children}</h2>;
  	// ...
    default:
      throw Error('未知的 level：' + level);
  }
}
```

`useContext` 是一个 Hook。和 `useState` 以及 `useReducer`一样，你只能在 React 组件中（不是循环或者条件里）立即调用 Hook。**`useContext` 告诉 React `Heading` 组件想要读取 `LevelContext`。**

在渲染组件时，用context provider包裹组件

```jsx
// Section.js
import { useContext } from 'react';
import { LevelContext } from './LevelContext.js';

export default function Section({ children }) {
  const level = useContext(LevelContext);
  return (
    <section className="section">
      <LevelContext.Provider value={level + 1}>  // 这里的+1使得标题级别可以自动增加
        {children}
      </LevelContext.Provider>
    </section>
  );
}

```

这告诉 React：“如果在 `<Section>` 组件中的任何子组件请求 `LevelContext`，给他们这个 `level`。”组件会使用 UI 树中在它上层最近的那个 `<LevelContext.Provider>` 传递过来的值。通过访问上层最近的 `Section` 来“断定”它的标题级别：

1. 你将一个 `level` 参数传递给 `<Section>`。
2. `Section` 把它的子元素包在 `<LevelContext.Provider value={level}>` 里面。
3. `Heading` 使用 `useContext(LevelContext)` 访问上层最近的 `LevelContext` 提供的值。



#### 条件渲染

React 中，你可以通过使用 JavaScript 的 `if` 语句、`&&` 和 `? :` 运算符来选择性地渲染 JSX。

```jsx
// if 语句
function Item({ name, isPacked }) {
  if (isPacked) {
    return <li className="item">{name} ✔</li>;
  }
  return <li className="item">{name}</li>;
}

// 使用三目运算符
function Item({ name, isPacked }) {
    return (
    <li className="item">
    	{isPacked ? name + " ✔": name} </li>
    )
}

// 使用 &&
function Item({ name, isPacked }) {
    return (
    <li className="item"> {name} {isPacked && " ✔"} </li>
    )
}

export default function PackingList() {
  return (
    <section>
      <h1>Sally Ride 的行李清单</h1>
      <ul>
        <Item 
          isPacked={true} 
          name="宇航服" 
        />
        <Item 
          isPacked={true} 
          name="带金箔的头盔" 
        />
        <Item 
          isPacked={false} 
          name="Tam 的照片" 
        />
      </ul>
    </section>
  );
}
```



#### 渲染列表

通过 JavaScript 的数组方法 来操作数组中的数据，从而将一个数据集渲染成多个相似的组件。在 React 中使用 `filter()` 筛选需要渲染的组件和使用 `map()` 把数组转换成组件数组。

```jsx
// 使用 map() 把数组转换成组件数组
export default function List() {
  const listItems = people.map(person =>
    <li>{person}</li>
  );
  return <ul>{listItems}</ul>;
}

// 使用 filter() 筛选需要渲染的组件
const chemists = people.filter(person =>
  person.profession === '化学家'
);
```



### 添加交互

在 React 中，随时间变化的数据被称为状态（state）。可以向任何组件添加状态，并按需进行更新。

#### 响应事件

使用 React 可以在 JSX 中添加 **事件处理函数**。其中事件处理函数为自定义函数，它将在响应交互（如点击、悬停、表单输入框获得焦点等）时触发。下面是在Button组件中添加事件处理函数的步骤：

1. 在 `Button` 组件 **内部** 声明一个名为 `handleClick` 的函数。
2. 实现函数内部的逻辑（使用 `alert` 来显示消息）。
3. 添加 `onClick={handleClick}` 到 `<button>` JSX 中。

```jsx
export default function Button() {
  function handleClick() { alert('你点击了我！'); s}
  return (
    <button onClick={handleClick}>点我</button>  // 注意这里handleClick绝对不能带括号
  );
}
```

可以定义 `handleClick` 函数然后将其作为 prop 传入 `<button>`。其中 `handleClick` 是一个 **事件处理函数** 。事件处理函数有如下特点:

- 通常在你的组件 **内部** 定义。
- 名称以 `handle` 开头，后跟事件名称。

事件处理函数可以是内联函数

```jsx
<button onClick={function handleClick() {
  alert('你点击了我！');
    }}></button>
<button onClick={() => {
  alert('你点击了我！');
    }}></button>
```

由于事件处理函数一般在组件内部定义，所以可以直接使用组件的参数。组件的事件处理函数存在传播机制，即触发组件的事件处理函数后，还会触发父组件的事件处理函数。为了解决这一问题，可以使用`e.stopPropagation()`来阻止传播

```jsx
function Button({ onClick, children }) {
  return (
    <button onClick={e => {
      e.stopPropagation();
      onClick();
    }}>
      {children}
    </button>
  );
}

export default function Toolbar() {
  return (
    <div className="Toolbar" onClick={() => {
      alert('你点击了 toolbar ！');
    }}>
      <Button onClick={() => alert('正在播放！')}>
        播放电影
      </Button>
      <Button onClick={() => alert('正在上传！')}>
        上传图片
      </Button>
    </div>
  );
}
```

`e.preventDefault()`可以阻止默认行为，如表单提取后重新加载整个页面的默认行为。



#### State：组件的记忆

React提供了 `useState` Hook实现了两个功能：

1. **State 变量** 用于保存渲染间的数据。
2. **State setter 函数** 更新变量并触发 React 再次渲染组件。

导入语句为

```jsx
import { useState } from 'react';
```

在 React 中，`useState` 以及任何其他以“`use`”开头的函数都被称为 **Hook**。

Hook 是特殊的函数，只在 React 渲染时有效（我们将在下一节详细介绍）。它们能让你 “hook” 到不同的 React 特性中去。

当你调用 `useState` 时，你是在告诉 React 你想让这个组件记住一些东西：

```jsx
const [index, setIndex] = useState(0);
```

在这个例子里，你希望 React 记住 `index`。

`useState` 的唯一参数是 state 变量的**初始值**。在这个例子中，`index` 的初始值被`useState(0)`设置为 `0`。

每次你的组件渲染时，`useState` 都会给你一个包含两个值的数组：

1. **state 变量** (`index`) 会保存上次渲染的值。
2. **state setter 函数** (`setIndex`) 可以更新 state 变量并触发 React 重新渲染组件。

实际发生的情况是：

1. **组件进行第一次渲染。** 因为你将 `0` 作为 `index` 的初始值传递给 `useState`，它将返回 `[0, setIndex]`。 React 记住 `0` 是最新的 state 值。
2. **你更新了 state**。当用户点击按钮时，它会调用 `setIndex(index + 1)`。 `index` 是 `0`，所以它是 `setIndex(1)`。这告诉 React 现在记住 `index` 是 `1` 并触发下一次渲染。
3. **组件进行第二次渲染**。React 仍然看到 `useState(0)`，但是因为 React *记住* 了你将 `index` 设置为了 `1`，它将返回 `[1, setIndex]`。
4. 以此类推！

> State 变量仅用于在组件重渲染时保存信息。在单个事件处理函数中，普通变量就足够了。当普通变量运行良好时，不要引入 state 变量。

当触发一次事件导致界面重绘时，此时state为当前渲染时的state，且**设置 state 只会为下一次渲染变更 state 的值**。如下面的例子中，每一次点击按钮时，state只会加 1。

```jsx
import { useState } from 'react';

export default function Counter() {
  const [number, setNumber] = useState(0);

  return (
    <>
      <h1>{number}</h1>
      <button onClick={() => {
        // 对于下面的三个setNumber而言，此时的number均为当前渲染的number值
        setNumber(number + 1);
        setNumber(number + 1);
        setNumber(number + 1);
        alert(number)  // 此时number不会变化
      }}>+3</button>
    </>
  )
}
```



#### 把一系列 state 更新加入队列

如果你想在下次渲染之前多次更新同一个 state，你可以像 `setNumber(n => n + 1)` 这样传入一个根据队列中的前一个 state 计算下一个 state 的 **函数**，而不是像 `setNumber(number + 1)` 这样传入 **下一个 state 值**。如下面的代码可以使得每次点击按钮都会加 3。

```jsx
import { useState } from 'react';

export default function Counter() {
  const [number, setNumber] = useState(0);

  return (
    <>
      <h1>{number}</h1>
      <button onClick={() => {
        setNumber(n => n + 1);
        setNumber(n => n + 1);
        setNumber(n => n + 1);
      }}>+3</button>
    </>
  )
}
```

在这里，`n => n + 1` 被称为 **更新函数**。当你将它传递给一个 state 设置函数时：

1. React 会将此函数加入队列，以便在事件处理函数中的所有其他代码运行后进行处理。
2. 在下一次渲染期间，React 会遍历队列并给你更新之后的最终 state。

> `setState(x)` 实际上会像 `setState(n => x)` 一样运行



#### 更新 state 中的对象

state 中可以保存任意类型的 JavaScript 值，包括对象。但是，你不应该直接修改存放在 React state 中的对象。相反，当你想要更新一个对象时，你需要创建一个新的对象（或者将其拷贝一份），然后将 state 更新为此对象。如下面的例子中，我们用一个存放在 state 中的对象来表示指针当前的位置。当你在预览区触摸或移动光标时，红色的点本应移动。但是实际上红点仍停留在原处：

```jsx
import { useState } from 'react';
export default function MovingDot() {
  const [position, setPosition] = useState({
    x: 0,
    y: 0
  });
  return (
    <div
      onPointerMove={e => {  // 问题出现在这里
        position.x = e.clientX;
        position.y = e.clientY;
      }}
      style={{
        position: 'relative',
        width: '100vw',
        height: '100vh',
      }}>
      <div style={{
        position: 'absolute',
        backgroundColor: 'red',
        borderRadius: '50%',
        transform: `translate(${position.x}px, ${position.y}px)`,
        left: -10,
        top: -10,
        width: 20,
        height: 20,
      }} />
    </div>
  );
}
```

为了修改上面的例子需要将出问题的代码更换成

```jsx
onPointerMove={e => {
  setPosition({
    x: e.clientX,
    y: e.clientY
  });
}}
```

当 state 中有多个需要更新的数据时，但是每次更新只能更新其中的一个，为了减少编写的代码量，可以使用`...`对象展开语法，

```jsx
setPerson({
  ...person, // 复制上一个 person 中的所有字段
  firstName: e.target.value // 但是覆盖 firstName 字段 
});
```

如果state中有多层的嵌套，如考虑嵌套对象

```jsx
const [person, setPerson] = useState({
  name: 'Niki de Saint Phalle',
  artwork: {
    title: 'Blue Nana',
    city: 'Hamburg',
    image: 'https://i.imgur.com/Sd1AgUOm.jpg',
  }
});
```

此时更新的方式为

```jsx
setPerson({
      ...person,
      artwork: {
        ...person.artwork,
        title: e.target.value
      }
    });
```

更便捷的嵌套展开语法可以使用 [use-immer](https://github.com/immerjs/use-immer) 库。



#### 更新 state 中的数组

数组是另外一种可以存储在 state 中的 JavaScript 对象，它虽然是可变的，但是却应该被视为不可变。同对象一样，当你想要更新存储于 state 中的数组时，你需要创建一个新的数组（或者创建一份已有数组的拷贝值），并使用新数组设置 state。数组的常见操作如下

|          | 避免使用 (会改变原始数组)     | 推荐使用 (会返回一个新数组）  |
| -------- | ----------------------------- | ----------------------------- |
| 添加元素 | `push`，`unshift`             | `concat`，`[...arr]` 展开语法 |
| 删除元素 | `pop`，`shift`，`splice`      | `filter`，`slice`             |
| 替换元素 | `splice`，`arr[i] = ...` 赋值 | `map`                         |
| 排序     | `reverse`，`sort`             | 先将数组复制一份              |

添加元素

```jsx
setArtists( // 替换 state
  [ // 是通过传入一个新数组实现的
    ...artists, // 新数组包含原数组的所有元素
    { id: nextId++, name: name } // 并在末尾添加了一个新的元素（也可在开头添加）
  ]
);
```



### 脱围机制

#### 使用 ref 引用值

当希望组件“记住”某些信息，但又不想让这些信息触发新的渲染时，可以使用 **ref** 。

```jsx
import { useRef } from 'react';

export default function Counter() {
  let ref = useRef(0);

  function handleClick() {
    ref.current = ref.current + 1;
    alert('你点击了 ' + ref.current + ' 次！');
  }

  return (
    <button onClick={handleClick}>
      点击我！
    </button>
  );
}
```

这里的 ref 指向一个数字，但是，像 state 一样，你可以让它指向任何东西：字符串、对象，甚至是函数。与 state 不同的是，ref 是一个普通的 JavaScript 对象，具有可以被读取和修改的 `current` 属性。

请注意，**组件不会在每次递增时重新渲染。** 与 state 一样，React 会在每次重新渲染之间保留 ref。但是，设置 state 会重新渲染组件，更改 ref 不会！

使用 ref 和 state 来实现计时器

```jsx
import { useState, useRef } from 'react';
export default function Stopwatch() {
  const [startTime, setStartTime] = useState(null);
  const [now, setNow] = useState(null);
  const intervalRef = useRef(null);

  function handleStart() {
    setStartTime(Date.now());
    setNow(Date.now());

    clearInterval(intervalRef.current);
    intervalRef.current = setInterval(() => {
      setNow(Date.now());
    }, 10);
  }
  function handleStop() {
    clearInterval(intervalRef.current);
  }
  let secondsPassed = 0;
  if (startTime != null && now != null) {
    secondsPassed = (now - startTime) / 1000;
  }
  return (
    <>
      <h1>时间过去了： {secondsPassed.toFixed(3)}</h1>
      <button onClick={handleStart}>
        开始
      </button>
      <button onClick={handleStop}>
        停止
      </button>
    </>
  );
}
```

以下是 state 和 ref 的对比：

| ref                                                     | state                                                        |
| ------------------------------------------------------- | ------------------------------------------------------------ |
| `useRef(initialValue)`返回 `{ current: initialValue }`  | `useState(initialValue)` 返回 state 变量的当前值和一个 state 设置函数 ( `[value, setValue]`) |
| 更改时不会触发重新渲染                                  | 更改时触发重新渲染。                                         |
| 可变 —— 你可以在渲染过程之外修改和更新 `current` 的值。 | “不可变” —— 你必须使用 state 设置函数来修改 state 变量，从而排队重新渲染。 |
| 你不应在渲染期间读取（或写入） `current` 值。           | 你可以随时读取 state。但是，每次渲染都有自己不变的 state 快照。 |

通常，当你的组件需要“跳出” React 并与外部 API 通信时，你会用到 ref —— 通常是不会影响组件外观的浏览器 API。以下是这些罕见情况中的几个：

- 存储 timeout ID
- 存储和操作 DOM 元素
- 存储不需要被用来计算 JSX 的其他对象。

如果你的组件需要存储一些值，但不影响渲染逻辑，请选择 ref。



#### 使用 ref 操作 DOM

由于 React 会自动处理更新 DOM 以匹配你的渲染输出，因此你在组件中通常不需要操作 DOM。但是，有时你可能需要访问由 React 管理的 DOM 元素 —— 例如，让一个节点获得焦点、滚动到它或测量它的尺寸和位置。在 React 中没有内置的方法来做这些事情，所以你需要一个指向 DOM 节点的 **ref** 来实现。

要访问由 React 管理的 DOM 节点，首先，引入 `useRef` Hook：

```jsx
import { useRef } from 'react';
```

然后，在你的组件中使用它声明一个 ref：

```jsx
const myRef = useRef(null);
```

最后，将 ref 作为 `ref` 属性值传递给想要获取的 DOM 节点的 JSX 标签：

```jsx
<div ref={myRef}>
```

`useRef` Hook 返回一个对象，该对象有一个名为 `current` 的属性。最初，`myRef.current` 是 `null`。当 React 为这个 `<div>` 创建一个 DOM 节点时，React 会把对该节点的引用放入 `myRef.current`。然后，你可以从 [事件处理器](https://zh-hans.react.dev/learn/responding-to-events) 访问此 DOM 节点，并使用在其上定义的内置[浏览器 API](https://developer.mozilla.org/docs/Web/API/Element)。

```jsx
// 你可以使用任意浏览器 API，例如：
myRef.current.scrollIntoView();
```

如果你尝试将 ref 放在 **你自己的** 组件上，例如 `<MyInput />`，默认情况下你会得到 `null`。发生这种情况是因为默认情况下，React 不允许组件访问其他组件的 DOM 节点。甚至自己的子组件也不行！这是故意的。Refs 是一种脱围机制，应该谨慎使用。手动操作 **另一个** 组件的 DOM 节点会使你的代码更加脆弱。相反，**想要**暴露其 DOM 节点的组件必须**选择**该行为。一个组件可以指定将它的 ref “转发”给一个子组件。下面是 `MyInput` 如何使用 `forwardRef` API：

```jsx
import { forwardRef, useRef } from 'react';

const MyInput = forwardRef((props, ref) => {
  return <input {...props} ref={ref} />;
});

export default function Form() {
  const inputRef = useRef(null);

  function handleClick() {
    inputRef.current.focus();
  }

  return (
    <>
      <MyInput ref={inputRef} />
      <button onClick={handleClick}>
        聚焦输入框
      </button>
    </>
  );
}
```





## 代码示例

### 导出函数

```jsx
export default function Square() {
  return <button className="square">X</button>;
}
```

The first line defines a function called `Square`. The `export` JavaScript keyword makes this function accessible outside of this file. The `default` keyword tells other files using your code that it’s the main function in your file.

### 值传递（函数传递也一样）

```jsx
function Square({ value }) {
  return <button className="square">{value}</button>;
}

// 值传递，函数传递
function Square({value, onSquareClick}) {
	return (
	<button className='square' onClick={onSquareClick}>{value}</button>
	)
}
// 使用
<Square value="1"/>
```

### for Each

```jsx
function ProductTable({ products, filterText, inStockOnly }) {
    const rows = [];
    let lastCategory = null;

    products.forEach(
        (product) => 
        {
        if (product.name.toLowerCase().indexOf(
                filterText.toLowerCase()) === -1		// 商品名中没有要查找的部分
        ) 
        {
            return;
        }
        if (inStockOnly && !product.stocked)
        {
            return;
        }
        if (product.category !== lastCategory) 
        {
            rows.push(
                <ProductCategoryRow
                    category={product.category}
                    key={product.category} />
            );
        }
        rows.push(
            <ProductRow
                product={product}
                key={product.name} />
        );
        lastCategory = product.category;
    }
    );
    return (
        <table>
            <thead>
            <tr>
                <th>Name</th>
                <th>Price</th>
            </tr>
            </thead>
            <tbody>{rows}</tbody>
        </table>
    );
}
```

