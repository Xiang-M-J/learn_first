
Kotlin 中使用 `val` 标记从值不更改的变量，`var` 标记值可以更改的变量。

Kotlin 中不提供三元运算符，而是使用条件表达式

```kotlin
val answerString: String = if (count == 42) {
    "I have the answer."
} else if (count > 35) {
    "The answer is close."
} else {
    "The answer eludes me."
}

println(answerString)
```

更加复杂的条件赋值使用 when

```kotlin
val answerString = when {
    count == 42 -> "I have the answer."
    count > 35 -> "The answer is close."
    else -> "The answer eludes me."
}

println(answerString)
```


### 函数

基本的函数定义

```kotlin
fun generateAnswerString(name: String): String {
    val answerString = if (count == 42) {
        "$name have the answer."
    } else {
        "The answer eludes me"
    }

    return answerString
}
```

匿名函数

```kotlin
val stringLengthFunc: (String) -> Int = { input ->
    input.length
}
```

函数传参

```kotlin
fun stringMapper(str: String, mapper: (String) -> Int): Int {
    // Invoke function
    return mapper(str)
}
```



### 可变列表

使用 MutableList 

```kotlin
private val byteArray: MutableList<Byte> = mutableListOf()
// 添加元素
byteArray.addAll(bytes.toList())

// 切片
val slice = byteArray.subList(0, length).toByteArray()  

// 删除列表中的部分值
byteArray.subList(0, length).clear()

// 获取列表长度
println(byteArray.size)

// 清空
byteArray.clear()
```


> [!WARNING] 异步操作
> MutableList 不支持异步操作，在读取时写入会报错，可以使用同步锁
> ```kotlin
> private val lock = Any()
> synchronized(lock){  
> 	byteArray.addAll(bytes.toList())  
> }
> ```
>

