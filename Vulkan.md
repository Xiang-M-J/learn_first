
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


#### 基础代码


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


代码见 [00_base_code.cpp](codes/vulkan/00_base_code.cpp)


#### 实例

创建实例（`createInstance`）来初始化Vulkan库，实例是应用程序和Vulkan库之间的连接

```c++
VkInstance instance;
void createInstance() {
	VkApplicationInfo appInfo{};  // 创建结构体传递信息
	appInfo.sType = VK_STRUCTURE_TYPE_APPLICATION_INFO;
	appInfo.pApplicationName = "Hello Triangle";
	appInfo.applicationVersion = VK_MAKE_VERSION(1, 0, 0);
	appInfo.pEngineName = "No Engine";
	appInfo.engineVersion = VK_MAKE_VERSION(1, 0, 0);
	appInfo.apiVersion = VK_API_VERSION_1_0;

	VkInstanceCreateInfo createInfo{};  // 告诉 Vulkan 驱动程序我们想要使用哪些全局扩展和验证层
	createInfo.sType = VK_STRUCTURE_TYPE_INSTANCE_CREATE_INFO;
	createInfo.pApplicationInfo = &appInfo;
	uint32_t glfwExtensionCount = 0;
	const char** glfwExtensions;

	glfwExtensions = glfwGetRequiredInstanceExtensions(&glfwExtensionCount);

	createInfo.enabledExtensionCount = glfwExtensionCount;
	createInfo.ppEnabledExtensionNames = glfwExtensions;
	createInfo.enabledLayerCount = 0;

	// 可以开始创建实例
	// 参数为 指向包含创建信息的结构体指针 &createInfo
	// 指向自定义分配器回调的指针，nullptr
	// 指向存储新对象句柄的变量指针，&instance
	if (vkCreateInstance(&createInfo, nullptr, &instance) != VK_SUCCESS) {
		throw std::runtime_error("failed to create instance!");
	}
}
```

判断某个扩展是否支持 [实例 :: Vulkan 文档项目](https://docs.vulkan.net.cn/tutorial/latest/03_Drawing_a_triangle/00_Setup/01_Instance.html#_checking_for_extension_support)

最后还需要清理实例

```c++
void cleanup() {
	vkDestroyInstance(instance, nullptr);
	// ...
}
```

代码见 [01_instance_creation.cpp](codes/vulkan/01_instance_creation.cpp)

#### 验证层

Vulkan API 的设计理念是最小化驱动程序开销，而这一目标的体现之一是默认情况下 API 中的错误检查非常有限。即使是像将枚举设置为不正确的值或将空指针传递给必需参数这样简单的错误，通常也不会显式处理，只会导致崩溃或未定义的行为。因为 Vulkan 要求您对所做的每一件事都非常明确，所以很容易犯许多小错误，例如使用新的 GPU 功能，但忘记在创建逻辑设备时请求它。

但是，这并不意味着这些检查不能添加到 API 中。Vulkan 引入了一个优雅的系统，称为_验证层_。验证层是可选组件，它们会挂接到 Vulkan 函数调用中以应用其他操作。验证层中的常见操作是

- 对照规范检查参数的值，以检测滥用
    
- 跟踪对象的创建和销毁，以查找资源泄漏
    
- 通过跟踪调用来源的线程来检查线程安全性
    
- 将每个调用及其参数记录到标准输出
    
- 跟踪 Vulkan 调用以进行分析和重放

让我们首先向程序添加两个配置变量，以指定要启用的层以及是否启用它们。我选择根据程序是否在调试模式下编译来确定该值。`NDEBUG` 宏是 C++ 标准的一部分，表示“非调试”。

```c++
#include <vector>

const std::vector<const char*> validationLayers = {
	"VK_LAYER_KHRONOS_validation"
};

#ifdef NDEBUG
const bool enableValidationLayers = false;
#else
const bool enableValidationLayers = true;
#endif
```

然后添加新函数 `checkValidationLayerSupport` 检查验证层是否可用，具体的方法是先列出所有的可用层，判断 `validationLayers` 中的所有层是否都在可用层之中。

```c++
bool checkValidationLayersSupport() {
	// 获取所有的可用层
	uint32_t layerCount;
	vkEnumerateInstanceLayerProperties(&layerCount, nullptr);

	std::vector<VkLayerProperties> availabelLayers(layerCount);
	vkEnumerateInstanceLayerProperties(&layerCount, availabelLayers.data());

	// 检查validationLayers 中的所有层是否存在于 availableLayers 列表中
	for (const char* layerName : validationLayers) {
		bool layerFound = false;

		for (const auto& layerProperties : availabelLayers) {
			if (strcmp(layerName, layerProperties.layerName))
			{
				layerFound = true;
			}
		}
		if (!layerFound) { return false; }
	}
	return true;
}
```

验证层需要在实例创建时加入，首先调用checkValidationLayersSupport函数，然后修改 `VkInstanceCreateInfo` 结构体实例化，以在启用验证层时包含验证层名称

```c++
void createInstance() {
	if (enableValidationLayers && !checkValidationLayersSupport())
	{
		throw std::runtime_error("validation layers requested, but not support");
	}
	// ...
	if (enableValidationLayers) {
		createInfo.enabledLayerCount = static_cast<uint32_t>(validationLayers.size());
		createInfo.ppEnabledLayerNames = validationLayers.data();
	}
	else {
		createInfo.enabledLayerCount = 0;
	}
	// ...
}
```

验证层默认将调试消息打印到标准输出，但也可以通过在程序中提供显式回调来处理消息。详细请见 [验证层 :: Vulkan 文档项目](https://docs.vulkan.net.cn/tutorial/latest/03_Drawing_a_triangle/00_Setup/02_Validation_layers.html#_message_callback)

代码见 [02_validation_layers.cpp](codes/vulkan/02_validation_layers.cpp)

#### 物理设备和队列族

通过 VkInstance 初始化 Vulkan 库后，我们需要查找并选择系统中支持我们所需功能的显卡。 实际上，我们可以选择任意数量的显卡并同时使用它们，但在本教程中，我们将只选择第一块满足我们需求的显卡。

添加一个函数 `pickPhysicalDevice`，用于选择显卡，先确定有哪些可用显卡，再评估每个设备，检查该设备是否可以执行操作。

```c++
bool isDeviceSuitable(VkPhysicalDevice device) {  // 可以直接返回True
	VkPhysicalDeviceProperties deviceProperties;
	VkPhysicalDeviceFeatures deviceFeatures;
	vkGetPhysicalDeviceProperties(device, &deviceProperties);
	vkGetPhysicalDeviceFeatures(device, &deviceFeatures);

	return deviceProperties.deviceType == VK_PHYSICAL_DEVICE_TYPE_DISCRETE_GPU &&
		deviceFeatures.geometryShader;
}

void pickPhysicalDevice() {
	uint32_t deviceCount = 0;
	vkEnumeratePhysicalDevices(instance, &deviceCount, nullptr);

	if (deviceCount == 0) {
		throw std::runtime_error("failed to find devices which support vulkan");
	}

	std::vector<VkPhysicalDevice> devices(deviceCount);
	vkEnumeratePhysicalDevices(instance, &deviceCount, devices.data());
	// 检查设备是否可用
	for (const auto& device : devices) {
		if (isDeviceSuitable(device))
		{
			physicalDevice = device;
			break;
		}
	}
}
```


Vulkan 中几乎每个操作，从绘制到上传纹理，都需要将命令提交到队列。有不同类型的队列来自不同的队列族，并且每个队列族只允许命令的一个子集。例如，可能有一个队列族只允许处理计算命令，或者一个只允许与内存传输相关的命令。

我们需要检查设备支持哪些队列族，以及其中哪些队列族支持我们要使用的命令。为此，我们将添加一个新函数 `findQueueFamilies` 来查找我们需要的所有队列族。

队列族可能会有很多个，因此通过一个结构体来管理所有的队列，队列族并不是必需的，所以需要区分是否包含某个队列，C++ 17引入了 optional 包装器来确定某个变量是否被赋值

```c++
#include <optional>

struct QueueFamilyIndices {
	std::optional<uint32_t> graphicsFamily;
};
```

然后就可以开始检索队列族列表

```c++
QueueFamilyIndices findQueueFamilies(VkPhysicalDevice device) {
	QueueFamilyIndices indices;

	uint32_t queueFamilyCount = 0;
	vkGetPhysicalDeviceQueueFamilyProperties(device, &queueFamilyCount, nullptr);

	std::vector<VkQueueFamilyProperties> queueFamilies(queueFamilyCount);
	vkGetPhysicalDeviceQueueFamilyProperties(device, &queueFamilyCount, queueFamilies.data());
	// VkQueueFamilyProperties 结构体包含有关队列族的一些详细信息，如支持的操作类型以及基于该族可以创建的队列数量
	// 我们需要找到至少一个支持 VK_QUEUE_GRAPHICS_BIT 的队列族。
	int index = 0;
	for (const auto& queueFamiliy : queueFamilies) {
		if (queueFamiliy.queueFlags & VK_QUEUE_GRAPHICS_BIT)
		{
			indices.graphicsFamily = index;
		}
		index++;
	}

	return indices;
}
```

这个函数可以在 `isDeviceSuitable` 中调用，作为判断一个设备是否可用的条件

```c++
bool isDeviceSuitable(VkPhysicalDevice device) {
	QueueFamilyIndices indices = findQueueFamilies(device);
	return indices.graphicsFamily.has_value();
}
```

代码见 [03_physical_device_selection.cpp](codes/vulkan/03_physical_device_selection.cpp)


#### 逻辑设备和队列

在选择要使用的物理设备后，我们需要设置一个_逻辑设备_来与它交互。逻辑设备的创建过程类似于实例的创建过程，并描述了我们想要使用的功能。我们还需要指定要创建哪些队列，现在我们已经查询了哪些队列族可用。如果您有不同的要求，甚至可以从同一个物理设备创建多个逻辑设备。

逻辑设备的创建涉及到再次在结构体中指定一堆细节，其中第一个将是 `VkDeviceQueueCreateInfo`。此结构描述了我们想要为一个队列族提供的队列数量。现在我们只对具有图形功能的队列感兴趣。

接下来要指定的信息是我们将要使用的一组设备功能。这些是我们在上一章中使用 `vkGetPhysicalDeviceFeatures` 查询支持的功能，例如几何着色器。

有了前面的两个结构，我们就可以开始填写主要的 `VkDeviceCreateInfo` 结构了。

```c++
VkDevice device;

void createLogicalDevice() {

	// 指定创建的队列
	QueueFamilyIndices indices = findQueueFamilies(physicalDevice);

	VkDeviceQueueCreateInfo queueCreateInfo{};
	queueCreateInfo.sType = VK_STRUCTURE_TYPE_DEVICE_QUEUE_CREATE_INFO;
	queueCreateInfo.queueFamilyIndex = indices.graphicsFamily.value();
	queueCreateInfo.queueCount = 1;

	// 分配优先级给队列，优先级用0.0到1.0之间的浮点数指定
	float queuePriority = 1.0f;
	queueCreateInfo.pQueuePriorities = &queuePriority;

	// 默认设备功能
	VkPhysicalDeviceFeatures deviceFeatures{};
	
	VkDeviceCreateInfo createInfo{};
	createInfo.sType = VK_STRUCTURE_TYPE_DEVICE_CREATE_INFO;
	
	// 添加队列信息和设备功能
	createInfo.pQueueCreateInfos = &queueCreateInfo;
	createInfo.queueCreateInfoCount = 1;

	createInfo.pEnabledFeatures = &deviceFeatures;

	createInfo.enabledExtensionCount = 0;   // 不需要任何特定于设备的扩展

	if (vkCreateDevice(physicalDevice, &createInfo, nullptr, &device) != VK_SUCCESS) {
		throw std::runtime_error("failed to create logical device!");
	}
}
```

逻辑设备需要在cleanup中销毁

```c++
void cleanup() {
    vkDestroyDevice(device, nullptr);
    // ...
}
```

代码见 [04_logical_device](codes/vulkan/04_logical_device.cpp)



### 呈现


#### 窗口表面

由于 Vulkan 是一个与平台无关的 API，它本身无法直接与窗口系统接口。为了建立 Vulkan 和窗口系统之间的连接，以便将结果呈现到屏幕上，需要使用 WSI（窗口系统集成）扩展，扩展有许多，当前只讨论 `VK_KHR_surface`，它公开了一个 `VkSurfaceKHR` 对象，该对象表示一种抽象类型的Surface 来呈现渲染的图像，Surface 将会放在GLFW创建的窗口上。

创建一个 surface 类成员

```c++
VkSurfaceKHR surface;
```

尽管 `VkSurfaceKHR` 对象及其使用是与平台无关的，但它的创建不是，因为它取决于窗口系统的详细信息。例如，它需要 Windows 上的 `HWND` 和 `HMODULE` 句柄。因此，该扩展有一个特定于平台的添加，在 Windows 上称为 `VK_KHR_win32_surface`，并且也自动包含在 `glfwGetRequiredInstanceExtensions` 的列表中。

[窗口表面 :: Vulkan 文档项目](https://docs.vulkan.net.cn/tutorial/latest/03_Drawing_a_triangle/01_Presentation/00_Window_surface.html#_window_surface_creation) 中演示如何使用这个特定于平台的扩展在 Windows 系统中创建表面

由于GLFW提供了 `glfwCreateWindowSurface` 处理平台差异，所以直接使用即可

```c++
void createSurface() {
	if (glfwCreateWindowSurface(instance, window, nullptr, &surface) != VK_SUCCESS)
	{
		throw std::runtime_error("failed to create window surface");
	}
}
```

同样surface需要在cleanup中销毁

```c++
void cleanup() {
	// ... 
	vkDestroySurfaceKHR(instance, surface, nullptr);
	vkDestroyInstance(instance, nullptr);
	// ...
}
```


尽管 Vulkan 实现可能支持窗口系统集成，但这并不意味着系统中的每个设备都支持它。因此，我们需要扩展 `isDeviceSuitable` 以确保设备可以将图像呈现到我们创建的表面。由于演示是特定于队列的功能，因此问题实际上是关于查找支持演示到我们创建的表面的队列族。实际上，支持绘图命令的队列族和支持演示的队列族可能不重叠。因此，我们必须考虑到可能存在不同的演示队列，方法是修改 `QueueFamilyIndices` 结构

```c++
struct QueueFamilyIndices {
	std::optional<uint32_t> graphicsFamily;
	std::optional<uint32_t> presentFamily;

	bool isComplete() {
		return graphicsFamily.has_value() && presentFamily.has_value();
	}
};
```

然后需要在 `findQueueFamilies` 函数中查找满足条件的队列
```c++
VkBool32 presentSupport = false;
vkGetPhysicalDeviceSurfaceSupportKHR(device, i, surface, &presentSupport);
if (presentSupport) { indices.presentFamily = i; }
```

下面需要修改逻辑设备创建过程，创建呈现队列并检索`VkQueue` 句柄，为该句柄添加成员变量

```c++
void createLogicalDevice() {

	// 指定创建的队列
	QueueFamilyIndices indices = findQueueFamilies(physicalDevice);

	float queuePriority = 1.0f;

	std::vector<VkDeviceQueueCreateInfo> queueCreateInfos;
	std::set<uint32_t> uniqueQueueFamilies = { indices.graphicsFamily.value(), indices.presentFamily.value() };

	float queuePriority = 1.0f;
	// 根据队列族来设置队列创建信息
	for (uint32_t queueFamily : uniqueQueueFamilies) {
		VkDeviceQueueCreateInfo queueCreateInfo{};
		queueCreateInfo.sType = VK_STRUCTURE_TYPE_DEVICE_QUEUE_CREATE_INFO;
		queueCreateInfo.queueFamilyIndex = queueFamily;
		queueCreateInfo.queueCount = 1;
		queueCreateInfo.pQueuePriorities = &queuePriority;
		queueCreateInfos.push_back(queueCreateInfo);
	}

	// 默认设备功能
	VkPhysicalDeviceFeatures deviceFeatures{};
	
	VkDeviceCreateInfo createInfo{};
	createInfo.sType = VK_STRUCTURE_TYPE_DEVICE_CREATE_INFO;
	
	// 添加队列信息和设备功能
	createInfo.pQueueCreateInfos = queueCreateInfos.data();
	createInfo.queueCreateInfoCount = static_cast<uint32_t>(queueCreateInfos.size());

	createInfo.pEnabledFeatures = &deviceFeatures;

	createInfo.enabledExtensionCount = 0;   // 不需要任何特定于设备的扩展

	if (vkCreateDevice(physicalDevice, &createInfo, nullptr, &device) != VK_SUCCESS) {
		throw std::runtime_error("failed to create logical device!");
	}
	// 添加一个调用来检索队列句柄。
	vkGetDeviceQueue(device, indices.presentFamily.value(), 0, &presentQueue);
	vkGetDeviceQueue(device, indices.graphicsFamily.value(), 0, &graphicsQueue);
}
```


代码为 [05_window_surface.cpp](codes/vulkan/05_window_surface.cpp)

#### 交换链

Vulkan 没有“默认帧缓冲”的概念，因此它需要一个基础设施来拥有我们将要渲染的缓冲，然后我们才能在屏幕上可视化它们。这个基础设施被称为交换链，必须在 Vulkan 中显式创建。交换链本质上是一个等待呈现到屏幕的图像队列。我们的应用程序将获取这样的图像来绘制它，然后将其返回到队列。队列的确切工作方式以及从队列中呈现图像的条件取决于交换链的设置方式，但交换链的总体目的是将图像的呈现与屏幕的刷新率同步。

