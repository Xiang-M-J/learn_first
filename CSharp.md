

# CSharp

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
        {
            
        }
        public Result Run(string command, string WorkingDirectory="")
        {
            Process process = new Process();
            process.StartInfo.FileName = "cmd.exe";
            process.StartInfo.UseShellExecute = false; // 是否使用操作系统shell启动
            process.StartInfo.RedirectStandardError = true;	// 是否有标准错误
            process.StartInfo.RedirectStandardOutput = true;	// 是否有标准输出
            process.StartInfo.RedirectStandardInput = true;		// 是否有标准输入
            process.StartInfo.CreateNoWindow = false;	// 是否无窗口
            if (WorkingDirectory != "") {				// 设置工作目录，不设置该项，则默认为与程序共同路径。
                process.StartInfo.WorkingDirectory = WorkingDirectory;
            }
            process.Start();
            process.StandardInput.WriteLine(command + "&exit");		// 加上 exit 确保退出，不会假死。
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
    string content = await GetHtmlContentAsync(url);	// 
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

## XAML 转写为 CSharp 代码

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





## 转换

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



