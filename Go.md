[Go Packages - Go Packages](https://pkg.go.dev/)

**执行文件**

```powershell
go run hello.go
```

**编译文件**

```powershell
go build hello.go & ./hello
```

**格式化文件**

```powershell
gofmt main.go
```

该命令会直接输出格式化后的代码，可以先保存在临时文件中，再修改后缀名

**注释**

与 C 相同，支持 `//` 行注释，`/**/` 块注释

**分割**

Go 支持 `;` 分割每一行，但不严格要求，可以不加

**条件判断**

Go 的条件判断中的条件不用加括号，和 Python 类似

**循环**

Go 中的循环有类似 C 语言的形式，也有类似 Python 的形式，不用加括号，Go 也支持使用 `_` 来表示后面无需使用的值

**位操作**

`&^` 可能是 Go 中特有的位操作符，`a &^ b` 等于 `a|b - b`


**基础的示例**

```go
package main

import "fmt"

func main()  {
	fmt.Println("hello")
}
```



## Go by Example

https://gobyexample.com/


### 变量

使用 var 声明变量（1 个或多个），Go 会自动推断变量类型，但是也可以指定

类型指定语法可以用 `:=` 表示，下面这两句等价

```go
var a int = 10
b := 10
var c,d

a, b = 10, 20   // 变量同时赋值
```


为变量分配空间可以使用 new 或者 make，new 在使用时不会初始化内存，new(T) 分配 0 字节，只会返回地址

```go
type SyncedBuffer struct {
    lock    sync.Mutex
    buffer  bytes.Buffer
}
p := new(SyncedBuffer)  // type *SyncedBuffer
var v SyncedBuffer      // type  SyncedBuffer
```

make 与 new 不同，只用于创建 slices、maps 和 channels，会返回一个初始化空间

```go
package main

import (
    "fmt"
)

func main() {
    a := make([]int, 10, 50)
    fmt.Println(a)
    fmt.Println(len(a))     // 长度为 10
    fmt.Println(cap(a))     // 容量为 50
}
```

**获取环境变量**

```go
var (
    home   = os.Getenv("HOME")
    user   = os.Getenv("USER")
    gopath = os.Getenv("GOPATH")
)
```


**深拷贝**

```go
func (s Sequence) Copy() Sequence {
    copy := make(Sequence, 0, len(s))
    return append(copy, s...)
}


```





### 循环



```go
package main

import "fmt"

func main() {

    i := 1
    for i <= 3 {
        fmt.Println(i)
        i = i + 1
    }

    for j := 0; j < 3; j++ {
        fmt.Println(j)
    }

    for i := range 3 {
        fmt.Println("range", i)
    }

    for {
        fmt.Println("loop")
        break
    }

    for n := range 6 {
        if n%2 == 0 {
            continue
        }
        fmt.Println(n)
    }
}
```

> range 将数字聚成一个切片，range 列表和字符串会返回 index 和值，在字典上range，则会返回键和值

```go
for key, value := range oldMap {
    newMap[key] = value
}
```


### 条件

条件判断的基本语句类似 C 语言，但是不需要括号包括条件

```go
if num := 9; num < 0 {
} else if num < 10 {
} else {
}
```

&& 表示与，|| 表示或

另外一类语句为 switch case

```go
i := 2
fmt.Print("Write ", i, " as ")
switch i {
    case 1:
    fmt.Println("one")
    case 2:
    fmt.Println("two")
    case 3:
    fmt.Println("three")
}

switch time.Now().Weekday() {
    case time.Saturday, time.Sunday:
    fmt.Println("It's the weekend")
    default:
    fmt.Println("It's a weekday")
}

t := time.Now()
switch {
    case t.Hour() < 12:
    fmt.Println("It's before noon")
    default:
    fmt.Println("It's after noon")
}

whatAmI := func(i interface{}) {
    switch t := i.(type) {
        case bool:
        fmt.Println("I'm a bool")
        case int:
        fmt.Println("I'm an int")
        default:
        fmt.Printf("Don't know type %T\n", t)
    }
}
whatAmI(true)
whatAmI(1)
whatAmI("hey")
```


### 字符串

#### 字符串函数

```go
package main

import (
    "fmt"
    "strings"
)
var p = fmt.Println
func main() {
    p("Contains:  ", s.Contains("test", "es"))
    p("Count:     ", s.Count("test", "t"))
    p("HasPrefix: ", s.HasPrefix("test", "te"))
    p("HasSuffix: ", s.HasSuffix("test", "st"))
    p("Index:     ", s.Index("test", "e"))
    p("Join:      ", s.Join([]string{"a", "b"}, "-"))
    p("Repeat:    ", s.Repeat("a", 5))
    p("Replace:   ", s.Replace("foo", "o", "0", -1))
    p("Replace:   ", s.Replace("foo", "o", "0", 1))
    p("Split:     ", s.Split("a-b-c-d-e", "-"))
    p("ToLower:   ", s.ToLower("TEST"))
    p("ToUpper:   ", s.ToUpper("test"))
}
```

#### 字符串格式化

类似 C 语言的 printf

%v 输出值，%+v 输出键值对，%#v 输出类型和键值对，%T 输出类型，%t 输出 bool 值，%d 输出数值，%b 输出二进制，%c 输出字符，%x 输出十六进制，

```go
package main

import (
    "fmt"
    "os"
)
type point struct {
    x, y int
}
func main() {
    p := point{1, 2}
    fmt.Printf("struct1: %v\n", p)     // {1 2}
    fmt.Printf("struct2: %+v\n", p)    // {x:1 y:2}
    fmt.Printf("struct3: %#v\n", p)    // main.point{x:1, y:2}
    fmt.Printf("type: %T\n", p)        // main.point
    fmt.Printf("bool: %t\n", true)     // 
    fmt.Printf("int: %d\n", 123)
    fmt.Printf("bin: %b\n", 14)
    fmt.Printf("char: %c\n", 33)
    fmt.Printf("hex: %x\n", 456)
    fmt.Printf("float1: %f\n", 78.9)
    fmt.Printf("float2: %e\n", 123400000.0)
    fmt.Printf("float3: %E\n", 123400000.0)
    fmt.Printf("str1: %s\n", "\"string\"")
    fmt.Printf("str2: %q\n", "\"string\"")
    fmt.Printf("str3: %x\n", "hex this")
    fmt.Printf("pointer: %p\n", &p)
    fmt.Printf("width1: |%6d|%6d|\n", 12, 345)
    fmt.Printf("width2: |%6.2f|%6.2f|\n", 1.2, 3.45)
    fmt.Printf("width3: |%-6.2f|%-6.2f|\n", 1.2, 3.45)
    fmt.Printf("width4: |%6s|%6s|\n", "foo", "b")
    fmt.Printf("width5: |%-6s|%-6s|\n", "foo", "b")
    s := fmt.Sprintf("sprintf: a %s", "string")
    fmt.Println(s)
    fmt.Fprintf(os.Stderr, "io: an %s\n", "error")
}
```


#### 文本模板

通过文本模板 text/template，可以自定义输出格式，此外还有 html/template，可以用于生成 HTML。

```go
package main

import (
    "os"
    "text/template"
)
func main() {
    t1 := template.New("t1")
    t1, err := t1.Parse("Value is {{.}}\n")
    if err != nil {
        panic(err)
    }
    t1 = template.Must(t1.Parse("Value: {{.}}\n"))
    t1.Execute(os.Stdout, "some text")
    t1.Execute(os.Stdout, 5)
    t1.Execute(os.Stdout, []string{
        "Go",
        "Rust",
        "C++",
        "C#",
    })
    Create := func(name, t string) *template.Template {
        return template.Must(template.New(name).Parse(t))
    }
    
    t2 := Create("t2", "Name: {{.Name}}\n")
    t2.Execute(os.Stdout, struct {
        Name string
    }{"Jane Doe"})
    t2.Execute(os.Stdout, map[string]string{
        "Name": "Mickey Mouse",
    })
    
	// if else 用于判断， - 可以删除空格
    t3 := Create("t3",
        "{{if . -}} yes {{else -}} no {{end}}\n")
    t3.Execute(os.Stdout, "not empty")
    t3.Execute(os.Stdout, "")

    t4 := Create("t4",
        "Range: {{range .}}{{.}} {{end}}\n")
    t4.Execute(os.Stdout,
        []string{
            "Go",
            "Rust",
            "C++",
            "C#",
        })
}
```



### 数组

数组的定义与其它的语言比较不同

```go
var a [5]int    // 默认全为0
b := [5]int{1, 2, 3, 4, 5}  
b = [...]int{1, 2, 3, 4, 5}  // ... 让编译器自己计算
b := [...]int{100, 3: 400, 500}  // 100 0 0 400 500
```

二维数组的定义如下

```go
var twoD [2][3]int
for i := 0; i < 2; i++ {
    for j := 0; j < 3; j++ {
        twoD[i][j] = i + j
    }
}
fmt.Println("2d: ", twoD)

twoD = [2][3]int{
    {1, 2, 3},
    {1, 2, 3},
}
```


计算数组之和

```go
package main

import (
    "fmt"
)
func Sum(a *[3]float64) (sum float64) {
    for _, v := range *a {
        sum += v
    }
    return
}
func main() {
    arr := [...]float64{7.0, 8.5, 9.1}
    x := Sum(&arr)
    fmt.Println(x)
}
```


### 字典

```go
m := make(map[string] int)   // 创建字典
m["k1"] = 7
m["k2"] = 13
delete(m, "k1")    // 删除键值对
clear(m)		// 清除字典
_, prs := m["k2"]

n := map[string]int{"foo": 1, "bar": 2}  // 创建字典
```



### 函数

```go
func plus(a int, b int) int {
    return a + b
}
func plusPlus(a, b, c int) int {
    return a + b + c
}

// 返回多个值，和 Python 类似
func swap(a, b int) (int, int){
    return b, a
}

// 不定参数
func sum(nums ...int) {
    fmt.Print(nums, " ")
    total := 0
    for _, num := range nums {
        total += num
    }
    fmt.Println(total)
}

func append(slice []T, elements ...T) []T

x = append(x, y...)
```




Go 支持匿名函数，可以形成闭包

```go
package main

import "fmt"

func intSeq() func() int {
    i := 0
    return func() int {
        i++
        return i
    }
}

func main() {
    nextInt := intSeq()
    fmt.Println(nextInt())     // 1
    fmt.Println(nextInt())     // 2
    fmt.Println(nextInt())     // 3

    newInts := intSeq()
    fmt.Println(newInts())     // 1
}
```


### 指针

指针用法和 C 类似

```go
package main

import "fmt"

func zeroval(ival int) {
    ival = 0
}

func zeroptr(iptr *int) {
    *iptr = 0
}

func main() {
    i := 1
    fmt.Println("initial:", i)   // 1

    zeroval(i)
    fmt.Println("zeroval:", i)   // 1

    zeroptr(&i)
    fmt.Println("zeroptr:", i)   // 0

    fmt.Println("pointer:", &i)  // i 的地址
}
```


### 结构

使用 type xxx struct 定义结构体

```go
package main

import "fmt"

type person struct {
    name string
    age  int
}

func newPerson(name string) *person {

    p := person{name: name}
    p.age = 42
    return &p
}

func main() {

    fmt.Println(person{"Bob", 20})

    fmt.Println(person{name: "Alice", age: 30})

    fmt.Println(person{name: "Fred"})

    fmt.Println(&person{name: "Ann", age: 40})

    fmt.Println(newPerson("Jon"))

    s := person{name: "Sean", age: 50}
    fmt.Println(s.name)

    sp := &s
    fmt.Println(sp.age)

    sp.age = 51
    fmt.Println(sp.age)

    dog := struct {
        name   string
        isGood bool
    }{
        "Rex",
        true,
    }
    fmt.Println(dog)
}
```

可以为结构体定义方法

```go
package main

import "fmt"

type rect struct {
    width, height int
}

func (r *rect) area() int {
    return r.width * r.height
}

func (r rect) perim() int {
    return 2*r.width + 2*r.height
}

func main() {
    r := rect{width: 10, height: 5}

    fmt.Println("area: ", r.area())
    fmt.Println("perim:", r.perim())

    rp := &r
    fmt.Println("area: ", rp.area())
    fmt.Println("perim:", rp.perim())
}
```

Go 提供了接口作为方法签名的集合

```go
package main

import (
    "fmt"
    "math"
)

// 定义了一个几何形状的基础接口
type geometry interface {
    area() float64
    perim() float64
}

type rect struct {
    width, height float64
}
type circle struct {
    radius float64
}

func (r rect) area() float64 {
    return r.width * r.height
}
func (r rect) perim() float64 {
    return 2*r.width + 2*r.height
}

func (c circle) area() float64 {
    return math.Pi * c.radius * c.radius
}
func (c circle) perim() float64 {
    return 2 * math.Pi * c.radius
}

func measure(g geometry) {
    fmt.Println(g)
    fmt.Println(g.area())
    fmt.Println(g.perim())
}

func main() {
    r := rect{width: 3, height: 4}
    c := circle{radius: 5}

    measure(r)
    measure(c)
}
```

### 推迟执行

defer 用来推迟函数的执行，如推迟文件的关闭

```go
package main

import (
    "fmt"
    "os"
)

func main() {
    f := createFile("/tmp/defer.txt")
    defer closeFile(f)
    writeFile(f)    // 在写完文件后，再执行 closeFile(f)
}

func createFile(p string) *os.File {
    fmt.Println("creating")
    f, err := os.Create(p)
    if err != nil {
        panic(err)
    }
    return f
}

func writeFile(f *os.File) {
    fmt.Println("writing")
    fmt.Fprintln(f, "data")
}

func closeFile(f *os.File) {
    fmt.Println("closing")
    err := f.Close()
    if err != nil {
        fmt.Fprintf(os.Stderr, "error: %v\n", err)
        os.Exit(1)
    }
}
```


### 错误

使用 errors 包抛出一个错误 errors.New("提示错误")

```go
package main

import (
    "errors"
    "fmt"
)
func f(arg int) (int, error) {
    if arg == 42 {
        return -1, errors.New("can't work with 42")
    }
    return arg + 3, nil
}
```

定义一个错误：var ErrOutOfTea = fmt.Errorf("no more tea available")

```go
var ErrOutOfTea = fmt.Errorf("no more tea available")
var ErrPower = fmt.Errorf("can't boil water")

func makeTea(arg int) error {
    if arg == 2 {
        return ErrOutOfTea
    } else if arg == 4 {

        return fmt.Errorf("making tea: %w", ErrPower)
    }
    return nil
}
```

判断错误类型 errors.Is(err, ErrOutOfTea)

```go
func main() {
    for i := range 5 {
        if err := makeTea(i); err != nil {
            if errors.Is(err, ErrOutOfTea) {
                fmt.Println("We should buy new tea!")
            } else if errors.Is(err, ErrPower) {
                fmt.Println("Now it is dark.")
            } else {
                fmt.Printf("unknown error: %s\n", err)
            }
            continue
        }
        fmt.Println("Tea is ready!")
    }
}
```


使用 panic 可以引发一个错误

```go
package main
import "os"
func main() {
    panic("a problem")
    _, err := os.Create("/tmp/file")
    if err != nil {
        panic(err)
    }
}
```


如果想从 panic 恢复回来，可以使用 recover + defer

```go
package main

import "fmt"

func mayPanic() {
    panic("a problem")
}

func main() {

    defer func() {
        if r := recover(); r != nil {
            fmt.Println("Recovered. Error:\n", r)
        }
    }()
    mayPanic()
    fmt.Println("After mayPanic()")
}
```

### 并行

#### Goroutines

一个轻量级的线程，定义一个函数，然后使用 go 调用

```go
package main

import (
    "fmt"
    "time"
)

func f(from string) {
    for i := 0; i < 3; i++ {
        fmt.Println(from, ":", i)
    }
}

func main() {

    f("direct")    // 直接调用

    go f("goroutine")  // 在线程中调用

    go func(msg string) {   // go 可以调用匿名函数
        fmt.Println(msg)
    }("going")

    time.Sleep(time.Second)
    fmt.Println("done")
}
```

执行结果如下：

```txt
direct : 0
direct : 1
direct : 2
going
goroutine : 0
goroutine : 1
goroutine : 2
done
```


#### Channels

如何希望两个 goruntine 之间相互通信，可以使用 channel

```go
package main

import "fmt"

func main()  {
	message := make(chan string)
	
	go func() {
		message <- "ping"
	}()

	msg := <-message
	fmt.Println(msg)
}
```


#### 并行计算

```go
type Vector []float64

// Apply the operation to v[i], v[i+1] ... up to v[n-1].
func (v Vector) DoSome(i, n int, u Vector, c chan int) {
    for ; i < n; i++ {
        v[i] += u.Op(v[i])
    }
    c <- 1    // signal that this piece is done
}
```

对上述函数进行并行计算，将整个计算分配到不同的 CPU 上进行计算

```go
const numCPU = 4 // number of CPU cores

func (v Vector) DoAll(u Vector) {
    c := make(chan int, numCPU)  // Buffering optional but sensible.
    for i := 0; i < numCPU; i++ {
        go v.DoSome(i*len(v)/numCPU, (i+1)*len(v)/numCPU, u, c)
    }
    // Drain the channel.
    for i := 0; i < numCPU; i++ {
        <-c    // wait for one task to complete
    }
    // All done.
}
```



#### WaitGroup

如果需要等待多个线程结束，可以使用 waitgroup

```go
package main

import (
    "fmt"
    "sync"
    "time"
)

func worker(id int) {
    fmt.Printf("Worker %d starting\n", id)

    time.Sleep(time.Second)
    fmt.Printf("Worker %d done\n", id)
}

func main() {

    var wg sync.WaitGroup

    for i := 1; i <= 3; i++ {
        wg.Add(1)

        go func() {
            defer wg.Done()   // 这里需要推迟 wg.Done()，否则后面会发生死锁问题
            worker(i)
        }()
    }
	fmt.Println("waiting")
    wg.Wait() 
	fmt.Println("All Done")
}
```

输出

```
waiting
Worker 3 starting
Worker 1 starting
Worker 2 starting
Worker 2 done
Worker 1 done
Worker 3 done
All Done
```


#### Rate Limiting

在使用资源时有时需要使用 limiter 控制资源的使用速率，下面的例子使用 limiter 每200毫秒发送一次请求

```go
package main

import (
    "fmt"
    "time"
)

func main() {

    requests := make(chan int, 5)
    for i := 1; i <= 5; i++ {
        requests <- i
    }
    close(requests)

    limiter := time.Tick(200 * time.Millisecond)

    for req := range requests {
        <-limiter
        fmt.Println("request", req, time.Now())
    }
}
```

有时候，允许请求量爆发，下面的 burstyLimiter 会允许请求量爆发一次，请求 3 次

```go
burstyLimiter := make(chan time.Time, 3)

for i := 0; i < 3; i++ {
	burstyLimiter <- time.Now()
}

go func() {
	for t := range time.Tick(200 * time.Millisecond) {
		burstyLimiter <- t
	}
}()

burstyRequests := make(chan int, 5)
for i := 1; i <= 5; i++ {
	burstyRequests <- i
}
close(burstyRequests)
for req := range burstyRequests {
	<-burstyLimiter
	fmt.Println("request", req, time.Now())
}
```


#### Atomic Counters

对于简单的状态管理，可以使用 Atomic Counters

```go
package main

import (
    "fmt"
    "sync"
    "sync/atomic"
)

func main() {

    var ops atomic.Uint64
    var wg sync.WaitGroup
    for i := 0; i < 50; i++ {
        wg.Add(1)

        go func() {
            for c := 0; c < 1000; c++ {
                ops.Add(1)
            }
            wg.Done()
        }()
    }

    wg.Wait()

    fmt.Println("ops:", ops.Load())   // 50000
}
```


#### Mutexes

更加复杂的状态管理使用 mutex

```go
package main

import (
    "fmt"
    "sync"
)

type Container struct {
    mu       sync.Mutex
    counters map[string]int
}

func (c *Container) inc(name string) {

    c.mu.Lock()
    defer c.mu.Unlock()
    c.counters[name]++
}

func main() {
    c := Container{
        counters: map[string]int{"a": 0, "b": 0},
    }

    var wg sync.WaitGroup

    doIncrement := func(name string, n int) {
        for i := 0; i < n; i++ {
            c.inc(name)
        }
        wg.Done()
    }

    wg.Add(3)
    go doIncrement("a", 10000)
    go doIncrement("a", 10000)
    go doIncrement("b", 10000)

    wg.Wait()
    fmt.Println(c.counters)
}
```



#### Stateful Goroutines


除了 mutex，另一种选择是使用 goroutine 和通道的内置同步特性来实现相同的效果。

```go
package main

import (
    "fmt"
    "math/rand"
    "sync/atomic"
    "time"
)

type readOp struct {
    key  int
    resp chan int
}
type writeOp struct {
    key  int
    val  int
    resp chan bool
}

func main() {

    var readOps uint64
    var writeOps uint64

    reads := make(chan readOp)
    writes := make(chan writeOp)

    go func() {
        var state = make(map[int]int)
        for {
            select {
            case read := <-reads:
                read.resp <- state[read.key]
            case write := <-writes:
                state[write.key] = write.val
                write.resp <- true
            }
        }
    }()

    for r := 0; r < 100; r++ {
        go func() {
            for {
                read := readOp{
                    key:  rand.Intn(5),
                    resp: make(chan int)}
                reads <- read
                <-read.resp
                atomic.AddUint64(&readOps, 1)
                time.Sleep(time.Millisecond)
            }
        }()
    }

    for w := 0; w < 10; w++ {
        go func() {
            for {
                write := writeOp{
                    key:  rand.Intn(5),
                    val:  rand.Intn(100),
                    resp: make(chan bool)}
                writes <- write
                <-write.resp
                atomic.AddUint64(&writeOps, 1)
                time.Sleep(time.Millisecond)
            }
        }()
    }

    time.Sleep(time.Second)
    readOpsFinal := atomic.LoadUint64(&readOps)
    fmt.Println("readOps:", readOpsFinal)
    writeOpsFinal := atomic.LoadUint64(&writeOps)
    fmt.Println("writeOps:", writeOpsFinal)
}
```


### 排序


Go 提供了 slices 库来排序内置和用户自定义的类型

```go
package main

import (
    "fmt"
    "slices"
)

func main() {

    strs := []string{"c", "a", "b"}
    slices.Sort(strs)            // 排序时会原位排序
    fmt.Println("Strings:", strs)

    ints := []int{7, 2, 4}
    slices.Sort(ints)
    fmt.Println("Ints:   ", ints)

    s := slices.IsSorted(ints)     // 判断是否排序了
    fmt.Println("Sorted: ", s)
}
```

除了排序，slices 库还提供了许多其它函数，如替换、查找、翻转等，具体参考 [slices package - slices - Go Packages](https://pkg.go.dev/slices)

对于自定义类型，需要自定义排序函数，通过 slices.SortFunc 来调用排序函数，而排序函数需要使用 cmp.Compare

```go
package main

import (
    "cmp"
    "fmt"
    "slices"
)

func main() {
    fruits := []string{"peach", "banana", "kiwi"}

    lenCmp := func(a, b string) int {
        return cmp.Compare(len(a), len(b))
    }

    slices.SortFunc(fruits, lenCmp)
    fmt.Println(fruits)

    type Person struct {
        name string
        age  int
    }

    people := []Person{
        Person{name: "Jax", age: 37},
        Person{name: "TJ", age: 25},
        Person{name: "Alex", age: 72},
    }

    slices.SortFunc(people,
        func(a, b Person) int {
            return cmp.Compare(a.age, b.age)
        })
    fmt.Println(people)
}
```


### 杂项


#### 编码

Go 支持 json（ encoding/json ）、xml（ encoding/xml ）、base64（ encoding/base64 ）


#### 时间

获取当前时间

```go
now := time.Now()
```

创建时间

```go
then := time.Date(2009, 11, 17, 20, 34, 58, 651387237, time.UTC)
```

获取 Unix 时间，从 1970年1月1日开始的时间

```go
now := time.Now()
fmt.Println(now)

fmt.Println(now.Unix())
fmt.Println(now.UnixMilli())
fmt.Println(now.UnixNano())
```



#### 随机数

```go
package main

import (
    "fmt"
    "math/rand/v2"
)

func main() {

    fmt.Print(rand.IntN(100), ",")
    fmt.Print(rand.IntN(100))
    fmt.Println()

    fmt.Println(rand.Float64())

    fmt.Print((rand.Float64()*5)+5, ",")
    fmt.Print((rand.Float64() * 5) + 5)
    fmt.Println()

    s2 := rand.NewPCG(42, 1024)
    r2 := rand.New(s2)
    fmt.Print(r2.IntN(100), ",")
    fmt.Print(r2.IntN(100))
    fmt.Println()

    s3 := rand.NewPCG(42, 1024)
    r3 := rand.New(s3)
    fmt.Print(r3.IntN(100), ",")
    fmt.Print(r3.IntN(100))
    fmt.Println()
}
```


#### 解析URL

使用 url.Parse 对 url 进行解析

```go
package main

import (
    "fmt"
    "net"
    "net/url"
)

func main() {

    s := "postgres://user:pass@host.com:5432/path?k=v#f"

    u, err := url.Parse(s)
    if err != nil {
        panic(err)
    }

    fmt.Println(u.Scheme)

    fmt.Println(u.User)
    fmt.Println(u.User.Username())
    p, _ := u.User.Password()
    fmt.Println(p)

    fmt.Println(u.Host)
    host, port, _ := net.SplitHostPort(u.Host)
    fmt.Println(host)
    fmt.Println(port)

    fmt.Println(u.Path)
    fmt.Println(u.Fragment)

    fmt.Println(u.RawQuery)
    m, _ := url.ParseQuery(u.RawQuery)
    fmt.Println(m)
    fmt.Println(m["k"][0])
}
```


#### 哈希

使用 crypto/sha256 计算 sha256 哈希值

```go
package main

import (
    "crypto/sha256"
    "fmt"
)
func main() {
    s := "sha256 this string"
    h := sha256.New()
    h.Write([]byte(s))
    bs := h.Sum(nil)
    fmt.Println(s)
    fmt.Printf("%x\n", bs)
}
```

除了 sha256，还有许多其它的哈希函数，参见 [crypto package - crypto - Go Packages](https://pkg.go.dev/crypto)



### 文件操作


#### 文件路径

```go
package main

import (
    "fmt"
    "path/filepath"
    "strings"
)

func main() {

    p := filepath.Join("dir1", "dir2", "filename")
    fmt.Println("p:", p)

    fmt.Println(filepath.Join("dir1//", "filename"))
    fmt.Println(filepath.Join("dir1/../dir1", "filename"))

    fmt.Println("Dir(p):", filepath.Dir(p))
    fmt.Println("Base(p):", filepath.Base(p))

    fmt.Println(filepath.IsAbs("dir/file"))
    fmt.Println(filepath.IsAbs("/dir/file"))

    filename := "config.json"

    ext := filepath.Ext(filename)
    fmt.Println(ext)

    fmt.Println(strings.TrimSuffix(filename, ext))

    rel, err := filepath.Rel("a/b", "a/b/t/file")
    if err != nil {
        panic(err)
    }
    fmt.Println(rel)
}
```


#### 文件夹

```go
import (
    "fmt"
    "io/fs"
    "os"
    "path/filepath"
)
```

创建文件夹

```go
err := os.Mkdir("subdir", 0755)
```

删除文件夹

```go
os.RemoveAll("subdir")
```

读取文件夹

```go
c, err := os.ReadDir(".")
for _, entry := range c {
	fmt.Println(" ", entry.Name(), entry.IsDir())
}
```

如果想要访问子文件夹，可以使用

```go
filepath.WalkDir("subdir", visit)
func visit(path string, d fs.DirEntry, err error) error {
    if err != nil {
        return err
    }
    fmt.Println(" ", path, d.IsDir())
    return nil
}
```


创建临时文件和临时文件夹

```go
os.CreateTemp("", "sample")
os.MkdirTemp("", "sampledir")
```



#### 读取文件

如果只想一次读完所有的数据，可以直接使用 os.ReadFile

```go
dat, err := os.ReadFile("test.txt")
fmt.Print(string(dat))
```

如果想要每次读取一部分数据，可以使用 os.Open

```go
f, err := os.Open("test.txt")
b1 := make([]byte, 5)      // 读取 5 个字符
n1, err := f.Read(b1)
fmt.Printf("%d bytes: %s\n", n1, string(b1[:n1]))

o2, err := f.Seek(6, io.SeekStart)
b2 := make([]byte, 2)
n2, err := f.Read(b2)
fmt.Printf("%d bytes @ %d: ", n2, o2)
fmt.Printf("%v\n", string(b2[:n2]))
```



#### 写入文件

直接写入文件

```go
d1 := []byte("hello world")
err := os.WriteFile("test1.txt", d1, 0644)
```

创建一个文件之后写入

```go
f, err := os.Create("/tmp/dat2")
check(err)

defer f.Close()

d2 := []byte{115, 111, 109, 101, 10}
n2, err := f.Write(d2)
check(err)
fmt.Printf("wrote %d bytes\n", n2)

n3, err := f.WriteString("writes\n")
check(err)
fmt.Printf("wrote %d bytes\n", n3)

f.Sync()

w := bufio.NewWriter(f)
n4, err := w.WriteString("buffered\n")
check(err)
fmt.Printf("wrote %d bytes\n", n4)

w.Flush()
```



### 测试和 Benchmark


```go
package main

import (
    "fmt"
    "testing"
)
func IntMin(a, b int) int {
    if a < b {
        return a
    }
    return b
}

func TestIntMinBasic(t *testing.T) {
    ans := IntMin(2, -2)
    if ans != -2 {
        t.Errorf("IntMin(2, -2) = %d; want -2", ans)
    }
}

func TestIntMinTableDriven(t *testing.T) {
    var tests = []struct {
        a, b int
        want int
    }{
        {0, 1, 0},
        {1, 0, 0},
        {2, -2, -2},
        {0, -1, -1},
        {-1, 0, -1},
    }

    for _, tt := range tests {

        testname := fmt.Sprintf("%d,%d", tt.a, tt.b)
        t.Run(testname, func(t *testing.T) {
            ans := IntMin(tt.a, tt.b)
            if ans != tt.want {
                t.Errorf("got %d, want %d", ans, tt.want)
            }
        })
    }
}

func BenchmarkIntMin(b *testing.B) {

    for i := 0; i < b.N; i++ {
        IntMin(1, 2)
    }
}
```

测试的命令为

```powershell
go test -bench=. main_test.go
```

注意文件在命名时需要用 `_test` 结尾。如果报

```
go: go.mod file not found in current directory or any parent directory;
```

需要将测试文件放在文件夹内，然后执行

```sh
go mod init
```



### 网络

#### http client

```go
package main

import (
    "bufio"
    "fmt"
    "net/http"
)

func main() {

    resp, err := http.Get("https://gobyexample.com")
    if err != nil {
        panic(err)
    }
    defer resp.Body.Close()

    fmt.Println("Response status:", resp.Status)

    scanner := bufio.NewScanner(resp.Body)
    for i := 0; scanner.Scan() && i < 5; i++ {
        fmt.Println(scanner.Text())
    }

    if err := scanner.Err(); err != nil {
        panic(err)
    }
}
```


#### http server

```go
package main

import (
    "fmt"
    "net/http"
)

func hello(w http.ResponseWriter, req *http.Request) {

    fmt.Fprintf(w, "hello\n")
}

func headers(w http.ResponseWriter, req *http.Request) {

    for name, headers := range req.Header {
        for _, h := range headers {
            fmt.Fprintf(w, "%v: %v\n", name, h)
        }
    }
}

func main() {

    http.HandleFunc("/hello", hello)
    http.HandleFunc("/headers", headers)

    http.ListenAndServe(":8090", nil)
}
```

运行该程序

```powershell
go run http-servers.go
```

访问该服务器

```powershell
curl localhost:8090/hello
```


#### Context

```go
package main

import (
    "fmt"
    "net/http"
    "time"
)

func hello(w http.ResponseWriter, req *http.Request) {

    ctx := req.Context()
    fmt.Println("server: hello handler started")
    defer fmt.Println("server: hello handler ended")

    select {
    case <-time.After(10 * time.Second):
        fmt.Fprintf(w, "hello\n")
    case <-ctx.Done():

        err := ctx.Err()
        fmt.Println("server:", err)
        internalError := http.StatusInternalServerError
        http.Error(w, err.Error(), internalError)
    }
}

func main() {

    http.HandleFunc("/hello", hello)
    http.ListenAndServe(":8090", nil)
}
```



## Practice

### 创建一个 Go 模块


#### 基础操作


1. 创建一个存放模块的文件夹

```powershell
mkdir greetings
cd greetings
```

2. 使用 go mod init 初始化模组路径，路径可以自定义，大致遵循 `<prefix>/<descriptive-text>` 的格式

```powershell
go mod init example.com/greetings
```

3. 创建一个文件 `greetings.go`，内容为

```go
package greetings

import (
	"errors"
	"fmt"
)

func Hello(name string) (string, error) {
	if name == "" {
		return "", errors.New("empty name")
	}
	message := fmt.Sprintf("Hi, %v. Welcome!", name)
	return message, nil
}
```

4. 创建 hello 文件夹，并且初始化模块

```powershell
cd ..
mkdir hello
cd hello
go mod init example.com/hello
```

5. 创建 hello.go，内容为

```go
package main

import (
	"fmt"
	"example.com/greetings"
)
func main() {
	message, err := greetings.Hello("Tom")
	fmt.Println((message))
	fmt.Println(err)
}
```

6. 在 hello 文件内执行下面命令

```powershell
go mod edit -replace example.com/greetings=../greetings
```

该命令会在 go.mod 文件内添加

```mod
replace example.com/greetings => ../greetings
```

7. 执行 go mod tidy 来同步依赖

```powershell
go mod tidy
```

8. 在 hello 文件夹内执行

```powershell
go run .
```


#### 添加测试

1. 在 greetings 文件夹内创建了 greetings_test.go

```go
package greetings

import (
	"regexp"
	"testing"
)

// TestHelloName calls greetings.Hello with a name, checking
// for a valid return value.
func TestHelloName(t *testing.T) {
	name := "Gladys"
	want := regexp.MustCompile(`\b` + name + `\b`)
	msg, err := Hello("Gladys")
	if !want.MatchString(msg) || err != nil {
		t.Fatalf(`Hello("Gladys") = %q, %v, want match for %#q, nil`, msg, err, want)
	}
}

// TestHelloEmpty calls greetings.Hello with an empty string,
// checking for an error.
func TestHelloEmpty(t *testing.T) {
	msg, err := Hello("")
	if msg != "" || err == nil {
		t.Fatalf(`Hello("") = %q, %v, want "", error`, msg, err)
	}
}
```

2. 在 greetings 文件夹内执行 go test

```powershell
go test
go test -v
```



#### 编译和安装

**编译**

```powershell
go build
```

**安装**

```powershell
go install
```



### 访问数据库

[Tutorial: Accessing a relational database - The Go Programming Language (google.cn)](https://golang.google.cn/doc/tutorial/database-access)

创建一个文件夹 data-access，并且初始化 go.mod，然后按照原文创建数据库

创建 dataaccess.go 文件

```go
package main

import (
	"database/sql"
	"fmt"
	"log"

	"github.com/go-sql-driver/mysql"
)

var db *sql.DB

func main() {
	// Capture connection properties.
	cfg := mysql.Config{
		User:                 "root",
		Passwd:               "XMJsql123456",
		Net:                  "tcp",
		Addr:                 "127.0.0.1:3306",
		DBName:               "recordings",
		AllowNativePasswords: true,
	}
	// Get a database handle.
	var err error
	db, err = sql.Open("mysql", cfg.FormatDSN())
	if err != nil {
		log.Fatal(err)
	}

	pingErr := db.Ping()
	if pingErr != nil {
		log.Fatal(pingErr)
	}
	fmt.Println("Connected!")
}
```

执行 `go get .` 来获取未安装的包。

定义一个结构用来表示数据，并且读取数据

```go
type Album struct {
	ID     int64
	Title  string
	Artist string
	Price  float32
}

func albumsByArtist(name string) ([]Album, error) {
	var albums []Album

	rows, err := db.Query("SELECT * FROM album WHERE artist = ?", name)

	if err != nil {
		return nil, fmt.Errorf("albumsByArtist %q: %v", name, err)
	}
	defer rows.Close()

	for rows.Next() {
		var alb Album
		if err := rows.Scan(&alb.ID, &alb.Title, &alb.Artist, &alb.Price); err != nil {
			return nil, fmt.Errorf("albumsByArtist %q: %v", name, err)
		}
		albums = append(albums, alb)
	}

	if err := rows.Err(); err != nil {
		return nil, fmt.Errorf("albumsByArtist %q: %v", name, err)
	}
	return albums, nil
}
```

通过 id 查找

```go
func albumByID(id int64) (Album, error) {
	// An album to hold data from the returned row.
	var alb Album

	row := db.QueryRow("SELECT * FROM album WHERE id = ?", id)
	if err := row.Scan(&alb.ID, &alb.Title, &alb.Artist, &alb.Price); err != nil {
		if err == sql.ErrNoRows {
			return alb, fmt.Errorf("albumsById %d: no such album", id)
		}
		return alb, fmt.Errorf("albumsById %d: %v", id, err)
	}
	return alb, nil
}
```

添加一条数据

```go
func addAlbum(alb Album) (int64, error) {
	result, err := db.Exec("INSERT INTO album (title, artist, price) VALUES (?, ?, ?)", alb.Title, alb.Artist, alb.Price)
	if err != nil {
		return 0, fmt.Errorf("addAlbum: %v", err)
	}
	id, err := result.LastInsertId()
	if err != nil {
		return 0, fmt.Errorf("addAlbum: %v", err)
	}
	return id, nil
}
```



### 使用 Gin 开发 Restful API



创建文件夹 web-service-gin，初始化模块

```powershell
mkdir web-service-gin
cd web-service-gin
go mod init example/web-service-gin
```



创建 main.go

```go
package main

type album struct {
	ID     string  `json:"id"`
	Title  string  `json:"title"`
	Artist string  `json:"artist"`
	Price  float64 `json:"price"`
}

// albums slice to seed record album data.
var albums = []album{
	{ID: "1", Title: "Blue Train", Artist: "John Coltrane", Price: 56.99},
	{ID: "2", Title: "Jeru", Artist: "Gerry Mulligan", Price: 17.99},
	{ID: "3", Title: "Sarah Vaughan and Clifford Brown", Artist: "Sarah Vaughan", Price: 39.99},
}
```

之后定义一些 Api

```go
// getAlbums responds with the list of all albums as JSON.
func getAlbums(c *gin.Context) {   // 使用 gin.Context 作为参数
    c.IndentedJSON(http.StatusOK, albums)
}
```

这里需要添加依赖

```go
import (
    "net/http"
    "github.com/gin-gonic/gin"
)
```


在 main 函数中定义路由和方法之间的联系

```go
func main() {
    router := gin.Default()
    router.GET("/albums", getAlbums)
    router.Run("localhost:8080")
}
```

运行程序

```powershell
go run .
```

使用 curl 测试 api

```powershell
curl http://localhost:8080/albums
[
    {
        "id": "1",
        "title": "Blue Train",
        "artist": "John Coltrane",
        "price": 56.99
    },
    {
        "id": "2",
        "title": "Jeru",
        "artist": "Gerry Mulligan",
        "price": 17.99
    },
    {
        "id": "3",
        "title": "Sarah Vaughan and Clifford Brown",
        "artist": "Sarah Vaughan",
        "price": 39.99
    }
]
```


编写程序来添加新项

```go
// postAlbums adds an album from JSON received in the request body.
// gin.Context 为上下文，提供一些服务
func postAlbums(c *gin.Context) {
    var newAlbum album

    // Call BindJSON to bind the received JSON to
    // newAlbum.
    if err := c.BindJSON(&newAlbum); err != nil {
        return
    }

    // Add the new album to the slice.
    albums = append(albums, newAlbum)
    c.IndentedJSON(http.StatusCreated, newAlbum)
}

func main(){
	router := gin.Default()
    router.GET("/albums", getAlbums)
    router.POST("/albums", postAlbums)

    router.Run("localhost:8080")
}
```

执行下面的命令

```powershell
curl http://localhost:8080/albums \
    --include \
    --header "Content-Type: application/json" \
    --request "POST" \
    --data '{"id": "4","title": "The Modern Sound of Betty Carter","artist": "Betty Carter","price": 49.99}'
```


通过 ID 查找

```go
func getAlbumByID(c *gin.Context) {
    id := c.Param("id")

    // Loop over the list of albums, looking for
    // an album whose ID value matches the parameter.
    for _, a := range albums {
        if a.ID == id {
            c.IndentedJSON(http.StatusOK, a)
            return
        }
    }
    c.IndentedJSON(http.StatusNotFound, gin.H{"message": "album not found"})
}

// router.GET("/albums/:id", getAlbumByID)
```


运行 curl 命令查找

```powershell
curl http://localhost:8080/albums/2
```


### 泛型

```go
package main
import "fmt"
func SumIntsOrFloats[K comparable, V int64 | float64](m map[K]V) V {
	var s V
	for _, v := range m {
		s += v
	}
	return s
}
func main() {
	ints := map[string]int64{
		"first":  34,
		"second": 12,
	}
	// Initialize a map for the float values
	floats := map[string]float64{
		"first":  35.98,
		"second": 26.99,
	}
	fmt.Printf("SumIntsOrFloats(ints): %v\n", SumIntsOrFloats[string, int64](ints))
	fmt.Printf("SumIntsOrFloats(floats): %v\n", SumIntsOrFloats[string, float64](floats))
}
```



### 创建一个简单的命令行应用

>使用 cobra 和 viper 库
>[Cobra. Dev](https://cobra.dev/#getting-started)


创建文件目录如下

```
D:.
│  go.mod
│  main.go
└─cmd
        root.go
        version.go
```


root.go 文件的内容为

```go
package cmd  
  
import (  
    "errors"  
    "fmt"    "os"  
    "github.com/mitchellh/go-homedir"    "github.com/spf13/cobra"    "github.com/spf13/viper")  
  
func init() {  
    //cobra.OnInitialize(initConfig)  
    rootCmd.PersistentFlags().Uint8Var(&color, "color", 12, "显示颜色")  
    rootCmd.PersistentFlags().StringVar(&cfgFile, "config", "", "config file (default is $HOME/.cobra.yaml)")  
    rootCmd.PersistentFlags().StringVarP(&projectBase, "projectbase", "b", "", "base project directory eg. github.com/spf13/")  
    rootCmd.PersistentFlags().StringP("author", "a", "YOUR NAME", "Author name for copyright attribution")  
    rootCmd.PersistentFlags().StringVarP(&userLicense, "license", "l", "", "Name of license for the project (can provide `licensetext` in config)")  
    rootCmd.PersistentFlags().Bool("viper", true, "Use Viper for configuration")  
    rootCmd.PersistentFlags().BoolVarP(&Verbose, "verbose", "v", false, "verbose output")  
    rootCmd.Flags().StringVarP(&Source, "source", "s", "", "Source directory to read from")  
      
    // 添加命令  
    rootCmd.AddCommand(versionCmd)  
  
    viper.BindPFlag("author", rootCmd.PersistentFlags().Lookup("author"))  
    viper.BindPFlag("projectbase", rootCmd.PersistentFlags().Lookup("projectbase"))  
    viper.BindPFlag("useViper", rootCmd.PersistentFlags().Lookup("viper"))  
    viper.BindPFlag("color", rootCmd.PersistentFlags().Lookup("color"))  
    viper.SetDefault("author", "NAME HERE <EMAIL ADDRESS>")  
    viper.SetDefault("license", "apache")  
}  
  
var Verbose bool  
var Source string  
var color uint8  
var cfgFile = "config.yaml"  
var projectBase = "C:\\Users\\xmj03\\Desktop"  
var userLicense = "mit"  
  
func initConfig() {  
    // Don't forget to read config either from cfgFile or from home directory!  
    if cfgFile != "" {  
       // Use config file from the flag.  
       viper.SetConfigFile(cfgFile)  
    } else {  
       // Find home directory.  
       home, err := homedir.Dir()  
       if err != nil {  
          fmt.Println(err)  
          os.Exit(1)  
       }  
  
       // Search config in home directory with name ".cobra" (without extension).  
       viper.AddConfigPath(home)  
       viper.SetConfigName(".cobra")  
    }  
  
    if err := viper.ReadInConfig(); err != nil {  
       fmt.Println("Can't read config:", err)  
       os.Exit(1)  
    }  
}  
  
var rootCmd = &cobra.Command{  
    Use:   "hello",  
    Short: "Hugo is a very fast static site generator",  
    Long: `A Fast and Flexible Static Site Generator built with  
                love by spf13 and friends in Go.                Complete documentation is available at http://hugo.spf13.com`,  
    Run: func(cmd *cobra.Command, args []string) {  
  
       author := viper.GetString("author")  
       color := viper.GetUint("color")  
       fmt.Printf("\x1b[0;%dm%s\x1b[0m", color, "hello "+author+"!")  
    },  
    Args: func(cmd *cobra.Command, args []string) error {  
       if len(args) < 1 {  
          return errors.New("requires at least one arg")  
       }  
       return nil  
    },  
}  
  
func Execute() {  
    if err := rootCmd.Execute(); err != nil {  
       fmt.Println(err)  
       os.Exit(1)  
    }  
}
```

version.go 的内容为

```go
package cmd  
  
import (  
    "fmt"  
  
    "github.com/spf13/cobra")  
  
func init() {  
    rootCmd.AddCommand(versionCmd)  
}  
  
var versionCmd = &cobra.Command{  
    Use:   "version",  
    Short: "Print the version number of Hugo",  
    Long:  `All software has versions. This is Hugo's`,  
    Run: func(cmd *cobra.Command, args []string) {  
       fmt.Println("Hugo Static Site Generator v0.9 -- HEAD")  
    },  
}
```

main.go 的内容为

```go
package main  
  
import "cobraTest/cmd"  
  
func main() {  
    cmd.Execute()  
}
```


将 main.go 编译为程序，执行下面的命令

```powershell
PS> .\main.exe version
Hugo Static Site Generator v0.9 -- HEAD
PS> .\main.exe hello --color=32 --author="xmj"
hello xmj!
```


### 分布式缓存

#### LRU缓存

LRU（最近最少使用）的实现可以通过维护一个队列，如果某条记录被访问了就移动到队尾，这样队首就是最近最少访问的数据，淘汰这条数据即可。

在 GO 中可以通过双向链表来实现这一队列，代码如下

```go
// lru/lru.go
package lru  
  
import "container/list"  
  
type Cache struct {  
    maxBytes  int64  
    nbytes    int64  
    ll        *list.List  
    cache     map[string]*list.Element  
    OnEvicted func(key string, value Value)  
}  
  
type entry struct {  
    key   string  
    value Value  
}  
  
type Value interface {  
    Len() int  
}

// 获取缓存的队列长度
func (c *Cache) Len() int {  
    return c.ll.Len()  
}
```

除此之外，还需添加初始化函数

```go
func New(maxBytes int64, onEvicted func(string2 string, value Value)) *Cache {  
    return &Cache{  
       maxBytes:  maxBytes,  
       ll:        list.New(),  
       cache:     make(map[string]*list.Element),  
       OnEvicted: onEvicted,  
    }  
}
```

之后添加查找功能

```go
func (c *Cache) Get(key string) (value Value, ok bool) {  
    if ele, ok := c.cache[key]; ok {  
       c.ll.MoveToFront(ele)  
       kv := ele.Value.(*entry)  
       return kv.value, true  
    }  
    return  
}
```

删除功能

```go
func (c *Cache) RemoveOldest() {  
    ele := c.ll.Back() // 获取队首节点  
    if ele != nil {  
       c.ll.Remove(ele)         // 删除节点  
       kv := ele.Value.(*entry) // 获取键值对  
       delete(c.cache, kv.key)  // 从缓存中删除键值对  
       c.nbytes -= int64(len(kv.key)) + int64(kv.value.Len())  
       if c.OnEvicted != nil {  
          c.OnEvicted(kv.key, kv.value)  
       }  
    }  
}
```


添加功能

```go
func (c *Cache) Add(key string, value Value) {  
    if ele, ok := c.cache[key]; ok {  
       c.ll.MoveToFront(ele)  
       kv := ele.Value.(*entry)  
       c.nbytes += int64(value.Len()) - int64(kv.value.Len())  
       kv.value = value  
    } else {  
       ele := c.ll.PushFront(&entry{key, value}) // PushFront 插入新数据  
       c.cache[key] = ele  
       c.nbytes += int64(len(key)) + int64(value.Len())  
    }  
    for c.maxBytes != 0 && c.maxBytes < c.nbytes {  
       c.RemoveOldest()  
    }  
}
```

创建一个test文件

```go
// lru/lru_test.go
package lru  
  
import "testing"  
  
type String string   // 因为需要为 string 类型额外实现方法，所以新定义一个类型，避免修改源码  
  
func (s String) Len() int {  
    return len(s)  
}  
  
func TestCache_Get(t *testing.T) {  
    lru := New(int64(0), nil)  
    lru.Add("key1", String("1234"))  
    if v, ok := lru.Get("key1"); !ok || string(v.(String)) != "1234" {  
       t.Error("key1 should be 1234")  
    }  
    if _, ok := lru.Get("key2"); ok {  
       t.Error("key2 miss in cache")  
    }  
}
```



#### 单机并发缓存

为了支持并发，使用 sync.Mutex 封装 LRU 的几个方法，使之支持并发的读写。先抽象出一个只读数据结构 ByteView 用于表示缓存值

```go
// byteview.go

package GeeCache  
  
type ByteView struct {  
    b []byte  
}  
  
func (v ByteView) Len() int {  
    return len(v.b)  
}  
  
func cloneBytes(b []byte) []byte {  
    c := make([]byte, len(b))  
    copy(c, b)  
    return c  
}  
  
func (v ByteView) ByteSlice() []byte {  
    return cloneBytes(v.b)  
}  
  
func (v ByteView) String() string {  
    return string(v.b)  
}
```


接下来为 lru.Cache 添加并发特性，即在进行操作加上互斥锁

```go
// cache.go

package GeeCache  
  
import (  
    "GeeCache/lru"  
    "sync")  
  
type cache struct {  
    mu         sync.Mutex  
    lru        *lru.Cache  
    cacheBytes int64  
}  
  
func (c *cache) add(key string, value ByteView) {  
    c.mu.Lock()  
    defer c.mu.Unlock()  
    if c.lru == nil {  
       c.lru = lru.New(c.cacheBytes, nil)  
    }  
    c.lru.Add(key, value)  
}  
  
func (c *cache) get(key string) (value ByteView, ok bool) {  
    c.mu.Lock()  
    defer c.mu.Unlock()  
    if c.lru == nil {  
       return  
    }  
    if value, ok := c.lru.Get(key); ok {  
       return value.(ByteView), true  
    }  
    return  
}
```

接下来添加与用户的交互结构 Group，首先添加一个回调函数，该函数可用于从数据源获取数据

```go
// geecache.go

package GeeCache  
  
type Getter interface {  
    Get(string) ([] byte, bool)  
}  
  
type GetterFunc func(string) ([]byte, bool)  
  
func (f GetterFunc) Get(key string) ([]byte, bool) {  
    return f(key)  
}
```

接下来定义 Group，Group 可以看成是一个缓存的命名空间

```go
type Group struct {  
    name      string  
    getter    Getter  
    mainCache cache  
}  
  
var (  
    mu     sync.RWMutex  
    groups = make(map[string]*Group)  
)  
  
func NewGroup(name string, cacheBytes int64, getter Getter) *Group {  
    if getter == nil {  
       panic("nil getter")  
    }
    mu.Lock()  
    defer mu.Unlock()  
    g := &Group{  
       name:      name,  
       getter:    getter,  
       mainCache: cache{cacheBytes: cacheBytes},  
    }  
    groups[name] = g  
    return g  
}  
  
func GetGroup(name string) *Group {  
    mu.RLock()  
    defer mu.RUnlock()  
    g := groups[name]  
    return g  
}  
  
func (g *Group) Get(key string) (ByteView, bool) {  
    if key == "" {  
       return ByteView{}, false  
    }  
    // mainCache 中存在对应的缓存，则直接返回  
    if v, ok := g.mainCache.get(key); ok {  
       log.Printf("hit")  
       return v, true  
    }  
    // 不存在缓存，则通过用户回调函数来获取数据  
    return g.load(key)  
}  
  
func (g *Group) load(key string) (value ByteView, ok bool) {  
    return g.getLocally(key)  
}  
  
func (g *Group) getLocally(key string) (ByteView, bool) {  
    bytes, err := g.getter.Get(key)  
    if err != true {  
       return ByteView{}, false  
    }  
    value := ByteView{b: cloneBytes(bytes)}  
    g.populateCache(key, value)  
    return value, true  
}  
  
func (g *Group) populateCache(key string, b ByteView) {  
    g.mainCache.add(key, b)  
}
```


#### HTTP 服务端

分布式缓存需要实现节点间通信，一种方法是建立基于 HTTP 的通信机制

```go
package GeeCache  
  
import (  
    "log"  
    "net/http"    "strings")  
  
const defaultBasePath = "/_geecache/"  
  
type HTTPPool struct {  
    self     string  
    basePath string  
}  
  
func NewHTTPPool(self string) *HTTPPool {  
    return &HTTPPool{self: self, basePath: defaultBasePath}  
}  
  
func (p *HTTPPool) Log(format string, args ...interface{}) {  
    log.Printf(p.self+format, args...)  
}  
  
func (p *HTTPPool) ServeHTTP(w http.ResponseWriter, r *http.Request) {  
    if !strings.HasPrefix(r.URL.Path, p.basePath) {  
       panic("HTTPPool ServeHTTP: invalid path: " + r.URL.Path)  
    }  
    p.Log("%s %s", r.Method, r.URL.Path)  
    parts := strings.SplitN(r.URL.Path[len(p.basePath):], "/", 2)  
    if len(parts) != 2 {  
       http.Error(w, "bad request", http.StatusBadRequest)  
       return  
    }  
    groupName := parts[0]  
    key := parts[1]  
  
    group := GetGroup(groupName)  
    if group == nil {  
       http.Error(w, "group not found", http.StatusNotFound)  
       return  
    }  
    view, err := group.Get(key)  
    if err != true {  
       http.Error(w, "group not found", http.StatusInternalServerError)  
       return  
    }  
  
    w.Header().Set("Content-Type", "application/octet-stream")  
    w.Write(view.ByteSlice())  
}
```


#### 一致性哈希

一致哈希的作用：先说哈希的作用，假设存在10个节点存储着数据，此时为了确定键对应的存储节点，可以计算键的哈希 hash(key)，再除以 10 得到的余数便可以确定节点。这种哈希存在一个问题，假如一个节点失效了，那么几乎所有缓存值对应的节点都发生了变化，即几乎所有缓存值都失效了。为了解决这一问题，采用一致性哈希算法。

一致性哈希算法将 key 映射到 2^32 的空间中，将这个数字首尾相连，形成一个环。

- 计算节点/机器(通常使用节点的名称、编号和 IP 地址)的哈希值，放置在环上。
- 计算 key 的哈希值，放置在环上，顺时针寻找到的第一个节点，就是应选取的节点/机器。

Go 中的实现

```go
package consistenthash  
  
import (  
    "hash/crc32"  
    "sort")  
  
type Hash func(data []byte) uint32  
  
type Map struct {  
    hash     Hash  
    replicas int  
    keys     []int  
    hashMap  map[int]string  
}  
  
func New(replicas int, hash Hash) *Map {  
    m := &Map{  
       hash:     hash,  
       replicas: replicas,  
       hashMap:  make(map[int]string),  
    }  
    if m.hash == nil {  
       m.hash = crc32.ChecksumIEEE  
    }  
    return m  
}  
  
func (m *Map) Add(keys ...string) {  
    for _, key := range keys {  
       hash := int(m.hash([]byte(key)))  
       m.keys = append(m.keys, hash)  
       m.hashMap[hash] = key  
    }  
    sort.Ints(m.keys)  
}  
func (m *Map) Get(key string) string {  
    if len(m.keys) == 0 {  
       return ""  
    }  
  
    hash := int(m.hash([]byte(key)))  
    // Binary search for appropriate replica.  
    idx := sort.Search(len(m.keys), func(i int) bool {  
       return m.keys[i] >= hash  
    })  
  
    return m.hashMap[m.keys[idx%len(m.keys)]]  
}
```



