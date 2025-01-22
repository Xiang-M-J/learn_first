
## 布局设计

### 响应式布局

在 QT 中设计响应式布局需要设置根 Widget 的布局为垂直布局、水平布局等（先不要设置，等到基本的组件已经放完了再设置），然后使用 Layouts 控件将组件放在一起，方便调整。

大部分控件（除了 Layouts 控件）可以通过设置 sizePolicy 中的水平策略和垂直策略来修改显示效果，如水平策略为 Fixed，控件的宽度就保持为固定的尺寸，如策略设置为 Perferred，就会自动推断占据的空间。

对于 Layouts 控件，可以通过设置 LayoutSpacing 来控制各个组件之间的间隔，设置 `layoutStretch` 来控制各个组件的大小比例（默认为 `0,0,0,0`），如设置 `layoutStretch` 为 `1,2,3,4` 将四个控件的比例设置为 1:2:3:4（当控件的策略为 Fixed，不起作用）

如果需要各个组件之间保持一定的间距，可以在两个组件之间放入 Spacers 控件，可以设置Spacers 控件的尺寸为 Fixed 来保证在窗体拉伸时始终维持固定的间隔。


如果需要设置一个组件的大小，可以通过设置 maximumSize 来调整。

### 绘图控件

Qt 中似乎没有自带的绘图控件，不过可以使用继承 QWidget 类（Container 中的 Widget 控件）来实现绘图功能

```python
from PySide6.QtGui import QPainter, QPen, QColor  
from PySide6.QtWidgets import QWidget  
  
  
class WaveformWidget(QWidget):  
    def __init__(self, parent=None):  
        super().__init__(parent)  
        self.setMinimumSize(100, 100)  # 设置最小尺寸  
        self.data = []  # 默认波形数据  
  
    def set_data(self, data):  
        """设置新的波形数据"""  
        self.data = data  
        self.repaint()  # 重新绘制界面  
  
    def paintEvent(self, event):  
        """绘制波形"""  
        painter = QPainter(self)  
        painter.setRenderHint(QPainter.Antialiasing)  
  
        # 绘制背景  
        painter.fillRect(self.rect(), QColor.fromRgb(255, 255, 255))  
  
        # 设置画笔  
        pen = QPen(QColor.fromRgb(0, 125, 125))  
        painter.setPen(pen)  
  
        # 计算绘制的比例  
        width = self.width()  
        height = self.height()  
        offset = height // 2  
  
        # 绘制波形  
        for i in range(1, len(self.data)):  
            x1 = (i - 1) * (width / len(self.data))  
            y1 = offset - self.data[i - 1] / 32768 * offset  
  
            x2 = i * (width / len(self.data))  
            y2 = offset - self.data[i] / 32768 * offset  
  
            painter.drawLine(x1, y1 / 1.05 , x2, y2 / 1.05)
```






## Qt in python

python 原生支持的gui框架 tkinter 受限太多，不能处理多线程任务

QT Creator + Python

先在 QT Creator 中创建一个 QT for Python 项目，在 `form.ui` 中先设计好界面，使用

```sh
pyside6-uic form.ui -o ui_form.py
```

将界面转为 `ui_form.py`，原本项目中包括了 `widget.py`，使用 python 运行 `widget.py` 即可得到在 QT 中设计的窗口。

为了添加点击事件，可以在 `ui_form.py` 的 `setupUi` 函数 中添加connect

```python
self.open_file_btn.clicked.connect(self.open_file)
self.play_btn1.clicked.connect(partial(self.play, 0))  # 带参数
```

如果需要重复执行一个操作，在此时拖拽窗口可以会延迟或无响应，这不一定需要使用 QThread 来手动多线程，可以考虑在循环中加入 `QApplication.processEvents()`

```python
while true:
	# do something
	
	QApplication.processEvents()
```

如果需要设置窗口标题，可以在 `ui_form.py` 的 `retranslateUi` 函数为

```python
def retranslateUi(self, Widget):  
    Widget.setWindowTitle(QCoreApplication.translate("Widget", u"新标题", None))
    # ...
```


### 编译程序

使用 pyinstaller 来编译应用程序

```sh
pyinstaller --paths D:\Python39\Lib\site-packages\PyQt6\Qt6\bin -F -w widget.py
```

其中 `--paths` 指定 PyQt6 的安装位置，编译结束后会生成一个同名的 widget.spec 文件。如果需要打包其它资源文件，需要修改资源文件中的 `Analysis` 的 `datas` 参数，并重新打包

```text
a = Analysis(  
    ['widget.py'],  
    pathex=['D:\\Python39\\Lib\\site-packages\\PyQt6\\Qt6\\bin'],  
    binaries=[],  
    datas=[('D:\\work\\app1028\\cap_inp_out_py\\libspl.dll', '.'),('D:\\work\\app1028\\cap_inp_out_py\\msa_dpcrn_fast.onnx', '.')],  
    hiddenimports=[],  
    hookspath=[],  
    hooksconfig={},  
    runtime_hooks=[],  
    excludes=[],  
    noarchive=False,  
    optimize=0,  
)
```

```python
pyinstaller  widget.spec
```

一些资源文件在打包之后可能会遇到找不到的情况可以参考如下做法

```python
if getattr(sys, 'frozen', False):
	real_path = os.path.join(sys._MEIPASS, 'model.onnx')  # 部署时
else:
	real_path = "model.onnx"     # 开发时
```

