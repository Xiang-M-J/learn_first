
## 创建项目

使用node.js，在工作目录下执行命令

```sh
npm create vue@latest
```

或者（推荐）

```sh
cnpm create vue@latest
```

创建时唯一需要注意的是项目名 `<your-project-name>`，后面的添加各项支持（TypeScript，JSX等）可以全部选否。运行项目执行下面的命令

```sh
cd <your-project-name>
npm install
npm run dev
```

如果想要将应用发布到生产环境时，运行下面的命令：

```sh
npm run build
```

此命令会在 `./dist` 文件夹中为你的应用创建一个生产环境的构建版本。



## 基本语法

Vue使用了一种基于HTML的模板语法，使我们能够声明式地将其组件实例的数据绑定到呈现的 DOM 上。

### 文本插值

最基本的数据绑定是文本插值，直接使用`{{ value }}`在html中插入文本

```vue
<script>
export default {
  data() {
    return {
      message: 'Hello World!',
      counter: {
        count: 0
      }
    }
  }
}
</script>

<template>
  <h1>{{ message }}</h1>
  <p>Count is: {{ counter.count }}</p>
</template>
```

此时插值只会插入纯文本，如果想要插入html，则需要插入`v-html`指令。

```vue
<script>
export default {
    data() {
        return {
            raw_html: "<span style=\"color: red\">This should be red.</span>"
        }
    },

}
</script>

<template>
  <!-- 使此按钮生效 -->
    <h1>{{raw_html}}</h1>
    <h1><span v-html="raw_html"></span></h1>
</template>
```



### 属性绑定

双大括号不能在HTML attributes中使用，想要响应式地绑定一个 attribute，应该使用 `v-bind` 指令：

template

```vue
<div v-bind:id="dynamicId"></div>
```

`v-bind` 指令指示 Vue 将元素的 `id` attribute 与组件的 `dynamicId` 属性保持一致。如果绑定的值是 `null` 或者 `undefined`，那么该 attribute 将会从渲染的元素上移除。

`v-bind` 的简写写法为

```vue
<div :id="dynamicId"></div>
```

这里的id可以是class，id等等，如下面的例子为h1标签动态绑定了一个类

```vue
<script>
export default {
  data() {
    return {
      titleClass: 'title'
    }
  }
}
</script>

<template>
  <h1 :class="titleClass">Make me red</h1>
</template>

<style>
.title {
  color: red;
}
</style>
```

> 绑定支持完整的JavaScript表达式（条件控制语句不支持，但是三元表达式支持）

如果想要有条件地渲染某个class，可以使用三元表达式

```vue
<div :class="[isActive ? activeClass : '', errorClass]"></div>
```

或者更简洁的写法：

```vue
<div :class="[{ active: isActive }, errorClass]"></div>
```



### 事件监听

一个按钮点击后发生的事件可以使用`v-on:click`（简写为`@click`）来绑定。下面的代码便将`increment`函数绑定到按钮上。

```vue
<script>
export default {
  data() {
    return {
      count: 0
    }
  },
  methods: {
    increment() {
      this.count++
    }
  }
}
</script>

<template>
  <button @click="increment">count is: {{ count }}</button>
</template>
```

这里的click可以换成其它的事件，如`focus`。

如果需要将一个函数绑定到动态的事件名称上，则要将事件名包含在方括号中，同样也适用于属性绑定

```vue
<a :[attributeName]="url"> ... </a>
<a @[eventName]="doSomething"> ... </a>
```



有时我们需要在内联事件处理器中访问原生 DOM 事件。你可以向该处理器方法传入一个特殊的 `$event` 变量，或者使用内联箭头函数：

```vue
<script>
export default {
    methods: {
      warn(message, event) {
        // 这里可以访问 DOM 原生事件
        if (event) {
          event.preventDefault()
        }
        alert(message)
      }
    }
}
</script>

<template>
    <!-- 使用特殊的 $event 变量 -->
    <button @click="warn('Form cannot be submitted yet.', $event)">
      Submit
    </button>

    <!-- 使用内联箭头函数 -->
    <button @click="(event) => warn('Form cannot be submitted yet.', event)">
      Submit
    </button>
</template>
```



在处理事件时调用 `event.preventDefault()` 或 `event.stopPropagation()` 是很常见的。尽管我们可以直接在方法内调用，但如果方法能更专注于数据逻辑而不用去处理 DOM 事件的细节会更好。

为解决这一问题，Vue 为 `v-on` 提供了**事件修饰符**。修饰符是用 `.` 表示的指令后缀，包含以下这些：

`.stop`、`.prevent`、`.self`、`.capture`、`.once`、`.passive`

```vue
<!-- 单击事件将停止传递 -->
<a @click.stop="doThis"></a>

<!-- 提交事件将不再重新加载页面 -->
<form @submit.prevent="onSubmit"></form>

<!-- 修饰语可以使用链式书写 -->
<a @click.stop.prevent="doThat"></a>

<!-- 也可以只有修饰符 -->
<form @submit.prevent></form>

<!-- 仅当 event.target 是元素本身时才会触发事件处理器 -->
<!-- 例如：事件处理器不来自子元素 -->
<div @click.self="doThat">...</div>
```

`.capture`、`.once` 和 `.passive` 修饰符与[原生 `addEventListener` 事件](https://developer.mozilla.org/zh-CN/docs/Web/API/EventTarget/addEventListener#options)相对应：

```vue
<!-- 添加事件监听器时，使用 `capture` 捕获模式 -->
<!-- 例如：指向内部元素的事件，在被内部元素处理前，先被外部处理 -->
<div @click.capture="doThis">...</div>

<!-- 点击事件最多被触发一次 -->
<a @click.once="doThis"></a>

<!-- 滚动事件的默认行为 (scrolling) 将立即发生而非等待 `onScroll` 完成 -->
<!-- 以防其中包含 `event.preventDefault()` -->
<!-- 一般用于触摸事件的监听器，可以用来改善移动端设备的滚屏性能。 -->
<div @scroll.passive="onScroll">...</div> 
```

除了上面的修饰符，还有按键、鼠标修饰符等。



### 表单绑定

同时使用`v-bind`和`v-on`来在表单的输入元素上创建双向绑定

```vue
<script>
export default {
  data() {
    return {
      text: ''
    }
  },
  methods: {
    onInput(e) {
      this.text = e.target.value
    }
  }
}
</script>

<template>
  <input :value="text" @input="onInput" placeholder="Type here">
  <p>{{ text }}</p>
</template>
```

这里可以使用`v-model`指令来简化双向绑定，上面的代码可以简化为

```vue
<script>
export default {
  data() {
    return {
      text: ''
    }
  }
}
</script>

<template>
  <input v-model="text" placeholder="Type here">
  <p>{{ text }}</p>
</template>
```

另外，`v-model` 还可以用于各种不同类型的输入，`<textarea>`、`<select>` 元素。

对于自定义组件，实现 `v-model` 需要做两件事：

1. 将内部原生 `<input>` 元素的 `value` attribute 绑定到 `modelValue` prop
2. 当原生的 `input` 事件触发时，触发一个携带了新值的 `update:modelValue` 自定义事件

```vue
<!-- CustomInput.vue -->
<script>
export default {
  props: ['modelValue'],
  emits: ['update:modelValue']
}
</script>

<template>
  <input
    :value="modelValue"
    @input="$emit('update:modelValue', $event.target.value)"
  />
</template>
```

```vue
<!-- 父组件 -->
<CustomInput v-model="searchText" />
```

可以在单个组件实例上创建多个 `v-model` 双向绑定

```vue
<!-- 父组件 -->
<UserName
  v-model:first-name="first"
  v-model:last-name="last"
/>
```

```vue
<!-- 子组件 -->
<script>
export default {
  props: {
    firstName: String,
    lastName: String
  },
  emits: ['update:firstName', 'update:lastName']
}
</script>

<template>
  <input
    type="text"
    :value="firstName"
    @input="$emit('update:firstName', $event.target.value)"
  />
  <input
    type="text"
    :value="lastName"
    @input="$emit('update:lastName', $event.target.value)"
  />
</template>
```

`v-model` 也支持修饰符。



### 条件渲染

使用`v-if`指令来有条件地渲染元素，如

```vue
<h1 v-if="awesome">Vue is awesome!</h1>
```

这个 `<h1>` 标签只会在 awesome 的值为真值 (Truthy) 时渲染。若 awesome 更改为假值 (Falsy)，它将被从 DOM 中移除。

我们也可以使用 `v-else` 和 `v-else-if` 来表示其他的条件分支：

```vue
<h1 v-if="awesome">Vue is awesome!</h1>
<h1 v-else>Oh no 😢</h1>
```

> 注意 `v-if` 可以在 template 上使用

另外一个可以用来按条件显示一个元素的指令是`v-show`，其用法基本一样：

```vue
<h1 v-show="ok">Hello!</h1>
```

不同之处在于 `v-show` 会在 DOM 渲染中保留该元素；`v-show` 仅切换了该元素上名为 `display` 的 CSS 属性。`v-show` 不支持在 `<template>` 元素上使用，也不能和 `v-else` 搭配使用。

> `v-if` 有更高的切换开销，而 `v-show` 有更高的初始渲染开销。因此，如果需要频繁切换，则使用 `v-show` 较好；如果在运行时绑定条件很少改变，则 `v-if` 会更合适。



### 列表渲染

使用 `v-for` 指令来渲染一个基于源数组的列表：

```vue
<ul>
  <li v-for="todo in todos" :key="todo.id">
    {{ todo.text }}
  </li>
</ul>
```

如果想要更新渲染的列表，直接更新原数组即可。添加新元素可以使用`push`，修改和删除数组中的元素可以使用`filter`。

```vue
<script>
// 给每个 todo 对象一个唯一的 id
let id = 0
export default {
  data() {
    return {
      newTodo: '',
      todos: [
        { id: id++, text: 'Learn HTML' },
        { id: id++, text: 'Learn JavaScript' },
        { id: id++, text: 'Learn Vue' }
      ]
    }
  },
  methods: {
    addTodo() {
      this.todos.push({ id: id++, text: this.newTodo })
      this.newTodo = ''
    },
    removeTodo(todo) {
      this.todos = this.todos.filter((t) => t !== todo)
    }
  }
}
</script>
<template>
  <form @submit.prevent="addTodo">
    <input v-model="newTodo">
    <button>Add Todo</button>    
  </form>
  <ul>
    <li v-for="todo in todos" :key="todo.id">
      {{ todo.text }}
      <button @click="removeTodo(todo)">X</button>
    </li>
  </ul>
</template>
```

Vue 能够侦听响应式数组的变更方法，并在它们被调用时触发相关的更新。这些变更方法包括：

- `push()`
- `pop()`
- `shift()`
- `unshift()`
- `splice()`
- `sort()`
- `reverse()`

`v-for`可以直接接受一个整数值，注意这里的n从1开始，一直到10（包括10）。

```vue
<span v-for="n in 10">{{ n }}</span>
```

注意 `v-for` 也可以在template上使用。



### 计算属性

在上一步的 todo 列表基础上继续，给每一个 todo 添加了切换功能。这是通过给每一个 todo 对象添加 `done` 属性来实现的，并且使用了 `v-model` 将其绑定到复选框上。下一个可以添加的改进是隐藏已经完成的 todo。已经有了一个能够切换 `hideCompleted` 状态的按钮。但是应该如何基于状态渲染不同的列表项呢？

可以使用 `computed` 选项声明一个响应式的属性，它的值由其他属性计算而来。下面这段代码中的`filteredTodos`函数便返回了由hideCompleted和done属性计算得到的新数组。

```vue
<script>
let id = 0
export default {
  data() {
    return {
      newTodo: '',
      hideCompleted: false,
      todos: [
        { id: id++, text: 'Learn HTML', done: true },
        { id: id++, text: 'Learn JavaScript', done: true },
        { id: id++, text: 'Learn Vue', done: false }
      ]
    }
  },
  computed: {
    filteredTodos() {
      return this.hideCompleted
        ? this.todos.filter((t) => !t.done)
        : this.todos
    }
  },
  methods: {
    addTodo() {
      this.todos.push({ id: id++, text: this.newTodo, done: false })
      this.newTodo = ''
    },
    removeTodo(todo) {
      this.todos = this.todos.filter((t) => t !== todo)
    }
  }
}
</script>
<template>
  <form @submit.prevent="addTodo">
    <input v-model="newTodo">
    <button>Add Todo</button>
  </form>
  <ul>
    <li v-for="todo in filteredTodos" :key="todo.id">
      <input type="checkbox" v-model="todo.done">
      <span :class="{ done: todo.done }">{{ todo.text }}</span>
      <button @click="removeTodo(todo)">X</button>
    </li>
  </ul>
  <button @click="hideCompleted = !hideCompleted">
    {{ hideCompleted ? 'Show all' : 'Hide completed' }}
  </button>
</template>

<style>
.done {
  text-decoration: line-through;
}
</style>
```



### 生命周期和模板引用

当我们需要手动操作DOM时，此时我们需要模板引用，即指向模板中一个DOM元素的ref。我们需要通过这个特殊的ref属性来实现模板引用。

```vue
<p ref="pElementRef">hello</p>
```

此元素将作为 `this.$refs.pElementRef` 暴露在 `this.$refs` 上。然而，你只能在组件**挂载**之后访问它。要在挂载之后执行代码，我们可以使用 `mounted` 选项：

```vue
export default {
  mounted() {
    // 此时组件已经挂载。
  }
}
```

这被称为**生命周期钩子**——它允许我们注册一个在组件的特定生命周期调用的回调函数。还有一些其他的钩子如 `created` 和 `updated`。更多细节请查阅[生命周期图示](https://cn.vuejs.org/guide/essentials/lifecycle.html#lifecycle-diagram)。

```vue
<script>
export default {
  // ...
  mounted(){
    this.$refs.pElementRef.textContent = "HELLO WORLD"
  }
}
</script>
<template>
  <p ref="pElementRef">hello</p>
</template>
```

`Vue` 的生命周期为

<img src="https://cn.vuejs.org/assets/lifecycle.DLmSwRQE.png">



### 侦听器

当一个属性发生变化时，需要执行某些操作，此时便需要侦听器。

例如，当一个数字改变时将其输出到控制台。我们可以通过侦听器来实现它：

```js
export default {
  data() {
    return {
      count: 0
    }
  },
  watch: {
    count(newCount) {
      console.log(`new count is: ${newCount}`)
    }
    count(newCount, oldCount){
      //
	}
  }
}
```

这里，我们使用 `watch` 选项来侦听 `count` 属性的变化。当 `count` 改变时，侦听回调将被调用，并且接收新值作为参数。



### 组件

父组件可以在模板中渲染另一个组件作为子组件。

```vue
<script>
  	import child from "./ChildComp.vue"
    export default {
      // 先注册子组件
      components:{
        child
      }
    }
</script>

<template>
  <!-- 渲染子组件 -->
  <child />
</template>
```

注意这里的注册是局部注册（更加推荐的一种注册方式）。

### Props

子组件可以通过 **props** 从父组件接受动态数据。首先在子组件中声明其接受的props，

```vue
<!-- ChildComp.vue -->
<script>
export default {
  props: {
    msg: String
  }
}
</script>

<template>
  <h2>{{ msg || 'No props passed yet' }}</h2>
</template>
```

在父组件中可以像声明html 属性一样传递props，若要传递动态值，可以使用`v-bind`语法

```vue
<script>
import ChildComp from './ChildComp.vue'

export default {
  components: {
    ChildComp
  },
  data() {
    return {
      greeting: 'Hello from parent'
    }
  }
}
</script>

<template>
  <ChildComp :msg="greeting" />
</template>
```

如果你想要将一个对象的所有属性都当作 props 传入，你可以使用没有参数的 `v-bind`，即只使用 `v-bind` 而非 `:prop-name`。

```vue
<script>
export default {
  data() {
    return {
      post: {
        id: 1,
        title: 'My Journey with Vue'
      }
    }
  }
}
</script>
<template>
<BlogPost v-bind="post" /> 
<BlogPost :id="post.id" :title="post.title" />
<!-- 上面这两行代码等价 -->
</template>
```

所有的 props 都遵循着**单向绑定**原则，props 因父组件的更新而变化，自然地将新的状态向下流往子组件，而不会逆向传递。另外，每次父组件更新后，所有的子组件中的 props 都会被更新到最新值，这意味着你**不应该**在子组件中去更改一个 prop。

更改prop的需要一般源于下面这两种场景：

1. **prop 被用于传入初始值；而子组件想在之后将其作为一个局部数据属性**。在这种情况下，最好是新定义一个局部数据属性，从 props 上获取初始值即可：

```js
export default {
  props: ['initialCounter'],
  data() {
    return {
      // 计数器只是将 this.initialCounter 作为初始值
      // 像下面这样做就使 prop 和后续更新无关了
      counter: this.initialCounter
    }
  }
}
```

2. **需要对传入的 prop 值做进一步的转换**。在这种情况中，最好是基于该 prop 值定义一个计算属性：

```js
export default {
  props: ['size'],
  computed: {
    // 该 prop 变更时计算属性也会自动更新
    normalizedSize() {
      return this.size.trim().toLowerCase()
    }
  }
}
```

Vue 组件可以更细致地声明对传入的 props 的校验要求。要声明对 props 的校验，可以向 `props` 选项提供一个带有 props 校验选项的对象，如

```js
export default {
  props: {
    // 基础类型检查
    //（给出 `null` 和 `undefined` 值则会跳过任何类型检查）
    propA: Number,
    // 多种可能的类型
    propB: [String, Number],
    // 必传，且为 String 类型
    propC: {
      type: String,
      required: true
    },
    // Number 类型的默认值
    propD: {
      type: Number,
      default: 100
    },
    // 对象类型的默认值
    propE: {
      type: Object,
      // 对象或者数组应当用工厂函数返回。
      // 工厂函数会收到组件所接收的原始 props
      // 作为参数
      default(rawProps) {
        return { message: 'hello' }
      }
    },
    // 自定义类型校验函数
    // 在 3.4+ 中完整的 props 作为第二个参数传入
    propF: {
      validator(value, props) {
        // The value must match one of these strings
        return ['success', 'warning', 'danger'].includes(value)
      }
    },
    // 函数类型的默认值
    propG: {
      type: Function,
      // 不像对象或数组的默认，这不是一个
      // 工厂函数。这会是一个用来作为默认值的函数
      default() {
        return 'Default function'
      }
    }
  }
}
```



### Emits

除了接收 props，子组件还可以向父组件触发事件：

```js
// 在子组件中
export default {
  // 声明触发的事件
  emits: ['response'],
  created() { // 创建时触发的事件
    // 带参数触发
    this.$emit('response', 'hello from child')
  }
}
```

`this.$emit()` 的第一个参数是事件的名称。其他所有参数都将传递给事件监听器。

父组件可以使用 `v-on` 监听子组件触发的事件——这里的处理函数接收了子组件触发事件时的额外参数并将它赋值给了本地状态：

```vue
<ChildComp @response="(msg) => childMsg = msg" />
```

有时候我们会需要在触发事件时附带一个特定的值。在子组件中

```vue
<button @click="$emit('increaseBy', 1)">
  Increase by 1
</button>
```

在父组件中监听事件，

```vue
<MyButton @increase-by="(n) => count += n" />
```



> “透传 attribute”指的是传递给一个组件，却没有被该组件声明为 [props](https://cn.vuejs.org/guide/components/props.html) 或 [emits](https://cn.vuejs.org/guide/components/events.html#defining-custom-events) 的 attribute 或者 `v-on` 事件监听器。最常见的例子就是 `class`、`style` 和 `id`。透传的 attribute 会自动被添加到根元素上，并且会合并。
>
> 假设有一个子组件的模板为
>
> ```vue
> <button class="btn">click me</button>
> ```
>
> 父组件使用了这个组件，并且传入了class，
>
> ```vue
> <MyButton class="large" />
> ```
>
> 则组件的渲染结果为
>
> ```vue
> <button class="btn large">click me</button>
> ```
>
> 注意这个规则也适用于 `v-on` 事件监听器。透传 Attributes可由 `this.$attrs` 访问



### 插槽

除了通过 props 传递数据外，父组件还可以通过**插槽** (slots) 将模板片段传递给子组件。在子组件中，可以使用 `<slot>` 元素作为插槽出口 (slot outlet) 渲染父组件中的插槽内容 (slot content)。`<slot>` 插口中的内容将被当作“默认”内容，在父组件没有传递任何插槽内容时显示。如父组件为

```vue
<template>
  <ChildComp>Message</ChildComp>
</template>
```

子组件为

```vue
<template>
  <slot>Fallback content</slot>
</template>
```

此时显示的便是Message，而如果父组件为

```vue
<template>
  <ChildComp></ChildComp>
</template>
```

此时显示的便是Fallback content。

如果一个组件中需要包含多个插槽出口，`<slot>` 元素可以有一个特殊的 attribute `name`，用来给各个插槽分配唯一的 ID，以确定每一处要渲染的内容：

```vue
<div class="container">
  <header>
    <slot name="header"></slot>
  </header>
  <main>
    <slot></slot>
  </main>
  <footer>
    <slot name="footer"></slot>
  </footer>
</div>
```

这类带 `name` 的插槽被称为具名插槽 (named slots)。没有提供 `name` 的 `<slot>` 出口会隐式地命名为“default”。

要为具名插槽传入内容，我们需要使用一个含 `v-slot` 指令的 `<template>` 元素，并将目标插槽的名字传给该指令：

```vue
<BaseLayout>
  <template v-slot:header>
    <!-- header 插槽的内容放这里 -->
  </template>
</BaseLayout>
```

注意 `v-slot:` 有对应的简写 `#`，因此 `<template v-slot:header>` 可以简写为 `<template #header>`。



### 依赖注入

当需要一个父组件向一个较深的子组件传递数据时，如果使用props，会遇到数据沿着组件链逐级传递的问题，会比较麻烦。此时可以使用依赖（provide）注入（inject）的方法。

provide有两种方式

```js
// 第一种方式
export default {
  provide: {
    message: 'hello!'
  }
}
// 第二种方式
export default {
  data() {
    return {
      message: 'hello!'
    }
  },
  provide() {
    // 使用函数的形式，可以访问到 `this`
    return {
      message: this.message
    }
  }
}
```

除了在组件中提供依赖，还可以在整个应用层提供依赖

```js
import { createApp } from 'vue'
const app = createApp({})
app.provide(/* 注入名 */ 'message', /* 值 */ 'hello!')
```



要注入上层组件提供的数据，需使用 `inject` 选项来声明：

```js
export default {
  inject: ['message'],
  created() {
    console.log(this.message) // injected value
  }
}
```

注入会在组件自身的状态**之前**被解析，因此你可以在 `data()` 中访问到注入的属性。

默认情况下，`inject` 假设传入的注入名会被某个祖先链上的组件提供。如果该注入名的确没有任何组件提供，则会抛出一个运行时警告。

如果在注入一个值时不要求必须有提供者，那么我们应该声明一个默认值，和 props 类似：

```js
export default {
  // 当声明注入的默认值时
  // 必须使用对象形式
  inject: {
    message: {
      from: 'message', // 当与原注入名同名时，这个属性是可选的
      default: 'default value'
    },
    user: {
      // 对于非基础类型数据，如果创建开销比较大，或是需要确保每个组件实例
      // 需要独立数据的，请使用工厂函数
      default: () => ({ name: 'John' })
    }
  }
}
```

如果注入方需要及时响应供给方的变化，我们需要使用 computed() 函数提供一个计算属性：

```js
import { computed } from 'vue'

export default {
  data() {
    return {
      message: 'hello!'
    }
  },
  provide() {
    return {
      // 显式提供一个计算属性
      message: computed(() => this.message)
    }
  }
}
```



### 异步组件

在大型项目中，我们可能需要拆分应用为更小的块，并仅在需要时再从服务器加载相关组件。Vue 提供了 `defineAsyncComponent` 方法来实现此功能：

```js
import { defineAsyncComponent } from 'vue'

const AsyncComp = defineAsyncComponent(() => {
  return new Promise((resolve, reject) => {
    // ...从服务器获取组件
    resolve(/* 获取到的组件 */)
  })
})
// ... 像使用其他一般组件一样使用 `AsyncComp`
```

可以在局部注册组件时使用 `defineAsyncComponent`：

```vue
<script>
import { defineAsyncComponent } from 'vue'

export default {
  components: {
    AdminPage: defineAsyncComponent(() =>
      import('./components/AdminPageComponent.vue')
    )
  }
}
</script>

<template>
  <AdminPage />
</template>
```

异步操作不可避免地会涉及到加载和错误状态，因此 `defineAsyncComponent()` 也支持在高级选项中处理这些状态：

```js
const AsyncComp = defineAsyncComponent({
  // 加载函数
  loader: () => import('./Foo.vue'),

  // 加载异步组件时使用的组件
  loadingComponent: LoadingComponent,
  // 展示加载组件前的延迟时间，默认为 200ms
  delay: 200,

  // 加载失败后展示的组件
  errorComponent: ErrorComponent,
  // 如果提供了一个 timeout 时间限制，并超时了
  // 也会显示这里配置的报错组件，默认值是：Infinity
  timeout: 3000
})
```

