API文档：https://api.flutter.dev/flutter

[本章目录 | 《Flutter实战·第二版》 (flutterchina.club)](https://book.flutterchina.club/chapter1/)



> flutter json 转 model，使用 json_to_model

## 入门知识

### 基本命令

`flutter doctor`：检查一下 `flutter` 环境是否有问题

`flutter create project_name`：新建项目工程（只能小写）

```cmd
cd project_name
flutter run
```

`flutter pub add <package>`：添加包



flutter 构建 App，在项目路径下执行

```powershell
flutter build apk
```

flutter 编译 web 应用

```sh
flutter build web
```

使用 --web-renderer 选择使用 html 或是 canvaskit 渲染

```sh
flutter build web --web-renderer html
```

在默认选项下以发行模式构建

```sh
flutter build web --release
```



 

### 基本知识

`flutter` 是跨平台的，一套代码适用于 ios、Android、web、Macos、Linux 和 windows。对于不需要的平台，可以直接删除文件夹。

`pubspec.yaml` 文件中声明了依赖、flutter 使用的资源



## 控件

**flutter 中可以放置多个控件的容器**：

1. [Row](https://api.flutter.dev/flutter/widgets/Row-class.html)和[Column](https://api.flutter.dev/flutter/widgets/Column-class.html)

2. [GridView](https://api.flutter.dev/flutter/widgets/GridView-class.html)

3. [ListView](https://api.flutter.dev/flutter/widgets/ListView-class.html)
4. [Stack](https://api.flutter.dev/flutter/widgets/Stack-class.html)
5. [Flex](https://api.flutter.dev/flutter/widgets/Flex-class.html) + [Expanded](https://api.flutter.dev/flutter/widgets/Expanded-class.html) 实现弹性窗口
6. [Wrap](https://api.flutter.dev/flutter/widgets/Wrap-class.html)



**可以用来占位调节位置的组件**：

Container 直接放在两个元素之间：

```dart
Container(height: 30,),
```

Padding 将元素包裹起来：

```dart
Padding(
    padding: const EdgeInsets.all(20),
    child: ListTile(
      title: Text("${list[index]}"),
    ),
)
```

SizedBox 放在两个元素之间

```dart
const SizedBox(height: 10),
```



### 两种窗口

flutter 中有 `StatelessWidget` 和 `StatefulWidget`，顾名思义，`StatelessWidget` 是一个不需要状态更改的 widget（没有要管理的内部状态），当界面部分不依赖于对象本身中的配置信息以及 widget 的`BuildContext` 时，可以使用 `StatelessWidget`。`StatefulWidget` 是可变状态的 widget。 使用`setState`方法管理 `StatefulWidget` 的状态的改变。调用`setState`告诉 Flutter 框架，某个状态发生了变化，Flutter 会重新运行 build 方法，以便应用程序可以应用最新状态。



如果用户与 widget 交互，widget 会发生变化，那么它就是 **有状态的**。



```dart
// StatelessWidget
import 'package:flutter/material.dart';

class MyStatelessWidget extends StatelessWidget {

  MyStatelessWidget({Key key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Center(
      child: Text(
        "hello",
        textDirection: TextDirection.ltr,
      ),
    );
  }
}

// StatefulWidget
class MyStatefulWidget extends StatefulWidget {
  MyStatefulWidget({super.key});
  @override
  _MyStatefulWidgetState createState() => _MyStatefulWidgetState();
}

class _MyStatefulWidgetState extends State<MyStatefulWidget> {
  @override
  Widget build(BuildContext context) {
    return Center(
      child: Text(
        "hello",
        textDirection: TextDirection.ltr,
      ),
    );
  }
```



### 控件的组合

在 flutter 中，如果希望在一个界面放置多个控件，需要使用 `Row`、`Column` 等包装起来：

```dart
return Scaffold(
      body: Center(
        child: Column(
          children: [
            const Spacer(),
            ElevatedButton(
              style: ButtonStyle(
                textStyle: MaterialStateProperty.all(const TextStyle(fontSize: 24))
              ),
              onPressed: (){
                Navigator.of(context).push(_createRoute());
              },
              child: const Text("A"),
            ),
            const Spacer(),
            ElevatedButton(
              style: ButtonStyle(
                textStyle: MaterialStateProperty.all(const TextStyle(fontSize: 24))
              ),
              onPressed: (){
                Navigator.of(context).push(MaterialPageRoute(builder: (context) => PhysicsCardDrag()));
              }, 
              child: const Text("B")
            ),
            const Spacer()
          ]
        ) 
      )
    );
```

> 使用 `const spacer()` 可以自动排列控件。



### AppBar

如果需要界面上面存在返回键，可以加上 `appBar: AppBar(),`

```dart
class Page extends StatelessWidget{
  const Page({super.key});
  @override
  Widget build(BuildContext context){
    return Scaffold(
      appBar: AppBar(
      	title: const Text("AppBar"),
      ),
      body: const Center(
        child: Text("Page"),
      ),
    );
  }
}
```



### Drawer 左侧菜单

> 注意当 AppBar 和 Drawer 同时存在时，屏幕不会出现返回键。

可以先定义左侧菜单类 MyDrawer：

```dart
class MyDrawer extends StatelessWidget {
  const MyDrawer({super.key});

  @override
  Widget build(BuildContext context) {
    return Drawer(
      elevation: 16.0,
      child: ListView
      (children: <Widget>[
          UserAccountsDrawerHeader(
            accountName: Text(User.username),
            accountEmail: Text(User.email),
            currentAccountPicture: const CircleAvatar(
              backgroundImage: AssetImage("assets/images/userIcon.jpg"),
            ),
            decoration: const BoxDecoration(
              image: DecorationImage(
                  image: AssetImage("assets/images/userBg.jpg"),
                  fit: BoxFit.cover),
            ),
          ),
          const ListTile(
            leading: Icon(Icons.settings),
          ),
          const Divider(),
          const ListTile(
            leading: Icon(Icons.language),
          ),
        ],
      ),
    );
  }
}
```

在 main.dart 中的 _MyHomePageState 的 Scaffold 类的 drawer 属性中设置：

```dart
class _MyHomePageState extends State<MyHomePage> {
  @override
  Widget build(BuildContext context) {
    return const Scaffold(
      body: Body(),
      drawer: MyDrawer(),
    );
  }
}
```

设置之后可以通过下面的命令弹出左侧窗口（关闭左侧窗口是默认操作）：

```dart
Scaffold.of(context).openDrawer();
```



### TabBar 选项卡

选项卡 TabBar，放在 AppBar 中，在非 MaterialApp 的环境下不会影响返回键的显示

```dart
Widget build(BuildContext context) {
    return MaterialApp(
      home: DefaultTabController(
        length: 3,
        child: Scaffold(
          appBar: AppBar(
            bottom: const TabBar(tabs: [
              Tab(icon: Icon(Icons.directions_car)),
              Tab(icon: Icon(Icons.directions_train)),
              Tab(icon: Icon(Icons.directions_bike)),
            ]),
            title: const Text("Tabs"),
          ),
          body: const TabBarView(children: [
            Icon(Icons.directions_car),
            Icon(Icons.directions_train),
            Icon(Icons.directions_bike)
          ]),
        ),
      ),
    );
  }
```



### Container 容器

```dart
Container(
  height: 200,
  width: 200,
  decoration: const BoxDecoration(
    color: Color.fromARGB(255, 11, 158, 158)
  ),
  alignment: Alignment.center,
  child: const Text(
    "Hello World",
    style: TextStyle(fontSize: 20),
  ),
)
```

double.infinity 和double.maxFinite可以让当前元素的width或者height达到父元素的尺寸



### 动态列表

使用 for 实现动态列表

```dart
class DynamicList extends StatelessWidget{
  const DynamicList({super.key});

  List<Widget> _initListView(){
    List<Widget> list = [];
    for (int i = 0; i < 10; i++) {
      list.add(Text("列表：$i"));
    }
    return list;
  }
  @override
  Widget build(BuildContext context){
    return ListView(
      children: _initListView(),
    );
  }
}
```

使用 ListView.builder 实现动态列表（实例化该页面时不能使用 const 修饰）

```dart
class DynamicList extends StatelessWidget {
  List list = [];
  DynamicList({Key? key}) : super(key: key) {
    for (var i = 0; i < 10; i++) {
      list.add("我是一个列表--$i");
    }
  }
  @override
  Widget build(BuildContext context) {
    return Material(child:  ListView.builder(
        itemCount: list.length,
        itemBuilder: (context, index) {
          return ListTile(
            title: Text("${list[index]}"),
          );
        })) ;
  }
}
```

动态列表往往容易溢出高度，可以使用 Flexible 组件包裹：

```dart
Flexible(
    child: ListView.builder(
        controller: _controller,
        itemCount: items.length,
        itemBuilder: (context, index) {
            return ListTile(
            	title: Text(items[index]),
            );
        },
    ),
),
```





### BottomNavigationBar 底部导航

```dart
import 'package:flutter/material.dart';

class BottomNavigation extends StatelessWidget {
  const BottomNavigation({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: "Navigation",
      theme: ThemeData(primarySwatch: Colors.amber),
      home: const Tabs()
    );
  }
}

class Tabs extends StatefulWidget {
  const Tabs({super.key});
  State<Tabs> createState() => _TabsState();
}

class _TabsState extends State<Tabs>{
  int _currentIndex = 0;
  @override
  Widget build(BuildContext context){
    return Scaffold(
        appBar: AppBar(
          title: const Text("App"),
        ),
        body: const Center(
          child: Text("body"),
        ),
        // 底部导航
        bottomNavigationBar: BottomNavigationBar(
          currentIndex: _currentIndex,
          onTap: (value){
            setState(() {
              _currentIndex = value;
            });
          },
          items: const [
            BottomNavigationBarItem(icon: Icon(Icons.home), label: "首页"),
            BottomNavigationBarItem(icon: Icon(Icons.category), label: "分类"),
            BottomNavigationBarItem(icon: Icon(Icons.settings), label: "设置")
          ],
        ),
      );
  }
}
```



### Toast

使用 fluttertoast 插件，显示 toast 的代码：

```dart
Fluttertoast.showToast(
    msg: "Detail",
    toastLength: Toast.LENGTH_SHORT,
    gravity: ToastGravity.CENTER,
    timeInSecForIosWeb: 1,
    backgroundColor: Colors.red,
    textColor: Colors.white,
    fontSize: 16.0
);
```



### 弹出列表菜单 PopupMenuButton

```dart
class Mymenu extends StatelessWidget {
  const Mymenu({super.key});

  List<PopupMenuEntry<String>> _getItemBuilder() {
    return <PopupMenuEntry<String>>[
      const PopupMenuItem<String>(
          child: ListTile(
        leading: Icon(Icons.share),
        title: Text("分享"),
      )),
      const PopupMenuDivider(),
      const PopupMenuItem<String>(
          child: ListTile(
        leading: Icon(Icons.update),
        title: Text("更新"),
      ))
    ];
  }

  @override
  Widget build(BuildContext context) {
    return PopupMenuButton(
      itemBuilder: (BuildContext context) {
        return _getItemBuilder();
      },
      icon: const Icon(Icons.menu),
      onSelected: (value) {
        print(value);
      },
      onCanceled: () {},
      offset: const Offset(100, 50),
    );
  }
}
```



### floatingActionButton 悬浮按钮

一般在 Scaffold 类中使用，可以实现一键回到顶端的功能。

```dart
class BodyState extends State<Body> {
  // 设置控件控制按钮的显示
  final ScrollController _controller = ScrollController(keepScrollOffset: false);
  bool shown = false;

  @override
  void initState() {
    super.initState();
    _controller.addListener(isScroll);
  }
  @override
  void dispose() {
    super.dispose();
    _controller.removeListener(isScroll);
  }
  
  void isScroll() {
    final bool toShow = (_controller.offset ?? 0) > MediaQuery.of(context).size.height / 2;
    shown = toShow ? true : false;
    setState(() {});
  }
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Column(
        ...
      ),
       floatingActionButton: !shown ? null : FloatingActionButton(
        onPressed: () {
          _controller.animateTo(0,
              duration: const Duration(milliseconds: 400),
              curve: Curves.easeIn);
        },
        tooltip: "一键回到顶端",
        child: const Icon(Icons.arrow_upward),
      ),
    );
  }
}
```





## 动画

### 循环播放

[Flutter Animation动画开发之——repeat循环播放_flutter 循环动画-CSDN博客](https://blog.csdn.net/mqdxiaoxiao/article/details/102933512)

循环播放一个圆从小到大，同时改变颜色。

```dart
import 'package:flutter/material.dart';

class RepeatAnimationWidget extends StatelessWidget {
  const RepeatAnimationWidget({super.key});
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Flutter Demo',
      home: const RepeatAnimation(),
    );
  }
}
class RepeatAnimation extends StatefulWidget {
  const RepeatAnimation({super.key});
  @override
  State<RepeatAnimation> createState() => _RepeatAnimation();
}
class _RepeatAnimation extends State<RepeatAnimation> with SingleTickerProviderStateMixin {
  late Animation<double> animation;   // 宽和高的动画
  late Animation<Color?> animationC;  // 颜色的动画
  late AnimationController controller;
  String text = "停止";
  @override
  initState() {
    super.initState();
    // Controller设置动画时长
    // vsync设置一个TickerProvider，当前State 混合了SingleTickerProviderStateMixin就是一个TickerProvider
    controller = AnimationController(
        duration: const Duration(seconds: 2),
        vsync: this );
    // Tween设置动画的区间值，animate()方法传入一个Animation，AnimationController继承Animation
    animation = Tween(begin: 100.0, end: 200.0).animate(controller);
    animationC = ColorTween(begin: Colors.blueAccent, end: Colors.amber).animate(controller);
    controller.repeat();   // 循环播放
//    controller.repeat(reverse: true);  // 循环往返播放
  }
  @override
  Widget build(BuildContext context) {
    return AnimatedBuilder(
        animation: Listenable.merge([animation, animationC]),  // 合并两个动画
        builder: (BuildContext ctx, Widget? child) {
          return Center(
            child: Container(
              alignment: Alignment.center,
              width: animation.value,
              height: animation.value,
              decoration: BoxDecoration(
                color: animationC.value,
                borderRadius: BorderRadius.circular(animation.value)
              ),
              child: FloatingActionButton(
                  onPressed: (){
                    if (controller.isAnimating) {
                      controller.stop();
                      setState(() { text = "开始"; });
                    }else{
                      controller.repeat();
                      setState(() { text = "停止";  });
                    }      
                  },
                  child: Text(text)
              ),
            ),
          );
        }
    );
  }
  @override
  void dispose() {
    // 释放资源
    controller.dispose();
    super.dispose();
  }
}
```



## 跳转

### 窗口跳转

如果希望跳转至另外一个窗口（PhysicsCardDrag），可以使用下面的方式

```dart
onPressed: () {
            Navigator.of(context).push(
                MaterialPageRoute(builder: (context) => const Page()));
          },
```

如果希望返回上一个页面，使用下面的方式：

```dart
onPressed: () {
            Navigator.of(context).pop(context);
          },
```

当存在许多页面进行跳转时，可以使用单独的路由文件进行跳转，首先创建一个 `routes.dart`：

```dart
final Map<String, Function> routes = {
  "/": (context,) => const MyHomePage(title: "Flutter Demo"),
  "/drawer": (context, {arguments}) => drawerWidget(title: arguments['title']),
  "/todo": (context) => const todosScreen(),
  "/Bottom": (context) => const BottomNavigation(),
  "/decorate": (context) => const DecorateText(),
  "/list": (context) => DynamicList(),
  "/physics": (context) => const PhysicsCardDrag(),
  "/snack": (context) => const snackBarWidget(),
  "/tab": (context) => const tabBarWidget()
};

var onGenerateRoute = (RouteSettings settings) {
  final String? name = settings.name;
  final Function? pageContentBuilder = routes[name];
  if (pageContentBuilder != null) {
    if (settings.arguments != null) {
      final Route route = MaterialPageRoute(
          builder: (context) =>
              pageContentBuilder(context, arguments: settings.arguments));
      return route;
    } else {
      final Route route =
          MaterialPageRoute(builder: (context) => pageContentBuilder(context));
      return route;
    }
  }
  return null;
};
```

然后在 `main.dart` 中，修改为

```dart
class MyApp extends StatelessWidget {
  const MyApp({super.key});

  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'App1',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(
            seedColor: const Color.fromRGBO(0, 107, 123, 1)),
        useMaterial3: true,
      ),
      initialRoute: "/",
      onGenerateRoute: onGenerateRoute,
    );
  }
}
```

跳转至某个页面：

```dart
Navigator.pushNamed(context, "/drawer", arguments: {
"title": "hello"
}); // 带参数
Navigator.pushNamed(context, "/snack");  // 不带参数
```

替换路由

```dart
Navigator.of(context).pushReplacementNamed('/registerSecond');
```

返回到根路由

```dart
Navigator.of(context).pushAndRemoveUntil(
    MaterialPageRoute(builder: (BuildContext context) {
    	return const HomePage();
    }), (route) => false);
```



### flutter 中的 key

许多组建的构造函数中都会有key

```dart
const tabBarWidget({super.key});
```

key 的作用是在 Widget tree 中保存状态。对于 `StatelessWidget` 来说，一般不需要指定 key。对于 `StatefulWidget` 来说，当我们想要改变组件时（进行添加、删除、重排序等操作），有时可能没有反应，这时便需要指定 key 了。

```dart
class _ScreenState extends State<Screen> {
  List<Widget> widgets = [
    StatefulContainer(key: UniqueKey(),),
    StatefulContainer(key: UniqueKey(),),
  ];
//  ···
```

详见 [Flutter | 深入浅出Key - 掘金 (juejin.cn)](https://juejin.cn/post/6844903811870359559)





### 传递数据到新页面

创建一个待办事项列表，当某个事项被点击的时候，会跳转到新的一屏，在新的一屏显示待办事项的详细信息。

> 数据的传递依靠导航窗口时传递参数

```dart
// todosScreen.dart
import 'package:flutter/material.dart';
import 'package:new01/compoents/todo/detailScreen.dart';

class Todo {
  final String title;
  final String description;

  const Todo(this.title, this.description);
}

class todosScreen extends StatelessWidget {
  const todosScreen({super.key});

  static List<Todo> todos = List.generate(
      20,
      (i) => Todo(
          "Todo $i", "A description of what needs to be done for Todo $i"));

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text("todos"),
      ),
      body: ListView.builder(
          itemCount: todos.length,
          itemBuilder: (context, index) {
            return ListTile(
              title: Text(todos[index].title),
              onTap: () {
                Navigator.of(context).push(MaterialPageRoute(
                    builder: (context) => detailScreen(todo: todos[index])));
              },
            );
          }),
    );
  }
}
```



```dart
// detailScreen.dart
import 'package:flutter/material.dart';
import 'package:new01/compoents/todo/todosScreen.dart';

class detailScreen extends StatelessWidget {
  const detailScreen({super.key, required this.todo});
  final Todo todo;
  
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(todo.title),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: Text(todo.description),
      ),
    );
  }
}
```

另外一种传递方式：[传递数据到新页面 - Flutter 中文文档 - Flutter 中文开发者网站 - Flutter](https://flutter.cn/docs/cookbook/navigation/passing-data#alternatively-pass-the-arguments-using-routesettings)



### 页面回传数据

通过 `Navigator.pop()` 实现

```dart
import 'package:flutter/material.dart';
...
class _SelectionButtonState extends State<SelectionButton> {
  // 异步
  Future<void> _navigateAndDisplaySelection(BuildContext context) async {
    // 通过 Navigator.pop 回传数据
    final result = await Navigator.push(
      context,
      MaterialPageRoute(builder: (context) => const SelectionScreen()),
    );

    // 当从StatefulWidget中使用BuildContext时，挂载的属性必须在异步间隙后检查。
    if (!context.mounted) return;

    // 在返回结果之后，隐藏组件并显示新结果。
    ScaffoldMessenger.of(context)
      ..removeCurrentSnackBar()
      ..showSnackBar(SnackBar(content: Text('$result')));
  }
}

class SelectionScreen extends StatelessWidget {
...
      child: ElevatedButton(
        onPressed: () {
          // Close the screen and return "Yep!" as the result.
          Navigator.pop(context, 'Yep!');
        },
        child: const Text('Yep!'),
      ),
...
      child: ElevatedButton(
        onPressed: () {
          // Close the screen and return "Nope." as the result.
          Navigator.pop(context, 'Nope.');
        },
        child: const Text('Nope.'),
      ),
...
```



## 操作

### 添加语音助手

#### 语音合成

使用 flutter_tts 包，[flutter_tts | Flutter package (pub.dev)](https://pub.dev/packages/flutter_tts)

这个包会调用 Android 本地库，所以需要申请对应的权限：

```xml
<queries>
  <intent>
    <action android:name="android.intent.action.TTS_SERVICE" />
  </intent>
</queries>
```

官方给出最小的 SdkVersion 为 21，需要修改 android\app\build.gradle 中的 defaultConfig：

```json
defaultConfig {
        applicationId "com.example.new03"
        // minSdkVersion flutter.minSdkVersion
        minSdkVersion 21 
        targetSdkVersion flutter.targetSdkVersion
        versionCode flutterVersionCode.toInteger()
        versionName flutterVersionName
    }
```

官方文档给出的关于 flutter_tts 的配置说明存在一些问题，如果写成

```yaml
dependencies:
    flutter:
      sdk: flutter
    flutter_tts:
```

会报错，可能是因为 flutter_tts 对应的 dart 版本不对。如果报错

```txt
[!] Your project requires a newer version of the Kotlin Gradle plugin. │ │ Find the latest version on https://kotlinlang.org/docs/releases.html#release-details, then │ │ update D:\work\app\flutterSample\new03\android\build.gradle: │ │ ext.kotlin_version = '<latest-version>'
```

可以降低版本：

```yaml
dependencies:
  flutter:
    sdk: flutter
  flutter_tts: ^3.8.5
```

基本用法：

```dart
FlutterTts flutterTts = FlutterTts();
await flutterTts.speak("中午好，今天天气真不错");
```



#### 语音识别

使用 speech_to_text 包，

具体使用参见文档：[speech_to_text - Dart API docs (pub.dev)](https://pub.dev/documentation/speech_to_text/latest/)

相较于语音合成，支持语音识别的浏览器明显较少["Web Speech API" | Can I use... Support tables for HTML5, CSS3, etc](https://caniuse.com/?search=Web Speech API)

speech_to_text 要求最小的 SdkVersion 为 21，需要修改 android\app\build.gradle 中的 defaultConfig：

```json
defaultConfig {
        applicationId "com.example.new03"
        // minSdkVersion flutter.minSdkVersion
        minSdkVersion 21 
        targetSdkVersion flutter.targetSdkVersion
        versionCode flutterVersionCode.toInteger()
        versionName flutterVersionName
    }
```



### flutter 解析 json

使用 http 包获取请求，使用 convert 转换为 json：

```dart
List pokemon = List.empty();

@override
void initState(){
	super.initState();
	fetchData();
}
Future<void> fetchData() async {
    final response = await http.get(Uri.parse('https://raw.githubusercontent.com/Biuni/PokemonGO-Pokedex/master/pokedex.json'));
    if (response.statusCode == 200) {
      Map<String, dynamic> jsonData = json.decode(response.body);
      setState(() {
        pokemon = jsonData['pokemon'];
      });
    } else {
      print("error");
    }
}
```

将其转换为列表展示，下面是列表项的初始化：

```dart
List<Widget> _initView(){
    List<Widget> list = [];
    for (var poke in pokemon) {
      list.add(Text("pokemon: ${poke['name']}"));
    }
    return list;
}
```



### 一键切换主题

[Flutter主题切换——让你的APP也能一键换肤 - 掘金 (juejin.cn)](https://juejin.cn/post/6844904137021194253)

使用 provider 和 flustars_flutter3 两个库。

首先确定想要切换的主题

```dart
Map<String, Color> themeColorMap = {
  'gray': Colors.grey,
  'blue': Colors.blue,
  'blueAccent': Colors.blueAccent,
  'cyan': Colors.cyan,
  'deepPurple': Colors.purple,
  'deepPurpleAccent': Colors.deepPurpleAccent,
  'deepOrange': Colors.orange,
  'green': Colors.green,
  'indigo': Colors.indigo,
  'indigoAccent': Colors.indigoAccent,
  'orange': Colors.orange,
  'purple': Colors.purple,
  'pink': Colors.pink,
  'red': Colors.red,
  'teal': Colors.teal,
  'black': Colors.black,
};
```

使用 Provider 进行全局状态管理

```dart
class AppInfoProvider with ChangeNotifier {
  String _themeColor = "";
  String get themeColor => _themeColor;

  setTheme(String themeColor){
    _themeColor = themeColor;
    notifyListeners();
  }
}
```

在 main.dart 配置创建的 provider，有多个状态管理就使用 MultiProvider，单个的使用 Provider.value：

```dart
class MyApp extends StatelessWidget {
  Color _themeColor = Colors.grey;
  MyApp({super.key});
  
  @override
  Widget build(BuildContext context) {
    return MultiProvider(
      providers: [ChangeNotifierProvider.value(value: AppInfoProvider())],
      child: Consumer<AppInfoProvider>(
        builder: (context, appInfo, child) {
          String colorKey = appInfo.themeColor;

          if (themeColorMap[colorKey] != null) {
            _themeColor = themeColorMap[colorKey]!;
          }
          return MaterialApp(
            title: 'Flutter Demo',
            // 重要的是对 ThemeData 的设置
            theme: ThemeData(
              primaryColor: _themeColor,
              floatingActionButtonTheme:
                  FloatingActionButtonThemeData(backgroundColor: _themeColor),
            ),
            home: const MyHomePage(title: 'Flutter Demo Home Page'),
          );
        },
      ),
    );
  }
}
```

如果需要改变主题，只需执行下面这行代码：

```dart
Provider.of<AppInfoProvider>(context, listen: false).setTheme(colorey);
```

关于 ThemeData 的设置：[ThemeData class - material library - Dart API (flutter.dev)](https://api.flutter.dev/flutter/material/ThemeData-class.html)

如果需要持久化选择的主题，需要使用 flustars_flutter3 中的 SpUtil，一般会在页面初始化加载的时候读取保存的颜色信息，所以我们需要在初始化页面配置如下代码：

```dart
String _colorKey;

@override
void initState() {
  super.initState();
  _initAsync();
}

Future<void> _initAsync() async {
  await SpUtil.getInstance();
  _colorKey = SpUtil.getString('key_theme_color', defValue: 'blue');
  // 设置初始化主题颜色
  Provider.of<AppInfoProvider>(context, listen: false).setTheme(_colorKey);
}
```

选择的代码为

```dart
setState(() {
  _colorKey = key;
});
SpHelper.putString('key_theme_color', key);
Provider.of<AppInfoProvider>(context).setTheme(key);
```



### 明暗切换

明暗切换的思路与主题切换的思路相同。

创建一个全局状态管理：

```dart
class DarkModeProvider with ChangeNotifier {
  int _darkMode = 2;
  int get darkMode => _darkMode;
  void changeMode(int darkMode) async{
    _darkMode = darkMode;
    notifyListeners();
    SpUtil.putInt("dark_mode", darkMode);
  }
}
```

在 mian.dart 中进行配置

| mode | 状态     |
| ---- | -------- |
| 0    | 明亮主题 |
| 1    | 暗黑主题 |
| 2    | 跟随系统 |

```dart
@override
  Widget build(BuildContext context) {
    return MultiProvider(
      providers: [
        ChangeNotifierProvider.value(value: DarkModeProvider())
        ],
      child: Consumer<DarkModeProvider>(
        builder: (context, appInfo, child) {
          return appInfo.darkMode == 2 ? MaterialApp(
            title: "Flutter Demo",
            theme: ThemeData(
              primarySwatch: Colors.blue,
            ),
            darkTheme: ThemeData.dark(),
            home: const MyHomePage(title: 'Flutter Demo Home Page'),
          ) : MaterialApp(
            title: "Flutter Demo",
            theme: appInfo.darkMode == 1 ? ThemeData.dark() :ThemeData(
              primarySwatch: Colors.blue
            ),
            home: const MyHomePage(title: 'Flutter Demo Home Page'),
          );
        },
      ),
    );
  }
```

想要配置主题时：

```dart
Provider.of<DarkModeProvider>(context, listen: false).changeMode(0); // 改为明亮主题
```

一个 UI 组件：

```dart
class lightDarkState extends State<lightDark> {
  final List<bool> _selectedMode = <bool>[false, false, true];
  @override
  Widget build(BuildContext context) {
    return ExpansionTile(
      leading: const Icon(Icons.contrast),
      title: const Text("明暗模式"),
      children: [
        ToggleButtons(
          onPressed: (int index) {
            setState(() {
              for (int i = 0; i < _selectedMode.length; i++) {
                _selectedMode[i] = i == index;
              }
            });
            Provider.of<DarkModeProvider>(context, listen: false).changeMode(index);
          },
          isSelected: _selectedMode,
          borderRadius: const BorderRadius.all(Radius.circular(8)),
          children: const [
            Icon(Icons.light_mode), Icon(Icons.dark_mode), Icon(Icons.sync_sharp)
          ],
        )
      ],
    );
  }
}
```


### 为某个组件添加交互事件

某些组件本身并没有交互事件，如 Text 本身并没有点击事件，可以使用 GestureDetector 进行添加：

```dart
GestureDetector(
  onTap: () => Navigator.pushNamed(context, SignUpScreen.routeName),
  child: Text(
    "注册",
    style: TextStyle(
        fontSize: getProportionateScreenWidth(16),
        color: kPrimaryColor),
  ),
),
```

### 日志操作

使用 logger 和 path_provider（提供日志文件保存的路径）

创建一个方法获取 logger

```dart
import 'package:logger/logger.dart';
import 'dart:io';
import 'package:path_provider/path_provider.dart';

Future<Logger> getLogger() async {
  final Directory appDocDir = await getApplicationDocumentsDirectory();
  String appDocPath = appDocDir.path;
  String logPath = "$appDocPath/app.log";
  Logger logger = Logger(
    output: MultiOutput(
      [ConsoleOutput(), FileOutput(file: File(logPath))]
    )
  );
  return logger;
}
```

在调用 logger 的时候需要初始化：

```dart
Logger logger = Logger();

// 注意 initState 不能带 async
@override
void initState() {
    super.initState();
    initLogger();
}
void initLogger() async{
	logger = await getLogger();
}

logger.t("Trace");
logger.d("Debug");
logger.i("Info");
logger.w("Warning");
logger.e("Error", error: 'Test Error');
logger.f("fatal", error: error, stackTrace: stackTrace);
```



读取日志文件：

```dart
final Directory appDocDir = await getApplicationDocumentsDirectory();
String appDocPath = appDocDir.path;
String logPath = "$appDocPath/app.log";
File file = File(logPath);
final contents = await file.readAsString();
print(contents);
```



## 报错

> Invalid constant value.dart(invalid_constant)

可能是组件前面加上了 const 前缀



> No Material widget found. ListTile widgets require a Material widqet ancestor wtthin the closest LookupBoundary. In Material Design, most wdgets are conceptualy "printed" on a sheet of material. In Flutters material library, that material is represe nted by the Material widget it is the Materal widget that renders ink splashes,forinstance.Because of this,many material lbrary wldgets requt e that there be a Material widget in the tree above them.

使用的组件没有被 Material 组件（Material、Scaffold等）包裹。



> RenderFlex children have non-zero flex but incoming height constraints are unbounded.

给 Flex 组件外侧套一层 Container 并设定高度



> Vertical viewport was given unbounded height.

可能是因为使用 ListView 出现的问题，需要在 ListView 中加入 shrinkWrap:true

```dart
ListView(
    shrinkWrap: true,
    children: _initView(),
)
```







