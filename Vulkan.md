
[Khronos Vulkan® 教程 :: Vulkan 文档项目](https://docs.vulkan.net.cn/tutorial/latest/00_Introduction.html)

## 开发环境

1. 下载 Vulkan SDK
2. 下载 GLFW [Download | GLFW](https://www.glfw.org/download.html)，该库可以创建支持Windows、Linux和MacOS的窗口
3. 下载GLM [Releases · brackeen/glfm](https://github.com/brackeen/glfm/releases)，该库是一个线性代数运算库

编译器选择Visual Studio，启动 Visual Studio 创建一个控制台应用程序，并且添加 `main.cpp`

设置头文件和链接路径，首先是 C/C++  -> General -> Additional Include Directories，添加Vulkan、GLFW和GLM的头文件目录
```
E:\glm_glfw\glm
E:\glm_glfw\glfw-3.4.bin.WIN64\include
E:\VulkanSDK\Include\vk_video
E:\VulkanSDK\Include
```

在 Linker -> General -> Additional Library Directories，添加链接目录

```
E:\glm_glfw\glfw-3.4.bin.WIN64\lib-vc2022
E:\VulkanSDK\Lib
```

然后在 Linker -> Input -> Additional Dependencies，添加需要用到的链接

```
vulkan-1.lib
glfw3.lib
```

最后可能需要将编译器更改为支持C++ 17功能，具体为在 C/C++ -> Language -> C++ Language Standard 中更改

创建一个窗口的代码如下

```c++
#define GLFW_INCLUDE_VULKAN
#include <GLFW/glfw3.h>

#define GLM_FORCE_DEPTH_ZERO_TO_ONE
#include <vec4.hpp>
#include <mat4x4.hpp>

#include <iostream>
#include <vulkan/vulkan.h>

int main() {
    glfwInit();

    glfwWindowHint(GLFW_CLIENT_API, GLFW_NO_API);
    GLFWwindow* window = glfwCreateWindow(800, 600, "Vulkan window", nullptr, nullptr);

    uint32_t extensionCount = 0;
    vkEnumerateInstanceExtensionProperties(nullptr, &extensionCount, nullptr);

    std::cout << extensionCount << " extensions supported\n";

    glm::mat4 matrix;
    glm::vec4 vec;
    auto test = matrix * vec;

    while (!glfwWindowShouldClose(window)) {
        glfwPollEvents();
    }

    glfwDestroyWindow(window);

    glfwTerminate();

    return 0;
}
```


## 绘制三角形

### 设置

为了能够渲染三角形，需要引入 `<vulkan/vulkan.h>`，为了能够显示窗口需要引入 `GLFW/glfw3.h`

首先初始化窗口（`initWindow`），`initWindow` 函数的代码如下

```c++
GLFWwindow* window;

void initWindow() {
	glfwInit();   // 初始化 GLFW 库
	// GLFW 最初设计用于创建 OpenGL 上下文，所以我们需要告诉它不要使用后续调用来创建 OpenGL 上下文
	glfwWindowHint(GLFW_CLIENT_API, GLFW_NO_API); 
	glfwWindowHint(GLFW_RESIZABLE, GLFW_FALSE);  // 设置窗口
	window = glfwCreateWindow(800, 600, "hello triangle", nullptr, nullptr);  // 创建窗口
} 
```

窗口需要不断运行 `mainLoop`

```c++
void mainLoop() {
	// 持续运行窗口，直到用户关闭窗口
	while (!glfwWindowShouldClose(window)) {
		glfwPollEvents();
	}
}
```

销毁窗口 `cleanup`

```c++
void cleanup() {
	// 销毁窗口，清理资源
	glfwDestroyWindow(window);
	glfwTerminate();
}
```


此时的代码如 [code](codes/vulkan/00_base_code.cpp) 
