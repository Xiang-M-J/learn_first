# Csharp

如果不想创建一个项目来测试一些代码，可以使用 `csc` 来编译执行代码：

csc.exe 位于 `C:\Windows\Microsoft.NET\Framework\v4.0.30319`，将其加入用户路径中。

```sh
csc test.cs&test
```



对于现代 .NET 应用程序，更推荐使用下面的方式：

```powershell
dotnet new console -n test
cd test
echo Console.WriteLine("Hello, World!"); > Program.cs
dotnet build
dotnet run
```



## 数据类型

### 数组

[数组 - C# | Microsoft Learn](https://learn.microsoft.com/zh-cn/dotnet/csharp/language-reference/builtin-types/arrays)

```csharp
int[] arr = new int[10];        // 一维数组
int[,] arr2 = new int[10,10];   // 二维数组
Console.WriteLine(arr[0]);     // 0
Console.WriteLine(arr2[0,0]);  // 0

// 数组的切片
int[] arr3 = {1,2,3,4,5,6};
Console.WriteLine(string.Join(" ", arr3[2..4]));      // arr3[2] arr3[3]：3 4
Console.WriteLine(string.Join(" ", arr3.Take(2)));    // 前面两个元素： 1 2
Console.WriteLine(string.Join(" ", arr3[^2..]));      // 最后两个元素：5 6
```



### 字典

```csharp
Dictionary<string, int> dict = new Dictionary<string, int>();
dict.Add("A", 0);
Console.WriteLine(dict["A"]);               // 0
dict.Remove("A");
Console.WriteLine(dict.ContainsKey("A"));   // 判断键是否存在 False
```



## 输入输出

### 文件读写



读取的文件内容不多：

```csharp
// 从文件直接读入完整的字符串，
File.ReadAllText(file, Encoding.UTF8);

// 从文件读入字符串数组（数组的每一项对应文件的一行）
File.ReadAllLines(file, Encoding.UTF8);
    
// 打开一个二进制文件，将文件的内容读入一个字节数组，然后关闭该文件。
File.ReadAllBytes(file);

```

> 上面的函数存在异步实现

读取的文件内容较多：

```csharp
// 采用流方式进行读取
using (StreamReader sr = new StreamReader("CDriveDirs.txt"))
{
    while ((line = sr.ReadLine()) != null)
    {
        Console.WriteLine(line);
    }
}
```



写入的内容不多：

```csharp
// 创建一个新文件，在其中写入指定的字节数组，然后关闭该文件。如果目标文件已存在，则会将其截断并覆盖。
File.WriteAllBytes (string path, byte[] bytes);

// 创建一个新文件，在其中写入一个或多个字符串，然后关闭该文件
File.WriteAllLines(path, string[], Encoding.UTF8);

// 创建一个新文件，向其中写入内容，然后关闭文件。 如果目标文件已存在，则会将其截断并覆盖。
File.WriteAllText(path, string, Encoding.UTF8);
```

> 上面的函数存在异步实现



写入的内容较多：

```csharp
using (StreamWriter sw = new StreamWriter("CDriveDirs.txt"))
{
    foreach (DirectoryInfo dir in cDirs)
    {
        sw.WriteLine(dir.Name);
    }
}
```



向文件中增加内容：

```csharp
File.AppendAllText (string path, string? contents);

File.AppendAllLines (string path, contents);
```

> 上面的函数存在异步实现



### 命令行

在 CSharp 中，通过 Process 类来实现命令行的输入输出

```csharp
using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace downloadGithub
{
    internal class CommandRunner
    {
        public CommandRunner()
        {}
        public Result Run(string command, string WorkingDirectory="")
        {
            Process process = new Process();
            process.StartInfo.FileName = "cmd.exe";
            process.StartInfo.UseShellExecute = false; // 是否使用操作系统shell启动
            process.StartInfo.RedirectStandardError = true;	// 是否有标准错误
            process.StartInfo.RedirectStandardOutput = true;	// 是否有标准输出
            process.StartInfo.RedirectStandardInput = true;		// 是否有标准输入
            process.StartInfo.CreateNoWindow = false;	// 是否无窗口
            if (WorkingDirectory != "") {  // 设置工作目录，不设置该项，则默认为与程序共同路径。
                process.StartInfo.WorkingDirectory = WorkingDirectory;
            }
            process.Start();
            process.StandardInput.WriteLine(command + "&exit");// 加上 exit 确保退出，不会假死。
            process.StandardInput.AutoFlush = true;
            process.WaitForExit();
            Result result = new Result(process.StandardOutput.ReadToEnd(), process.StandardError.ReadToEnd());
            process.Close();
            return result;
        }
        public class Result
        {
            public string Output { get; }
            public string Error { get; }
            public Result(string output, string error)
            {
                Output = output;
                Error = error;
            }
            public override string ToString()
            {
                return Output + Error;
            }
        }
    }
}

```




## 网络

### C# 访问网址获取网页

使用 [HttpClient](https://learn.microsoft.com/zh-cn/dotnet/fundamentals/networking/http/httpclient) 异步实现：

```csharp
private async void htmlParser(string url)
{
    string content = await GetHtmlContentAsync(url);
    Trace.WriteLine(content);
}

async Task<string> GetHtmlContentAsync(string url)
{
    HttpClient httpClient = new HttpClient();
    string content = "";
    try
    {
        HttpResponseMessage response = await httpClient.GetAsync(url);
        response.EnsureSuccessStatusCode();
        content = await response.Content.ReadAsStringAsync();
    }
    catch (HttpRequestException ex)
    {
        Console.WriteLine($"Error: {ex.Message}");
    }
    return content;
}
```

除了上面这种方法，对于 `HttpClient` 还可以指定 baseurl：

```c#
HttpClient httpClient = new HttpClient{
    BaseAddress = new Uri("https://github.com") // 基地址
};
string content = "";
try
{
    HttpResponseMessage response = await httpClient.GetAsync("WongKinYiu/yolov9"); // 本地地址
    response.EnsureSuccessStatusCode();
    content = await response.Content.ReadAsStringAsync();
}

```



## 时间相关

### 获取时间戳

```csharp
public string GetTimeStamp()
{
    TimeSpan ts = DateTime.Now - new DateTime(1970, 1, 1, 0, 0, 0, 0);
    return Convert.ToInt64(ts.TotalSeconds).ToString();
}  
```



## 字符串处理

### 常用处理函数

1. Trim 去除两边空格

```csharp
string b = " space ".Trim();  // b = "space"
```

2. 字符串切片

```c#
string b = "1slice1"[1..^1]	 // b = "slice" [1..^1] 相当于 python 中的 [1:-1]
```





### 列表的输出

```csharp
int[] arr = {1,2,3,4,5};
Console.WriteLine(string.Join(" ", arr));
```



### 字符串格式化

```csharp
int a = 10;
double num1 = 3.1415926;
double num2 = 3.14;
Console.WriteLine($"a={a}");                // a=10  
Console.WriteLine(num1.ToString("0.000"));  // 3.142 保留三位小数
Console.WriteLine(num2.ToString("0.000"));  // 3.140 不足用0补齐
```



### 正则表达式

[C# 正则表达式 | 菜鸟教程 (runoob.com)](https://www.runoob.com/csharp/csharp-regular-expressions.html)

```csharp
Regex regex = new Regex(pattern);
MatchCollection mc = regex.Matches(content);

foreach(Match m in mc){
    Console.WriteLine(m.ToString());
}

// 替换多余的空格
string pattern = "\\s+";
string replacement = " ";
Regex rgx = new Regex(pattern);
string result = rgx.Replace(input, replacement);
```



# WPF 

>  基于 WPF 对 CSharp 进行学习



> 为应用程序生成单文件程序

[为应用程序部署创建单个文件 - .NET | Microsoft Learn](https://learn.microsoft.com/zh-cn/dotnet/core/deploying/single-file/overview?tabs=vs)

点击 生成 -> 发布选定内容

- 将“部署模式”设置为“独立式”（体积会很大）或“依赖于框架”。
- 将“目标运行时”设置为要发布到的平台 。 必须是除“可移植”以外的设置。
- 选择“生成单个文件”。




> 1. 在查看文档时，由于 WPF 的类非常多，所以要注意类的命名空间
>
> 2. :warning: 打印信息使用 `Trace.WriteLine()`



## NuGet 包

### UI 组件库

#### WPF-UI

[wpf-ui](https://github.com/lepoco/wpfui)  ⭐6.3k ⬇️ 233k  文档: [WPF UI | WPF UI (lepo.co)](https://wpfui.lepo.co/)

一个符合现代设计的 UI 库，类似 Fluent的设计。

在 App.xaml 中定义 ResourceDictionary 元素：

```xaml
<Application
  ...
  xmlns:ui="http://schemas.lepo.co/wpfui/2022/xaml">
  <Application.Resources>
    <ResourceDictionary>
      <ResourceDictionary.MergedDictionaries>
        <ui:ThemesDictionary Theme="Dark" />
        <ui:ControlsDictionary />
      </ResourceDictionary.MergedDictionaries>
    </ResourceDictionary>
  </Application.Resources>
</Application>
```

修改 MainWindow 的基类，并且加入 `ApplicationThemeManager.Apply(frameworkElement)`：

```csharp
public partial class MainWindow : FluentWindow
{
    public MainWindow()
    {
        InitializeComponent();
        ApplicationThemeManager.Apply(this);
    }
}
```

删除 MainWindow.xaml 中的内容，并加入如下代码：

```xaml
<ui:FluentWindow x:Class="WpfUITest.MainWindow"
    xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
    xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
    xmlns:d="http://schemas.microsoft.com/expression/blend/2008"
    xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006"
    mc:Ignorable="d"
    Title="MainWindow" Height="450" Width="800" xmlns:ui="http://schemas.lepo.co/wpfui/2022/xaml">
    <StackPanel>
        <ui:TitleBar Title="WPF UI"/>
        <ui:Card Margin="8">
            <ui:Button Content="Hello World" Icon="{ui:SymbolIcon Fluent24}" />
        </ui:Card>
    </StackPanel>
</ui:FluentWindow>
```

其中 StackPanel 为原生组件，带有 ui 标识为 WPF-UI 中的组件。



#### Shade.WPF.Controls

[Shade.WPF.Controls](https://github.com/ControlzEx/ControlzEx) :star: 911 :arrow_down: 10.9M

提供了一套为 WPF 应用程序量身定制的共享控件。通过对细节的细致关注和无缝集成，这个包丰富了您跨各种领域的WPF开发经验。使用这些控件需要加上下面的 xmlns

```xaml
<Window 
        ...
		xmlns:controlzEx="urn:Shade">
    <Grid>
        ...
    </Grid>
</Window>
```

下面是几种组件：

**TextBoxInputMaskBehavior**

为 TextBox 加上一个 mask（不会校验数据），（这里还需要加入额外的 xmlns）：

```xaml
<Window 
        ...
        xmlns:behaviors="http://schemas.microsoft.com/xaml/behaviors"
		xmlns:controlzEx="urn:Shade">
    <Grid>
        <TextBlock Grid.Row="0" Grid.Column="0" Margin="4" Text="Datetime" />
		<TextBox Grid.Row="0" Grid.Column="1" Margin="4">
            <behaviors:Interaction.Behaviors>
                <controlzEx:TextBoxInputMaskBehavior InputMask="00/00/0000" />
            </behaviors:Interaction.Behaviors>
		</TextBox>
    </Grid>
</Window>
```

**KeyboardNavigationEx**：UI focus

**AutoMove ToolTip**：会移动的 tooltip

**GlowWindowBehavior**：给窗口加上光圈

**WindowChromeBehavior**：自定义的 [WindowChrome](https://learn.microsoft.com/zh-cn/dotnet/api/system.windows.shell.windowchrome?view=windowsdesktop-8.0)

**PopupEx**：自定义的弹出框

**TabControlEx**：自定义选项卡

**PackIconBase**：一个基类，用于帮助在WPF中创建图标包的通用方法。

**Theming**：提供主题管理器



#### MaterialDesignThemes

[MaterialDesignThemes](https://github.com/MaterialDesignInXAML/MaterialDesignInXamlToolkit) :star: 14.5k  :arrow_down: 6.88M 文档：[Getting Started](http://materialdesigninxaml.net/)

提供了 Material 主题的组件库。



#### HandyControl

[HandyControl](https://github.com/HandyOrg/HandyControl) :star: 5.5k :arrow_down: 239.1k 文档：[快速开始 | HandyOrg](https://handyorg.github.io/handycontrol/quick_start/)

包含了一些简单和常用的控件。



#### ReactiveUI.WPF

[reactiveui](https://github.com/reactiveui/reactiveui) :star: 7.9k :arrow_down: 1.3M 

ReactiveUI 是一个可组合的、跨平台的模型-视图-视图模型框架，受到了函数式响应式编程的启发，是一种范式，从用户界面中抽象出可变状态，并在一个可读的地方表达围绕特性的想法，从而提高应用程序的可测试性。



## 数据绑定

### 声明绑定

通常情况下，每个绑定具有四个组件：

- 绑定目标对象。
- 目标属性。
- 绑定源。
- 指向绑定源中要使用的值的路径。

例如，如果将 TextBox 的内容绑定到 Employee.Name 属性，则可以类似如下所示设置绑定：

| 设置         | 值       |
| :----------- | :------- |
| 目标         | TextBox  |
| 目标属性     | Text     |
| 源对象       | Employee |
| 源对象值路径 | Name     |

一个简单的数据绑定案例：

创建一个类 Person：

```csharp
class Person
{
    string name = "text";

    public string Name
    {
        get { return name; }
        set { name = value; }
    }
}
```

在初始化时进行绑定：

```csharp
public MainWindow()
{
    InitializeComponent();
    Person person = new Person();
    this.DataContext = person;
}
```

在 xaml 文件中添加 TextBox 和 TextBlock 控件

```xaml
<TextBox Name="BindText" Text="{Binding Path=Name, UpdateSourceTrigger=PropertyChanged}" Margin="0,0,400,270"/>
<TextBlock Name="ShowText" Text="{Binding Path=Name, UpdateSourceTrigger=PropertyChanged}" Margin="0,200,400,50"/>
```

这里需要设置 UpdateSourceTrigger，否则 Textblock 的值不会变化。



当在 XAML 元素上声明数据绑定时，它们会通过查看其直接的 DataContext 属性来解析数据绑定。 数据上下文通常是绑定源值路径评估的绑定源对象。 可以在绑定中重写此行为，并设置特定的绑定源对象值。 如果未设置承载绑定的对象的 DataContext 属性，则将检查父元素的 DataContext 属性，依此类推，直到 XAML 对象树的根。 简而言之，除非在对象上显式设置，否则用于解析绑定的数据上下文将继承自父级。

数据流的方向可以通过设置 Binding.Mode 来控制：

![databinding-dataflow](https://learn.microsoft.com/zh-cn/dotnet/desktop/wpf/data/media/index/databinding-dataflow.png)


+ 通过 OneWay 绑定，对源属性的更改会自动更新目标属性，但对目标属性的更改不会传播回源属性。

+ 通过 TwoWay 绑定，更改源属性或目标属性时会自动更新另一方。 此类型的绑定适用于可编辑窗体或其他完全交互式 UI 方案。

+ OneWayToSource 绑定与 OneWay 绑定相反；当目标属性更改时，它会更新源属性。

+ OneTime 绑定未在图中显示，该绑定会使源属性初始化目标属性，但不传播后续更改。 如果数据上下文发生更改，或者数据上下文中的对象发生更改，则更改不会在目标属性中反映。


触发源更新的因素：TwoWay 或 OneWayToSource 绑定侦听目标属性中的更改，并将更改传播回源（称为更新源）。但是，在编辑文本时或完成文本编辑后控件失去焦点时，源值是否会更新？ Binding.UpdateSourceTrigger 属性确定触发源更新的因素。


如果 UpdateSourceTrigger 值为 UpdateSourceTrigger.PropertyChanged，则目标属性更改后，TwoWay 或 OneWayToSource 绑定的右箭头指向的值会立即更新。 但是，如果 UpdateSourceTrigger 值为 LostFocus，则仅当目标属性失去焦点时才会使用新值更新该值。

下表以 TextBox 为例，提供每个 UpdateSourceTrigger 值的示例方案。

| UpdateSourceTrigger 值 | 源值更新时间              | TextBox 的示例方案                                           |
| :--------------------- | :------------------------ | :----------------------------------------------------------- |
| `LostFocus`（默认值）  | TextBox 控件失去焦点时。  | 与验证逻辑关联的 TextBox。                                   |
| `PropertyChanged`      | 键入 TextBox 时。         | 聊天室窗口中的 TextBox 控件。                                |
| `Explicit`             | 应用调用 UpdateSource时。 | 可编辑窗体中的 TextBox 控件（仅当用户按“提交”按钮时才更新源值）。 |

指定绑定的另一种方法是直接在代码中的 Binding 对象上设置属性，然后将绑定分配给属性：

```csharp
private void Window_Loaded(object sender, RoutedEventArgs e)
{
    // Make a new data source object
    var personDetails = new Person()
    {
        Name = "John",
        Birthdate = DateTime.Parse("2001-02-03")
    };

    // New binding object using the path of 'Name' for whatever source object is used
    var nameBindingObject = new Binding("Name");

    // Configure the binding
    nameBindingObject.Mode = BindingMode.OneWay;
    nameBindingObject.Source = personDetails;
    nameBindingObject.Converter = NameConverter.Instance;
    nameBindingObject.ConverterCulture = new CultureInfo("en-US");

    // Set the binding to a target object. The TextBlock.Name property on the NameBlock UI element
    BindingOperations.SetBinding(NameBlock, TextBlock.TextProperty, nameBindingObject);
}
```

关于绑定路径语法：[绑定声明概述 - WPF .NET | Microsoft Learn](https://learn.microsoft.com/zh-cn/dotnet/desktop/wpf/data/binding-declarations-overview?view=netdesktop-6.0#binding-path-syntax)



### 绑定源

指定绑定源：在之前的示例中，通过设置 this.DataContext 来指定绑定源，实际上可以在绑定声明中直接设置 Binding.Source 属性来指定绑定源：

```xaml
<DockPanel xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
           xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
           xmlns:c="clr-namespace:SDKSample">
    <DockPanel.Resources>
        <c:MyData x:Key="myDataSource"/>
    </DockPanel.Resources>
    <Button Background="{Binding Source={StaticResource myDataSource}, Path=ColorName}"
            Width="150" Height="30">
        I am bound to be RED!
    </Button>
</DockPanel>
```

如果绑定对象和源对象直接没有默认的转换器，就会导致类型错误，这时可以通过实现 IValueConverter 接口来创建一个自定义转换器，如以下示例所示：

```csharp
[ValueConversion(typeof(Color), typeof(SolidColorBrush))]
public class ColorBrushConverter : IValueConverter
{
    public object Convert(object value, Type targetType, object parameter, System.Globalization.CultureInfo culture)
    {
        Color color = (Color)value;
        return new SolidColorBrush(color);
    }

    public object ConvertBack(object value, Type targetType, object parameter, System.Globalization.CultureInfo culture)
    {
        return null;
    }
}
```

数据绑定支持以下绑定源类型：

- **.NET 公共语言运行时 (CLR) 对象**

    可以绑定到任何公共语言运行时 (CLR) 对象的公共属性、子属性和索引器。 绑定引擎使用 CLR 反射来获取属性值。 实现了 [ICustomTypeDescriptor](https://learn.microsoft.com/zh-cn/dotnet/api/system.componentmodel.icustomtypedescriptor) 或具有已注册 [TypeDescriptionProvider](https://learn.microsoft.com/zh-cn/dotnet/api/system.componentmodel.typedescriptionprovider) 的对象也可以使用绑定引擎。

    有关如何实现可用作绑定源的类的详细信息，请参阅本文后面的[在对象上实现绑定源](https://learn.microsoft.com/zh-cn/dotnet/desktop/wpf/data/binding-sources-overview?view=netdesktop-6.0#implement-a-binding-source-on-your-objects)。

- 动态对象

    可以绑定到对象的可用属性和索引器，该对象实现 [IDynamicMetaObjectProvider](https://learn.microsoft.com/zh-cn/dotnet/api/system.dynamic.idynamicmetaobjectprovider) 接口。 如果可以访问代码中的成员，则可以绑定到该成员。 例如，如果动态对象使用户可以通过 `SomeObject.AProperty` 访问代码中的成员，则可以通过将绑定路径设置为 `AProperty` 来绑定到该成员。

- **ADO.NET 对象**

    可以绑定到 ADO.NET 对象，例如 [DataTable](https://learn.microsoft.com/zh-cn/dotnet/api/system.data.datatable)。 ADO.NET [DataView](https://learn.microsoft.com/zh-cn/dotnet/api/system.data.dataview) 实现 [IBindingList](https://learn.microsoft.com/zh-cn/dotnet/api/system.componentmodel.ibindinglist) 接口，该接口提供绑定引擎侦听的更改通知。

- **XML 对象**

    可以绑定到 [XmlNode](https://learn.microsoft.com/zh-cn/dotnet/api/system.xml.xmlnode)、[XmlDocument](https://learn.microsoft.com/zh-cn/dotnet/api/system.xml.xmldocument) 或 [XmlElement](https://learn.microsoft.com/zh-cn/dotnet/api/system.xml.xmlelement)，并对其运行 `XPath` 查询。 访问 XML 数据（标记中的绑定源）的便捷方法是使用 [XmlDataProvider](https://learn.microsoft.com/zh-cn/dotnet/api/system.windows.data.xmldataprovider) 对象。 有关详细信息，请参阅[使用 XMLDataProvider 和 XPath 查询绑定到 XML 数据 (.NET Framework)](https://learn.microsoft.com/zh-cn/dotnet/desktop/wpf/data/how-to-bind-to-xml-data-using-an-xmldataprovider-and-xpath-queries?view=netdesktop-6.0)。

    使用 LINQ to XML，还可以绑定到 [XElement](https://learn.microsoft.com/zh-cn/dotnet/api/system.xml.linq.xelement) 或 [XDocument](https://learn.microsoft.com/zh-cn/dotnet/api/system.xml.linq.xdocument)，或者绑定到对这些类型的对象运行查询而得到的结果。 使用 LINQ to XML 访问 XML 数据（标记中的绑定源）的便捷方法是使用 [ObjectDataProvider](https://learn.microsoft.com/zh-cn/dotnet/api/system.windows.data.objectdataprovider) 对象。 有关详细信息，请参阅[绑定到 XDocument、XElement 或 LINQ for XML 查询结果 (.NET Framework)](https://learn.microsoft.com/zh-cn/dotnet/desktop/wpf/data/how-to-bind-to-xdocument-xelement-or-linq-for-xml-query-results?view=netdesktop-6.0)。

- **[DependencyObject](https://learn.microsoft.com/zh-cn/dotnet/api/system.windows.dependencyobject) 对象**

    可以绑定到任何 [DependencyObject](https://learn.microsoft.com/zh-cn/dotnet/api/system.windows.dependencyobject) 的依赖属性。 有关示例，请参阅[绑定两个控件的属性 (.NET Framework)](https://learn.microsoft.com/zh-cn/dotnet/desktop/wpf/data/how-to-bind-the-properties-of-two-controls?view=netdesktop-6.0)。

绑定到枚举：[如何绑定到枚举 - WPF .NET | Microsoft Learn](https://learn.microsoft.com/zh-cn/dotnet/desktop/wpf/data/how-to-bind-to-an-enumeration?view=netdesktop-6.0)



## 事件

### 路由事件

从功能或实现的角度来理解路由事件：

- 从功能角度来看，路由事件是一种可以针对元素树中的多个侦听器（而不是仅针对事件源）调用处理程序的事件。 事件侦听器是附加和调用了事件处理程序的元素。 事件源是最初引发事件的元素或对象。
- 从实现的角度来看，路由事件是向 WPF 事件系统注册的事件，由 [RoutedEvent](https://learn.microsoft.com/zh-cn/dotnet/api/system.windows.routedevent) 类的实例提供支持，并由 WPF 事件系统处理。 通常，路由事件是使用 CLR 事件“包装器”实现的，可以在 XAML 和代码隐藏中启用附加处理程序，就像你使用 CLR 事件一样。

 根据路由事件的定义方式，当事件在源元素上被引发时，它会：

- 通过元素树从源元素浮升到根元素（通常是页面或窗口）。
- 通过元素树从根元素到源元素向下进行隧道操作。
- 不会遍历元素树，只发生在源元素上。

如下面这个元素树：

```xaml
<Border Height="30" Width="200" BorderBrush="Gray" BorderThickness="1">
    <StackPanel Background="LightBlue" Orientation="Horizontal" Button.Click="YesNoCancelButton_Click">
        <Button Name="YesButton">Yes</Button>
        <Button Name="NoButton">No</Button>
        <Button Name="CancelButton">Cancel</Button>
    </StackPanel>
</Border>
```

这三个按钮中的每一个都是潜在的 [Click](https://learn.microsoft.com/zh-cn/dotnet/api/system.windows.controls.primitives.buttonbase.click#system-windows-controls-primitives-buttonbase-click) 事件源。 单击其中一个按钮时，它会引发 `Click` 事件，从按钮浮升到根元素。 [Button](https://learn.microsoft.com/zh-cn/dotnet/api/system.windows.controls.button) 和 [Border](https://learn.microsoft.com/zh-cn/dotnet/api/system.windows.controls.border) 元素没有附加事件处理程序，但 [StackPanel](https://learn.microsoft.com/zh-cn/dotnet/api/system.windows.controls.stackpanel) 有。 树中较高、未显示的其他元素可能也附加了 `Click` 事件处理程序。 当 `Click` 事件到达 `StackPanel` 元素时，WPF 事件系统将调用附加到它的 `YesNoCancelButton_Click` 处理程序。 示例中 `Click` 事件的事件路由为：`Button`>`StackPanel`>`Border`> 连续的父元素。

对于（通过继承或其他方式）成为侦听器类的成员的事件，可以按如下所示附加处理程序：

```xaml
<Button Name="Button1" Click="Button_Click">Click me</Button>
```

如果事件不是侦听器类的成员，则必须以 `<owner type>.<event name>` 的形式使用限定的事件名称。 例如，由于 [StackPanel](https://learn.microsoft.com/zh-cn/dotnet/api/system.windows.controls.stackpanel) 类不实现 [Click](https://learn.microsoft.com/zh-cn/dotnet/api/system.windows.controls.primitives.buttonbase.click#system-windows-controls-primitives-buttonbase-click) 事件，若要将处理程序附加到浮升到该元素的 `Click` 事件的 `StackPanel`，需要使用限定的事件名称语法：

```xaml
<StackPanel Name="StackPanel1" Button.Click="Button_Click">
    <Button>Click me</Button>
</StackPanel>
```

若要使用代码将路由事件的事件处理程序附加到元素，通常有两个选择：

- 直接调用 [AddHandler](https://learn.microsoft.com/zh-cn/dotnet/api/system.windows.uielement.addhandler) 方法。 始终可以通过这种方式附加路由事件处理程序。 下面的示例使用 `AddHandler` 方法将 `Click` 事件处理程序附加到按钮：

    ```csharp
    Button1.AddHandler(ButtonBase.ClickEvent, new RoutedEventHandler(Button_Click));
    ```

    将按钮的 `Click` 事件的处理程序附加到事件路由中的不同元素，例如名为 `StackPanel1` 的 [StackPanel](https://learn.microsoft.com/zh-cn/dotnet/api/system.windows.controls.stackpanel)：

    ```csharp
    StackPanel1.AddHandler(ButtonBase.ClickEvent, new RoutedEventHandler(Button_Click));
    ```

- 如果路由事件实现 CLR 事件包装器，请使用特定于语言的事件语法添加事件处理程序，就像对标准 CLR 事件的操作一样。 大多数现有的 WPF 路由事件实现 CLR 包装器，从而实现了特定于语言的事件语法。 此示例使用特定于语言的语法将 `Click` 事件处理程序附加到按钮：

    ```csharp
    Button1.Click += Button_Click;
    ```



### 附加事件

在 XAML 语法中，附加事件由其事件名称及其所有者类型指定，格式为 `<owner type>.<event name>`。以下 XAML 属性语法将 `AquariumFilter.Clean` 附加事件的 `AquariumFilter_Clean` 处理程序附加到 `aquarium1` 元素：

```xaml
<aqua:Aquarium x:Name="aquarium1" Height="300" Width="400" aqua:AquariumFilter.Clean="AquariumFilter_Clean"/>
```

### 对象生存期

对于 WPF 框架级元素（视觉对象），WPF 会实现 Initialized、Loaded 和 Unloaded 生存期事件。以下示例演示主要在 XAML 中实现的元素树。 XAML 定义一个父 Canvas 元素，其中包含嵌套元素，每个元素都使用 XAML 属性语法附加 Initialized、Loaded 和 Unloaded 生存期事件处理程序：

```xaml
<Canvas x:Name="canvas">
    <StackPanel x:Name="outerStackPanel" Initialized="InitHandler" Loaded="LoadHandler" Unloaded="UnloadHandler">
        <custom:ComponentWrapper x:Name="componentWrapper" Initialized="InitHandler" Loaded="LoadHandler" Unloaded="UnloadHandler">
            <TextBox Name="textBox1" Initialized="InitHandler" Loaded="LoadHandler" Unloaded="UnloadHandler" />
            <TextBox Name="textBox2" Initialized="InitHandler" Loaded="LoadHandler" Unloaded="UnloadHandler" />
        </custom:ComponentWrapper>
    </StackPanel>
    <Button Content="Remove canvas child elements" Click="Button_Click"/>
</Canvas>
```
其中一个 XAML 元素是自定义控件，它派生自在代码隐藏中分配生存期事件处理程序的基类。

```csharp
public partial class MainWindow : Window
{
    public MainWindow() => InitializeComponent();
    // Handler for the Initialized lifetime event (attached in XAML).
    private void InitHandler(object sender, System.EventArgs e) => 
        Debug.WriteLine($"Initialized event on {((FrameworkElement)sender).Name}.");
    // Handler for the Loaded lifetime event (attached in XAML).
    private void LoadHandler(object sender, RoutedEventArgs e) => 
        Debug.WriteLine($"Loaded event on {((FrameworkElement)sender).Name}.");
    // Handler for the Unloaded lifetime event (attached in XAML).
    private void UnloadHandler(object sender, RoutedEventArgs e) =>
        Debug.WriteLine($"Unloaded event on {((FrameworkElement)sender).Name}.");
    // Remove nested controls.
    private void Button_Click(object sender, RoutedEventArgs e) => 
        canvas.Children.Clear();
}

// Custom control.
public class ComponentWrapper : ComponentWrapperBase { }

// Custom base control.
public class ComponentWrapperBase : StackPanel
{
    public ComponentWrapperBase()
    {
        // Assign handler for the Initialized lifetime event (attached in code-behind).
        Initialized += (object sender, System.EventArgs e) => 
            Debug.WriteLine($"Initialized event on componentWrapperBase.");

        // Assign handler for the Loaded lifetime event (attached in code-behind).
        Loaded += (object sender, RoutedEventArgs e) => 
            Debug.WriteLine($"Loaded event on componentWrapperBase.");

        // Assign handler for the Unloaded lifetime event (attached in code-behind).
        Unloaded += (object sender, RoutedEventArgs e) => 
            Debug.WriteLine($"Unloaded event on componentWrapperBase.");
    }
}

/* Output:
Initialized event on textBox1.
Initialized event on textBox2.
Initialized event on componentWrapperBase.
Initialized event on componentWrapper.
Initialized event on outerStackPanel.

Loaded event on outerStackPanel.
Loaded event on componentWrapperBase.
Loaded event on componentWrapper.
Loaded event on textBox1.
Loaded event on textBox2.

Unloaded event on outerStackPanel.
Unloaded event on componentWrapperBase.
Unloaded event on componentWrapper.
Unloaded event on textBox1.
Unloaded event on textBox2.
*/
```

在以下情况下，WPF 事件系统会在元素上引发 Initialized 事件：

+ 设置元素的属性时。

+ 大约在同一时间通过调用对象构造函数对其进行初始化。

某些元素属性（如 Panel.Children）可以包含子元素。 父元素在初始化其子元素之前无法报告初始化。 因此，从元素树中嵌套最深的元素开始设置属性值，后跟连续父元素，一直到应用程序根。 由于在设置元素的属性时发生 Initialized 事件，因此首先在标记中定义的嵌套最深的元素上调用该事件，后跟连续父元素，一直到应用程序根。 在代码隐藏中动态创建对象时，其初始化可能不按顺序进行。

WPF 事件系统不会等待元素树中的所有元素都完成初始化，然后再对元素引发 Initialized 事件。 **因此，在为任何元素编写 Initialized 事件处理程序时，请记住，逻辑树或可视化树中的周围元素（尤其是父元素）可能尚未创建。 或者，其成员变量和数据绑定可能未初始化。**


在以下情况下，WPF 事件系统会在元素上引发 Loaded 事件：

+ 当包含该元素的逻辑树完成并连接到演示文稿源时。 演示源提供窗口句柄 (HWND) 和呈现图面。

+ 当数据绑定到本地源（例如其他属性或直接定义的数据源）完成时。

+ 在布局系统已计算呈现所需的所有值后。

+ 在最终呈现之前。

在加载逻辑树中的所有元素之前，不会在元素树中的任何元素上引发 Loaded 事件。 WPF 事件系统首先在元素树的根元素上引发 Loaded 事件，然后在每个连续的子元素上向下引发嵌套最深的元素。 尽管此事件可能类似于隧道路由事件，但 Loaded 事件不会将事件数据从一个元素传输到另一个元素，因此将事件标记为已处理没有效果。


在以下情况下，WPF 事件系统会在元素上引发 Unloaded 事件：

+ 删除其演示文稿源时，或

+ 删除其视觉对象父级时。

WPF 事件系统首先在元素树的根元素上引发 Unloaded 事件，然后在每个连续的子元素上向下引发嵌套最深的元素。 尽管此事件可能类似于隧道路由事件，但 Unloaded 事件不会将事件数据在元素间传播，因此将事件标记为已处理没有效果。

在 Unloaded 元素上引发事件时，它的父元素或逻辑树或可视化树中更高级的元素可能已取消设置。 取消设置意味着元素的数据绑定、资源引用和样式不再设置为其正常或上次已知运行时值。


### 弱事件模式

对事件的侦听可能会导致内存泄漏，每当源的对象生存期超出侦听器的有用对象生存期时，侦听器的存活时间比必要时间要长。 在这种情况下，未分配的内存相当于内存泄漏。

弱事件模式旨在解决内存泄漏问题。 当侦听器需要注册事件时，都可以使用弱事件模式，但侦听器并不明确知晓事件会在何时注销。 当源的对象生存期超过侦听器的有用对象生存期时，也可以使用弱事件模式。 在这种情况下，有用与否将由你来决定。 弱事件模式允许侦听器注册事件和接收事件，而不会以任何方式影响侦听器的对象生存期特征。 实际上，对源的隐式引用并不能确定侦听器是否有资格执行垃圾回收。 由于是弱引用，因而引用是对弱事件模式和相关 API 的命名。 侦听器可以被垃圾回收或以其他方式销毁，而源可以继续运行，无需保留针对现已销毁的对象的不可回收的处理程序引用。



### 常见任务

#### 使用代码添加事件处理程序

使用 XAML 定义名为 ButtonCreatedByXaml 的 Button 并分配 ButtonCreatedByXaml_Click 方法作为其 Click 事件处理程序。 Click 是派生自 ButtonBase 的按钮的内置路由事件：

```xaml
<StackPanel Name="StackPanel1">
    <Button
        Name="ButtonCreatedByXaml" 
        Click="ButtonCreatedByXaml_Click"
        Content="Create a new button with an event handler"
        Background="LightGray">
    </Button>
</StackPanel>
```

事件代码的实现：

```csharp
// The click event handler for the existing button 'ButtonCreatedByXaml'.
private void ButtonCreatedByXaml_Click(object sender, RoutedEventArgs e)
{
    // Create a new button.
    Button ButtonCreatedByCode = new();

    // Specify button properties.
    ButtonCreatedByCode.Name = "ButtonCreatedByCode";
    ButtonCreatedByCode.Content = "New button and event handler created in code";
    ButtonCreatedByCode.Background = Brushes.Yellow;

    // Add the new button to the StackPanel.
    StackPanel1.Children.Add(ButtonCreatedByCode);

    // Assign an event handler to the new button using the '+=' operator.
    ButtonCreatedByCode.Click += new RoutedEventHandler(ButtonCreatedByCode_Click);

    // Assign an event handler to the new button using the AddHandler method.
    // AddHandler(ButtonBase.ClickEvent, new RoutedEventHandler(ButtonCreatedByCode_Click);

    // Assign an event handler to the StackPanel using the AddHandler method.
    StackPanel1.AddHandler(ButtonBase.ClickEvent, new RoutedEventHandler(ButtonCreatedByCode_Click));
}
// The Click event handler for the new button 'ButtonCreatedByCode'.
private void ButtonCreatedByCode_Click(object sender, RoutedEventArgs e)
{
    string sourceName = ((FrameworkElement)e.Source).Name;
    string senderName = ((FrameworkElement)sender).Name;

    Debug.WriteLine($"Routed event handler attached to {senderName}, " +
        $"triggered by the Click routed event raised by {sourceName}.");
}
```



## 样式和模板

### 概述

```xaml
<Window.Resources>
    <!-- .... other resources .... -->

	<!-- 自动应用于所有的 TextBlock 元素 -->
    <Style TargetType="TextBlock">
        <Setter Property="HorizontalAlignment" Value="Center" />
        <Setter Property="FontFamily" Value="Comic Sans MS"/>
        <Setter Property="FontSize" Value="14"/>
    </Style>
    
    <!-- 该样式需要显式引用，引用时使用 Key -->
    <Style BasedOn="{StaticResource {x:Type TextBlock}}"
           TargetType="TextBlock"
           x:Key="TitleText">
        <Setter Property="FontSize" Value="26"/>
        <Setter Property="Foreground">
            <Setter.Value>
                <LinearGradientBrush StartPoint="0.5,0" EndPoint="0.5,1">
                    <LinearGradientBrush.GradientStops>
                        <GradientStop Offset="0.0" Color="#90DDDD" />
                        <GradientStop Offset="1.0" Color="#5BFFFF" />
                    </LinearGradientBrush.GradientStops>
                </LinearGradientBrush>
            </Setter.Value>
        </Setter>
    </Style>
</Window.Resources>
<StackPanel>
    <!-- 显式引用 -->
    <TextBlock Style="{StaticResource TitleText}" Name="textblock1">My Pictures</TextBlock>
    <TextBlock>Check out my new pictures!</TextBlock>
</StackPanel>
```

除了上面这两种引用方式，还可以以编程方式应用样式：

```csharp
textblock1.Style = (Style)Resources["TitleText"];
```

将 TargetType 属性设置为 TextBlock 时，如果不为样式分配 x:Key，会导致将样式应用于所有 TextBlock 元素。 在此情况下，x:Key 隐式设置为 {x:Type TextBlock}。

在 WPF 中，控件的 ControlTemplate 用于定义控件的外观。 可以通过定义新的 ControlTemplate 并将其分配给控件来更改控件的结构和外观。 每个控件都有一个分配给 Control.Template 属性的默认模板。 该模板将控件的视觉呈现与控件的功能关联起来。控件模板比样式复杂得多。 这是因为控件模板重写了整个控件的视觉外观，而样式只是将属性更改应用于现有控件。 但是，控件模板是通过设置 Control.Template 属性来应用的，因此可以使用样式来定义或设置模板。设计器通常允许创建现有模板的副本并进行修改。 例如，在 Visual Studio WPF 设计器中，选择一个 CheckBox 控件，然后右键单击并选择“编辑模板”>“创建副本”。 此命令会生成一个用于定义模板的样式。

根据属性的值设置属性值或启动操作的 Trigger 称为属性触发器。若要演示如何使用属性触发器，可以使每个 ListBoxItem 在未选中时部分透明。 以下样式将 ListBoxItem 的 Opacity 值设置为 0.5。 但是，当 IsSelected 属性为 true 时，Opacity 设置为 1.0。

```xaml
<Window.Resources>
    <!-- .... other resources .... -->
    <Style TargetType="ListBoxItem">
        <Setter Property="Opacity" Value="0.5" />
        <Setter Property="MaxHeight" Value="75" />
        <Style.Triggers>
            <Trigger Property="IsSelected" Value="True">
                <Trigger.Setters>
                    <Setter Property="Opacity" Value="1.0" />
                </Trigger.Setters>
            </Trigger>
        </Style.Triggers>
    </Style>
</Window.Resources>
```

另一个触发器类型是 EventTrigger，用于根据某个事件的发生启动一组操作。

```xaml
<Style.Triggers>
    <EventTrigger RoutedEvent="Mouse.MouseEnter">
        <EventTrigger.Actions>
            <BeginStoryboard>
                <Storyboard>
                    <DoubleAnimation Duration="0:0:1" Storyboard.TargetProperty="Opacity" From="0.0" To="1.0"/>
                </Storyboard>
            </BeginStoryboard>
        </EventTrigger.Actions>
    </EventTrigger>
</Style.Triggers>
```



### 非矩形窗口样式

```xaml
<Window x:Class="WindowsOverview.ClippedWindow"
        xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
        xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
        Title="ClippedWindow" SizeToContent="WidthAndHeight"
        WindowStyle="None" AllowsTransparency="True" Background="Transparent">
    <Grid Margin="20">
        <Grid.RowDefinitions>
            <RowDefinition Height="*"/>
            <RowDefinition Height="20"/>
        </Grid.RowDefinitions>

        <Rectangle Stroke="#FF000000" RadiusX="10" RadiusY="10"/>
        <Path Fill="White" Stretch="Fill" Stroke="#FF000000" HorizontalAlignment="Left" Margin="15,-5.597,0,-0.003" Width="30" Grid.Row="1" Data="M22.166642,154.45381 L29.999666,187.66699 40.791059,154.54395"/>
        <Rectangle Fill="White" RadiusX="10" RadiusY="10" Margin="1"/>
        
        <TextBlock HorizontalAlignment="Left" VerticalAlignment="Center" FontSize="25" Text="Greetings!" TextWrapping="Wrap" Margin="5,5,50,5"/>
        <Button HorizontalAlignment="Right" VerticalAlignment="Top" Background="Transparent" BorderBrush="{x:Null}" Foreground="Red" Content="❌" FontSize="15" />

        <Grid.Effect>
            <DropShadowEffect BlurRadius="10" ShadowDepth="3" Color="LightBlue"/>
        </Grid.Effect>
    </Grid>
</Window>
```



### XAML 转写为 CSharp 代码

假设我们想要实现下面的显示效果：

在 XAML 中

```xaml
<ListView x:Name="filesTree" Margin="75,133,330,74" UseLayoutRounding="False" BorderBrush="#FF004889" Background="#FFF4F4F4">
    <ListViewItem>
        <StackPanel Orientation="Horizontal">
            <Path Fill="#FF368CF9" Data="M0 2.75C0 1.784.784 1 1.75 1H5c.55 0 1.07.26 1.4.7l.9 1.2a.25.25 0 0 0 .2.1h6.75c.966 0 1.75.784 1.75 1.75v8.5A1.75 1.75 0 0 1 14.25 15H1.75A1.75 1.75 0 0 1 0 13.25Zm9.42 9.36 2.883-2.677a.25.25 0 0 0 0-.366L9.42 6.39a.249.249 0 0 0-.42.183V8.5H4.75a.75.75 0 0 0 0 1.5H9v1.927c0 .218.26.331.42.183Z"></Path>
            <Rectangle Width="8" />
            <TextBlock>Text</TextBlock>
        </StackPanel>
    </ListViewItem>
</ListView>
```

在 CSharp 中对应的实现为

```csharp
StackPanel panel= new StackPanel();
System.Windows.Shapes.Path path = new System.Windows.Shapes.Path();
PathGeometry geometry = new PathGeometry();
geometry.AddGeometry(Geometry.Parse("M0 2.75C0 1.784.784 1 1.75 1H5c.55 0 1.07.26 1.4.7l.9 1.2a.25.25 0 0 0 .2.1h6.75c.966 0 1.75.784 1.75 1.75v8.5A1.75 1.75 0 0 1 14.25 15H1.75A1.75 1.75 0 0 1 0 13.25Zm9.42 9.36 2.883-2.677a.25.25 0 0 0 0-.366L9.42 6.39a.249.249 0 0 0-.42.183V8.5H4.75a.75.75 0 0 0 0 1.5H9v1.927c0 .218.26.331.42.183Z"));
path.Data = geometry;
path.Fill= new SolidColorBrush(Color.FromRgb(54, 140, 249));

panel.Children.Add(path);
panel.Children.Add(new Rectangle
{
    Width = 8
});
panel.Children.Add(new TextBlock
{
    Text = "Text",    
});
panel.Orientation = Orientation.Horizontal;
filesTree.Items.Add(panel);
```

注意由于 `StackPanel` 无法添加鼠标双击事件，为了更加方便后面的操作，可以将 `StackPanel` 加到 `ListViewItem` 中

```c#
ListViewItem item = new ListViewItem { 
    Content = panel,		// 设置属性 Content
};
item.MouseDoubleClick += Item_MouseDoubleClick;   // 添加双击事件
filesTree.Items.Add(item);
```



>  在实现这些效果时，先通过 XAML 确定使用哪些组件，再在CSharp找到同名的类，具体实现时需要经常查阅文档来确定对应的方法





## 组件

### 右键菜单

为一个 `ListViewItem` 类实例 `item` 添加右键菜单：

```csharp
ContextMenu menu = new ContextMenu();
MenuItem menuItem = new MenuItem();
menuItem.Header = "菜单";
menuItem.Icon = parseStroke(stroke_download, color);
menuItem.Click += MenuItem_Click;
menu.Items.Add(menuItem);
item.ContextMenu = menu;
```

注意此处在 `MenuItem_Click` 中通过 `ListView` 的 `SelectedIndex` 属性来找到对应的 `item` 是一个推荐的方法（当然可以通过 Parent 属性一步步找到 `item`）。对于有明确 `id` 的组件，直接通过 `id` 访问即可。





## 资源

### 在 WPF 中使用 SVG

一个完整的SVG的代码如下：

```xml
<svg t="1709188552602" class="icon" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="1809" width="200" height="200"><path d="M483.555556 312.888889m28.444444 0l0 0q28.444444 0 28.444444 28.444444l0 341.333334q0 28.444444-28.444444 28.444444l0 0q-28.444444 0-28.444444-28.444444l0-341.333334q0-28.444444 28.444444-28.444444Z" p-id="1810"></path></svg>
```

在XAML中

```xaml
<Path Fill="#FF368CF9" Data="M0 2.75C0 1.784.784 1 1.75 1H5c.55 0 1.07.26 1.4.7l.9 1.2a.25.25 0 0 0 .2.1h6.75c.966 0 1.75.784 1.75 1.75v8.5A1.75 1.75 0 0 1 14.25 15H1.75A1.75 1.75 0 0 1 0 13.25Zm9.42 9.36 2.883-2.677a.25.25 0 0 0 0-.366L9.42 6.39a.249.249 0 0 0-.42.183V8.5H4.75a.75.75 0 0 0 0 1.5H9v1.927c0 .218.26.331.42.183Z"></Path>
```

在 CSharp 中

```csharp
System.Windows.Shapes.Path path = new System.Windows.Shapes.Path();
PathGeometry geometry = new PathGeometry();
geometry.AddGeometry(Geometry.Parse("M0 2.75C0 1.784.784 1 1.75 1H5c.55 0 1.07.26 1.4.7l.9 1.2a.25.25 0 0 0 .2.1h6.75c.966 0 1.75.784 1.75 1.75v8.5A1.75 1.75 0 0 1 14.25 15H1.75A1.75 1.75 0 0 1 0 13.25Zm9.42 9.36 2.883-2.677a.25.25 0 0 0 0-.366L9.42 6.39a.249.249 0 0 0-.42.183V8.5H4.75a.75.75 0 0 0 0 1.5H9v1.927c0 .218.26.331.42.183Z"));
path.Data = geometry;
path.Fill= new SolidColorBrush(Color.FromRgb(54, 140, 249));
```



>  使用 inkscape 如何修改自己想要的 svg 尺寸
>
> 1. 在网站中下载到svg文件，打开svg文件，将width、height 属性设置与 viewbox 相同大小
>
> 下载的原始svg
>
> ```xml
> class="icon" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="1962" width="16" height="16"
> ```
>
> 修改后的 svg
>
> ```xml
> class="icon" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="1962" width="1024" height="1024"
> ```
>
> 2. 使用 inkscape 将 svg 修改至适当的大小（先修改文档大小，再缩放svg）





## 类型转换

### 颜色

##### 16进制 string ->  color

```c#
Color color = (Color)ColorConverter.ConvertFromString(hexcolor)
```

##### color -> Brush

```csharp
Brush brush = new SolidColorBrush(color);
```



## 高级操作

### 深拷贝

在 WPF 中，组件之间存在关联关系，单纯的浅复制无法满足要求，甚至会报错。假设我们想把一个 `ListView` 组件 `LV1` 的第一项复制到另一个 `ListView` 组件 `LV2`。

下面的操作会报错：

```csharp
ListViewItem item = LV1.Items[0];
LV2.Items.Add(item);
// 报错：system.invalidoperationexception:“元素已具有逻辑父级。将其附加到新的父级之前必须将其与旧父级断开。”
```

下面的操作会把 `LV1` 中第一项的 `Content` 的父级从 `LV1.Items[0]` 转为 `LV2.Items[0]`：

```csharp
ListViewItem item = LV1.Items[0];
ListViewItem nitem = new ListViewItem();
nitem.Content = item.Content;
LV2.Items.Add(nitem); // 不会报错，但是存在很大问题
```

正确的做法是采用深拷贝的方式：

```csharp
StackPanel panel = (StackPanel)((ListViewItem)LV1.Items[0]).Content;
TextBlock tb = (TextBlock)panel.Children[2];
string name = (string)tb.Text.Clone();
string[] tag = (string[])tb.Tag;
string lpath = (string)tag[0].Clone();
string type = (string)tag[1].Clone();
ListViewItem nItem = createItem(name, lpath, type, doubleclick:false);
LV1.Items.Add(nItem);
```

上面的 `createItem` 是创建 item 的函数，需要将原本的列表项逐层分解到最基本的数据类型的数据，并且进行 `Clone()`（不使用 `Clone()` 似乎也行）。



### 如何看 C# 的文档

对于一个 C# 中的一个类，一般会有定义、示例、注解、构造函数、属性、方法、事件、显式接口实现、扩展方法等。

构造函数：给出如何创建类的一个实例。

属性：一种成员，它提供灵活的机制来读取、写入或计算私有字段的值。如果属性中有 Item[Int32] 这种属性，表示该类可以通过 [] 访问，如 `List<T>` 类的一个实例 list，可以通过 list[0] 访问第一个元素。

方法：包含一系列语句的代码块。 程序通过调用该方法并指定任何所需的方法参数使语句得以执行。

事件：如 DataTableCollection 类中有两个事件，这两个事件会在添加或移除 DataTableCollection 对象时或之后发生。

显式接口实现：可以调用的接口，不过需要显式转换。如 DataSet 类本身没有 GetList 方法，而显式接口实现中存在 IListSource.GetList() 的接口实现，所以存在下面的代码实现：

```csharp
DataSet dataSet = new DataSet();
var a = ((IListSource)dataSet).GetList();
```

扩展方法：能够向现有类型“添加”方法，而无需创建新的派生类型、重新编译或以其他方式修改原始类型。使用时可以直接当成方法来用，如 `List<T>` 中的 OrderBy 方法便是扩展方法。



## 演练

### 使用 Grid 动态布局

[演练：构造动态布局 | Microsoft Learn](https://learn.microsoft.com/zh-cn/previous-versions/visualstudio/visual-studio-2010/bb514519(v=vs.100))

[演练：使用 WPF 设计器创建大小可调的应用程序 | Microsoft Learn](https://learn.microsoft.com/zh-cn/previous-versions/visualstudio/visual-studio-2010/bb546954(v=vs.100))

通过为 Grid 定义四行四列，通过设置 Grid.Column 和 Grid.Column 将组件放在对应的行和列中，通过设置 Grid.ColumnSpan 和 Grid.RowSpan 所占据的范围。

```xaml
<Window x:Class="WPFLearn1.DynamicLayout"
        xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
        xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
        xmlns:d="http://schemas.microsoft.com/expression/blend/2008"
        xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006"
        xmlns:local="clr-namespace:WPFLearn1"
        mc:Ignorable="d"
        Title="DynamicLayout" Height="200" Width="400" SizeToContent="WidthAndHeight">
    <Grid>
        <Grid.RowDefinitions>
            <RowDefinition Height="Auto"/>
            <RowDefinition Height="Auto"/>
            <RowDefinition/>
            <RowDefinition Height="Auto"/>
        </Grid.RowDefinitions>
        <Grid.ColumnDefinitions>
            <ColumnDefinition Width="Auto"/>
            <ColumnDefinition/>
            <ColumnDefinition Width="Auto"/>
            <ColumnDefinition Width="Auto"/>
        </Grid.ColumnDefinitions>
        <Label Grid.Column="0" Content="Name:" Margin="20,10,20,10" VerticalAlignment="Top" Height="23"/>
        <Label Content="Password:" Margin="20,10,20,10" VerticalAlignment="Top" Height="23" Grid.Row="1"/>
        <TextBox Grid.Row="0" Grid.Column="1" Margin="10,10,20,10" TextWrapping="Wrap" Text="TextBox" Grid.ColumnSpan="3"/>
        <TextBox Grid.Row="1" Grid.Column="1" Margin="10,10,20,10" TextWrapping="Wrap" Text="TextBox" Grid.ColumnSpan="3"/>
        <Button Grid.Column="2" Content="确定" Margin="10,10,6,20" Grid.Row="3" Width="75" Height="23"/>
        <Button Grid.Column="3" Content="取消" Margin="6,10,20,20" Grid.Row="3" Width="75" Height="23"/>
    </Grid>
</Window>
```

在 WPF 中，star "*" 的作用是按比例调整大小。例如下面的语句将30%分配给第1列，70%分配给第2列

```xaml
<ColumnDefinition Width="3*" />
<ColumnDefinition Width="7*" />
```

除了使用 Grid 的行和列，还可以使用 GridSplitter 帮助布局：

```xaml
<Window x:Class="WPFLearn1.ResizableApplication"
        xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
        xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
        xmlns:d="http://schemas.microsoft.com/expression/blend/2008"
        xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006"
        xmlns:local="clr-namespace:WPFLearn1"
        mc:Ignorable="d"
        Title="ResizableApplication" Height="450" Width="800">
    <Grid>
        <Grid.RowDefinitions>
            <RowDefinition/>
            <RowDefinition Height="Auto"/>
            <RowDefinition MinHeight="70"/>
        </Grid.RowDefinitions>
        <GridSplitter HorizontalAlignment="Stretch" Height="10" ResizeDirection="Rows" Grid.Row="1"/>
        <DockPanel>
            <Label Content="显示" Height="23" Background="Blue" Foreground="White" DockPanel.Dock="Top"/>
            <RichTextBox Background="LightBlue" DockPanel.Dock="Bottom" IsReadOnly="True"></RichTextBox>
        </DockPanel>
        <Grid Grid.Row="2">
            <Grid.ColumnDefinitions>
                <ColumnDefinition/>
                <ColumnDefinition Width="Auto"/>
            </Grid.ColumnDefinitions>
            <Button Content="确定" Margin="5,0,0,0" Grid.Column="1" Width="60" Height="60"/>
            <RichTextBox Background="PaleGoldenrod"></RichTextBox>
        </Grid>

    </Grid>
</Window>
```



### DataGrid 控件显示 Mysql 的数据

新建一个窗口，添加一个 DataGrid 控件，添加 Window 的 loaded 事件，在 Window_Loaded 添加下面的代码：

```csharp
string conStr = "server=localhost;user id=root;password=XMJsql123456;database=library";
string sql = "select * from library.book";
MySqlConnection con = new MySqlConnection(conStr);
con.Open();
MySqlDataAdapter da = new MySqlDataAdapter(sql, con);
DataSet ds = new DataSet();
da.Fill(ds);
dataGrid1.ItemsSource = ((IListSource)ds.Tables[0]).GetList();
con.Close();
```

[C# WinForm/WPF 实现数据库连接与操作(MySQL)_wpf mysql-CSDN博客](https://blog.csdn.net/u013518478/article/details/129594959)

[DataSet 类 (System.Data) | Microsoft Learn](https://learn.microsoft.com/zh-cn/dotnet/api/system.data.dataset?view=net-8.0)

[MySQL :: MySQL Connector/NET Developer Guide :: 4 Connector/NET Connections](https://dev.mysql.com/doc/connector-net/en/connector-net-connections.html)











# ASP.NET Core

## ASP.NET Core 中的 Razor Pages 和 Entity Framework Core

[ASP.NET Core 中的 Razor Pages 和 Entity Framework Core - 第 1 个教程（共 8 个） | Microsoft Learn](https://learn.microsoft.com/zh-cn/aspnet/core/data/ef-rp/intro?view=aspnetcore-8.0&tabs=visual-studio)


>在 [ASP.NET Core Razor Pages](https://learn.microsoft.com/zh-cn/aspnet/core/razor-pages/?view=aspnetcore-8.0) 应用中使用 Entity Framework (EF) Core，为虚构的 Contoso University 生成一个网站。

在“创建新项目”对话框中，选择“ASP.NET Core Web 应用”


`Pages/Shared/_Layout.cshtml` 中为网站格式，可以根据需求修改

`Pages/Index.cshtml` 中为网站首页的内容

`Models`：存放数据模型，各种实体（学生、课程等）

`Data`：包括初始数据和数据上下文

项目数据库的位置在解决方案资源管理器、Connected Services、在 SQL 对象编辑器打开、`(localdb)\MSSQLLocalDB` 、数据库。


### 创建、读取、更新和删除（CRUD）

#### 读取注册

读取数据使用 `FirstOrDefaultAsync` ，如果未找到任何内容，则此方法返回 NULL；否则，它将返回满足查询筛选条件的第一行。 `FirstOrDefaultAsync` 通常是比 `SingleOrDefaultAsync` 和 `FindAsync` 更好的选择：

```csharp
public async Task<IActionResult> OnGetAsync(int? id)
{
    if (id == null)
    {
        return NotFound();
    }

    Student = await _context.Students.FirstOrDefaultAsync(m => m.ID == id);

    if (Student == null)
    {
        return NotFound();
    }
    return Page();
}
```

下面的代码可以读取更多的数据：

```csharp
public async Task<IActionResult> OnGetAsync(int? id)
{
    if (id == null)
    {
        return NotFound();
    }

    Student = await _context.Students
        .Include(s => s.Enrollments)
        .ThenInclude(e => e.Course)
        .AsNoTracking()
        .FirstOrDefaultAsync(m => m.ID == id);

    if (Student == null)
    {
        return NotFound();
    }
    return Page();
}
```

`Include` 和 `ThenInclude` 方法使上下文加载 `Student.Enrollments` 导航属性，并在每个注册中加载 `Enrollment.Course` 导航属性。对于返回的实体未在当前上下文中更新的情况，`AsNoTracking` 方法将会提升性能。

注意还要在对应的 cshtml 加上显示的代码：

```xml
<dt class="col-sm-2"> @Html.DisplayNameFor(model => model.Student.Enrollments) </dt> <dd class="col-sm-10"> <table class="table"> <tr> <th>Course Title</th> <th>Grade</th> </tr> @foreach (var item in Model.Student.Enrollments) { <tr> <td> @Html.DisplayFor(modelItem => item.Course.Title) </td> <td> @Html.DisplayFor(modelItem => item.Grade) </td> </tr> } </table> </dd>
```


#### 更新“创建”页

“创建”页面的基架 `OnPostAsync` 代码容易受到[过多发布攻击](https://learn.microsoft.com/zh-cn/aspnet/core/data/ef-rp/crud?view=aspnetcore-8.0#overposting)。 将 `Pages/Students/Create.cshtml.cs` 中的 `OnPostAsync` 方法替换为以下代码。

```csharp
public async Task<IActionResult> OnPostAsync()
{
    var emptyStudent = new Student();

    if (await TryUpdateModelAsync<Student>(
        emptyStudent,
        "student",   // Prefix for form value.
        s => s.FirstMidName, s => s.LastName, s => s.EnrollmentDate))
    {
        _context.Students.Add(emptyStudent);
        await _context.SaveChangesAsync();
        return RedirectToPage("./Index");
    }

    return Page();
}
```


#### 更新“编辑”页

在 `Pages/Students/Edit.cshtml.cs` 中，使用以下代码替换 `OnGetAsync` 和 `OnPostAsync` 方法。

```csharp
public async Task<IActionResult> OnGetAsync(int? id)
{
    if (id == null)
    {
        return NotFound();
    }

    Student = await _context.Students.FindAsync(id);

    if (Student == null)
    {
        return NotFound();
    }
    return Page();
}

public async Task<IActionResult> OnPostAsync(int id)
{
    var studentToUpdate = await _context.Students.FindAsync(id);

    if (studentToUpdate == null)
    {
        return NotFound();
    }

    if (await TryUpdateModelAsync<Student>(
        studentToUpdate,
        "student",
        s => s.FirstMidName, s => s.LastName, s => s.EnrollmentDate))
    {
        await _context.SaveChangesAsync();
        return RedirectToPage("./Index");
    }

    return Page();
}
```

 `FirstOrDefaultAsync` 已替换为 `FindAsync`。 不需要包含相关数据时，`FindAsync` 效率更高。


#### 更新“删除”页


将 `Pages/Students/Delete.cshtml.cs` 中的代码替换为以下代码：

```csharp
namespace ContosoUniversity.Pages.Students
{
    public class DeleteModel : PageModel
    {
        private readonly ContosoUniversity.Data.SchoolContext _context;
        private readonly ILogger<DeleteModel> _logger;

        public DeleteModel(ContosoUniversity.Data.SchoolContext context,
                           ILogger<DeleteModel> logger)
        {
            _context = context;
            _logger = logger;
        }

        [BindProperty]
        public Student Student { get; set; }
        public string ErrorMessage { get; set; }

        public async Task<IActionResult> OnGetAsync(int? id, bool? saveChangesError = false)
        {
            if (id == null)
            {
                return NotFound();
            }

            Student = await _context.Students
                .AsNoTracking()
                .FirstOrDefaultAsync(m => m.ID == id);

            if (Student == null)
            {
                return NotFound();
            }

            if (saveChangesError.GetValueOrDefault())
            {
                ErrorMessage = String.Format("Delete {ID} failed. Try again", id);
            }

            return Page();
        }

        public async Task<IActionResult> OnPostAsync(int? id)
        {
            if (id == null)
            {
                return NotFound();
            }

            var student = await _context.Students.FindAsync(id);

            if (student == null)
            {
                return NotFound();
            }

            try
            {
                _context.Students.Remove(student);
                await _context.SaveChangesAsync();
                return RedirectToPage("./Index");
            }
            catch (DbUpdateException ex)
            {
                _logger.LogError(ex, ErrorMessage);

                return RedirectToAction("./Delete",
                                     new { id, saveChangesError = true });
            }
        }
    }
}
```


### 排序、筛选器、页面和组


使用以下代码替换 `Pages/Students/Index.cshtml.cs` 中的代码，以添加排序。

```csharp
public class IndexModel : PageModel
{
    private readonly SchoolContext _context;
    public IndexModel(SchoolContext context)
    {
        _context = context;
    }

    public string NameSort { get; set; }
    public string DateSort { get; set; }
    public string CurrentFilter { get; set; }
    public string CurrentSort { get; set; }

    public IList<Student> Students { get; set; }

    public async Task OnGetAsync(string sortOrder, string searchString)
    {
        // using System;
        NameSort = String.IsNullOrEmpty(sortOrder) ? "name_desc" : "";
        DateSort = sortOrder == "Date" ? "date_desc" : "Date";
        
		CurrentFilter = searchString;

        IQueryable<Student> studentsIQ = from s in _context.Students
                                        select s;

		// 筛选
        if (!String.IsNullOrEmpty(searchString)) 
        { 
        studentsIQ = studentsIQ.Where(s => s.LastName.Contains(searchString) || s.FirstMidName.Contains(searchString)); 
        }

		// 排序
        switch (sortOrder)
        {
            case "name_desc":
                studentsIQ = studentsIQ.OrderByDescending(s => s.LastName);
                break;
            case "Date":
                studentsIQ = studentsIQ.OrderBy(s => s.EnrollmentDate);
                break;
            case "date_desc":
                studentsIQ = studentsIQ.OrderByDescending(s => s.EnrollmentDate);
                break;
            default:
                studentsIQ = studentsIQ.OrderBy(s => s.LastName);
                break;
        }

        Students = await studentsIQ.AsNoTracking().ToListAsync();
    }
}
```




## Visual Studio 2022 连接 MySQL


### 连接操作

> ~~首先 Visual Studio 目前（2024年3月4日）不能直接连接 MySQL~~
> ~~参考教程：[【vs2022连接MySQL】_vs2022如何与mysql链接-CSDN博客](https://blog.csdn.net/conan04260426/article/details/131432789)~~

1. ~~下载好 MySQL 后，需要下载 MySQL 的 ODBC 驱动~~
2. ~~打开 ODBC 数据源（直接在搜索框内输入即可）~~
3. ~~默认没有 MySQL 数据源，添加数据源，选择 MySQL ODBC 8.0 Unicode Driver~~
4. ~~填写 Data Source name、User、Password 和 Database，点击完成即可~~
5. ~~进入 Visual Studio，点击 工具 连接到数据库，数据源选择其他，数据提供程序选择用于 ODBC 的 .net Framework 数据提供程序~~
6. ~~输入登录信息即可（MySQL 中的登录信息）~~



参考 [MySQL :: MySQL Connector/NET Developer Guide :: 7.2 Entity Framework Core Support](https://dev.mysql.com/doc/connector-net/en/connector-net-entityframework-core.html)

以模板 `ASP.NET Core 空` 创建项目，安装 `MySql.EntityFrameworkCore` 包。

### 创建数据库

创建文件 `LibraryModel.cs`

```csharp
namespace TestConnectToMySQL.Models
{
    public class LibraryModel
    {

    }

    public class Book
    {
        public string? ISBN { get; set; }
        public string? Title { get; set; }
        public string? Author { get; set; }
        public string? Language { get; set; }
        public int Pages { get; set; }
        public virtual Publisher? Publisher { get; set; }
    }

    public class Publisher
    {
        public int ID { get; set; }
        public string? Name { get; set; }
        public virtual ICollection<Book>? Books { get; set; }
    }
}
```

创建文件 `LibraryContext.cs`

```csharp
using Microsoft.EntityFrameworkCore;

namespace TestConnectToMySQL.Models
{
    public class LibraryContext: DbContext
    {
        public DbSet<Book>? Book { get; set; }

        public DbSet<Publisher>? Publisher { get; set; }

        protected override void OnConfiguring(DbContextOptionsBuilder optionsBuilder)
        {
            optionsBuilder.UseMySQL("server=localhost;database=library;user=root;password=XMJsql123456");
        }

        protected override void OnModelCreating(ModelBuilder modelBuilder)
        {
            base.OnModelCreating(modelBuilder);

            modelBuilder.Entity<Publisher>(entity =>
            {
                entity.HasKey(e => e.ID);
                entity.Property(e => e.Name).IsRequired();
            });

            modelBuilder.Entity<Book>(entity =>
            {
                entity.HasKey(e => e.ISBN);
                entity.Property(e => e.Title).IsRequired();
                entity.HasOne(d => d.Publisher)
                  .WithMany(p => p.Books);
            });
        }

    }
}
```


将 `Program.cs` 改写如下

```csharp
using Microsoft.EntityFrameworkCore;
using Org.BouncyCastle.Security;
using System.Text;
using TestConnectToMySQL.Models;
using static Microsoft.EntityFrameworkCore.DbLoggerCategory.Database;

namespace TestConnectToMySQL
{
    class Program
    {
        static void Main(string[] args)
        {
            var builder = WebApplication.CreateBuilder(args);
            var app = builder.Build();
            InsertData();
            app.MapGet("/", () => PrintData());
            app.Run();
        }
        private static void InsertData()
        {
            using (var context = new LibraryContext())
            {
                context.Database.EnsureCreated();
                // 添加出版社
                var publisher = new Publisher
                {
                    Name = "Mariner Books",
                };
                context.Publisher.Add(publisher);

                // 添加一些书
                context.Book.Add(new Book
                {
                    ISBN = "978-0544003415",
                    Title = "The Lord of the Rings",
                    Author = "J.R.R. Tolkien",
                    Language = "English",
                    Pages = 1216,
                    Publisher = publisher
                });
                context.Book.Add(new Book
                {
                    ISBN = "978-0547247762",
                    Title = "The Sealed Letter",
                    Author = "Emma Donoghue",
                    Language = "English",
                    Pages = 416,
                    Publisher = publisher
                });
                // 保存修改
                context.SaveChanges();
            }
        }
        private static string PrintData()
        {
            using (var context = new LibraryContext())
            {
                var books = context.Book.Include(p => p.Publisher);
                var data = new StringBuilder();
                int i = 1;
                foreach (var book in books)
                {
                    data.AppendLine($"Book {i}");
                    data.AppendLine($"ISBN: {book.ISBN}");
                    data.AppendLine($"Title: {book.Title}");
                    data.AppendLine($"Publisher: {book.Publisher.Name}");
                    data.AppendLine();
                    i++;
                }
                return data.ToString();
            }
        }
    }
}
```

### 操作已有数据库

安装 Nuget 包

```txt
Microsoft.EntityFrameworkCore.Design	 7.0.16
MySql.EntityFrameworkCore      		     8.0.0   // 不一定需要
Pomelo.EntityFrameworkCore.MySql		 7.0.0
Microsoft.EntityFrameworkCore             7.0.16 
```



可以使用命令行直接从 MySql 中创建类，在 ASP.NET Web 项目中创建文件夹 Models，执行下面的命令：

```sh
dotnet ef dbcontext scaffold "server=localhost;uid=root;pwd=XMJsql123456;database=sakila" Pomelo.EntityFrameworkCore.MySql -o Models -t actor -t film -t film_actor -t language -f
```

这里的 `connection-string` 的格式如下：

```txt
"server=主机名;uid=用户名;pwd=密码;database=数据库名字"
```

上面的命令会直接从数据库中创建类。





## 使用 JavaScript 调用 ASP.NET Core Web API

[教程：使用 JavaScript 调用 ASP.NET Core Web API | Microsoft Learn](https://learn.microsoft.com/zh-cn/aspnet/core/tutorials/web-api-javascript?view=aspnetcore-6.0)



使用 fetch 函数来启动 HTTP 请求，返回 Promise 对象，该对象包含表示为 `Response` 对象的 HTTP 响应。 常见模式是通过调用 `Response` 对象上的 `json` 函数来提取 JSON 响应正文。



