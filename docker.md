## 安装 docker

### 在 WSL2 中使用 docker

[WSL 上的 Docker 容器入门 | Microsoft Learn](https://learn.microsoft.com/zh-cn/windows/wsl/tutorials/wsl-containers#prerequisites)

[Docker Desktop WSL 2 backend on Windows | Docker Docs](https://docs.docker.com/desktop/wsl/#download)

[Windows安装使用Docker，方便你的开发和部署(DockerDesktop篇)_windows安装docker-CSDN博客](https://blog.csdn.net/qq_60750453/article/details/128636298)

#### 查看系统版本和内核版本

查看系统版本和内核版本判断是否满足要求

```sh
lsb_release -a    // 系统版本
uname -a		 // 内核版本
```

1. 安装好 WSL2 之后，安装 [Docker Desktop](https://www.docker.com/products/docker-desktop/)，默认安装到 C:\Program Files\Docker\Docker，如果想要更换路径，需要在安装器下载完成的路径下面执行命令：

    ```powershell
    start /w "" "Docker Desktop Installer.exe" install --installation-dir=D:\Docker
    ```


2. 进入设置，Docker Engine，配置镜像源。

```json
{
  "builder": {
    "gc": {
      "defaultKeepStorage": "20GB",
      "enabled": true
    }
  },
  "experimental": false,
  "registry-mirrors": [
    "https://hub-mirror.c.163.com",
    "https://registry.docker-cn.com",
    "https://mirror.ccs.tencentyun.com",
      "https://docker.nju.edu.cn/"
  ]
}
```

3. 确保在“设置”>“常规”中选中“使用基于 WSL 2 的引擎”。

<img src="https://learn.microsoft.com/zh-cn/windows/wsl/media/docker-running.png" style="zoom: 33%;" />

4. 通过转到“设置”>“资源”>“WSL 集成”，从要启用 Docker 集成的已安装 WSL 2 发行版中进行选择。

<img src="https://learn.microsoft.com/zh-cn/windows/wsl/media/docker-dashboard.png" style="zoom:33%;" />

5. 若要确认已安装 Docker，请打开 WSL 发行版（例如 Ubuntu），并通过输入 `docker --version` 来显示版本和内部版本号

```sh
xmj@DESKTOP-HFO48O5:~$ docker --version
Docker version 25.0.3, build 4debf41
```

6. 通过使用 `docker run hello-world` 运行简单的内置 Docker 镜像，测试安装是否正常工作

```sh
xmj@DESKTOP-HFO48O5:~$ docker run hello-world
Unable to find image 'hello-world:latest' locally
latest: Pulling from library/hello-world
c1ec31eb5944: Pull complete
Digest: sha256:53641cd209a4fecfc68e21a99871ce8c6920b2e7502df0a20671c6fccc73a7c6
Status: Downloaded newer image for hello-world:latest

Hello from Docker!
This message shows that your installation appears to be working correctly.

To generate this message, Docker took the following steps:
 1. The Docker client contacted the Docker daemon.
 2. The Docker daemon pulled the "hello-world" image from the Docker Hub.
    (amd64)
 3. The Docker daemon created a new container from that image which runs the
    executable that produces the output you are currently reading.
 4. The Docker daemon streamed that output to the Docker client, which sent it
    to your terminal.

To try something more ambitious, you can run an Ubuntu container with:
 $ docker run -it ubuntu bash

Share images, automate workflows, and more with a free Docker ID:
 https://hub.docker.com/

For more examples and ideas, visit:
 https://docs.docker.com/get-started/
```

### 迁移 docker-desktop-data 和 docker-desktop 

Docker Desktop 会创建两个发行版：`docker-desktop-data` 和 `docker-desktop`，默认位置在 `C:\Users\<用户名>\AppData\Local\Docker\wsl`，可以将其迁移到其它位置。

首先关闭 docker 和 WSL：

```powershell
wsl --shutdown
```

下面开始迁移，先导出

```powershell
wsl --export docker-desktop-data E:\docker\docker-desktop-data.tar
wsl --export docker-desktop E:\docker\docker-desktop.tar
```

后注销

```powershell
wsl --unregister docker-desktop-data
wsl --unregister docker-desktop
```

最后导入

```powershell
wsl --import docker-desktop-data E:\wsl\docker\docker-desktop-data E:\docker\docker-desktop-data.tar
wsl --import docker-desktop E:\wsl\docker\docker-desktop E:\docker\docker-desktop.tar
```



## Docker 基本知识

[Docker overview | Docker Docs](https://docs.docker.com/get-started/overview/)

### docker 常用命令

拉取远程镜像到本地

```sh
docker pull tensorflow/tensorflow:1.15.4-gpu-py3
```

下面的命令运行一个 ubuntu 容器，以交互方式连接到本地命令行会话，并运行 /bin/bash

```sh
docker run -i -t ubuntu /bin/bash
```

运行这段命令后，会有下面的流程：

1. 如果你在本地没有 ubuntu 镜像，Docker会从配置的仓库中提取它，就像手动运行 Docker pull ubuntu一样。
2. Docker创建一个新容器，就像手动运行 Docker container create 命令一样。
3. Docker 为容器分配一个读写文件系统，作为它的最后一层。这允许运行中的容器在其本地文件系统中创建或修改文件和目录。
4. Docker创建了一个网络接口，将容器连接到默认网络，因为没有指定任何网络选项。这包括为容器分配一个IP地址。默认情况下，容器可以使用主机的网络连接连接到外部网络。
5. Docker启动容器并执行 /bin/bash 由于容器以交互方式运行并连接到您的终端 (由于-i和-t标志)，因此您可以使用键盘提供输入，而Docker将输出记录到您的终端。
6. 当您运行 exit 命令终止 /bin/bash 命令时，容器会停止，但不会被移除。您可以重新启动或删除它。


### docker 简介

<img src="https://docs.docker.com/get-started/images/docker-architecture.webp" alt="docker-architecture" style="zoom: 50%;" />

Docker 使用 client-server 架构。Docker client 与 Docker daemon（守护进程） 通信，后者完成构建、运行和分发 Docker 容器的繁重工作。Docker client 和 daemon 可以运行在同一个系统上，或者将 Docker client 连接到远程 Docker daemon。Docker client 和 daemon 使用REST API，通过UNIX 套接字或网络接口进行通信。另一个Docker client 是Docker Compose，处理由一组容器组成的应用程序。

#### Docker daemon

Docker daemon 监听 Docker API 请求，管理 Docker 对象如镜像、容器、网络等，Docker daemon 可以和其他 daemon 通信

#### Docker client

Docker client 是许多 Docker 用户与 Docker 交互的主要方式。当使用诸如 docker run 之类的命令时，客户端将这些命令发送给 Docker Daemon（dockerd），后者执行这些命令。docker 命令使用 docker API。Docker客户端可以与多个 daemon 通信。

#### Docker Desktop

Docker Desktop 是一个易于安装的应用程序，适用于Mac、Windows或Linux环境，能够构建和共享容器化应用程序和微服务。Docker Desktop包括Docker Daemon (dockerd)、Docker 客户端(Docker)、Docker Compose、Docker Content Trust、Kubernetes 和 Credential Helper。

#### Docker registries

Docker registries 存储 Docker Images。Docker Hub 是一个任何人都可以使用的公共仓库，默认情况下Docker会在Docker Hub上查找镜像，也可以在私人仓库中查找。

#### Images

镜像是一个只读模板，带有创建 Docker 容器的说明。通常，一个镜像基于另一个镜像，并进行一些额外的定制。例如，可以构建一个基于 ubuntu 镜像的镜像，但是安装 Apache web 服务器和其它应用程序，以及使应用程序运行所需的配置细节。可以创建自己的镜像，也可以只使用其他人创建并发布在仓库中的镜像。要构建自己的镜像，需要创建一个 Dockerfile，该文件使用简单的语法来定义创建和运行镜像所需的步骤。Dockerfile 中的每条指令都会在镜像中创建一个层。当你改变Dockerfile并重建镜像时，只有那些已经改变的层才会被重建。

#### Containers

容器是镜像的可运行实例。可以使用 Docker API 或 CLI 创建、启动、停止、移动或删除容器。可以将容器连接到一个或多个网络，将存储附加到其上，甚至可以根据其当前状态创建新镜像。默认情况下，容器相对较好地与其他容器及其主机隔离。您可以控制容器的网络、存储或其他底层子系统与其他容器或主机的隔离程度。容器是由它的镜像以及在创建或启动它时提供给它的任何配置选项定义的。当容器被删除时，任何未存储在持久存储中的对其状态的更改都会消失。

容器是一个隔离环境，容器不了解操作系统或文件。运行在 Docker Desktop 提供的环境中。容器包含代码运行所需的一切，包括基本操作系统。可以使用 Docker Desktop 来管理和操作容器。


### docker guide

#### 创建容器

**在 Docker Desktop 中创建容器**


1. Open Docker Desktop and select the search.
2. Specify `docker/welcome-to-docker` in the search and then select **Run**.
3. Expand the **Optional settings**.
4. In **Container name**, specify `welcome-to-docker`.
5. In **Host port**, specify `8088`.
6. Select **Run**

上面这个例子是一个前端容器，复杂的容器可能会包括前端、后端和数据库。前端容器可以在本地访问，如上面的容器可以访问 http://localhost:8088。 

运行单个容器：[How do I run a container? | Docker Docs](https://docs.docker.com/guides/walkthroughs/run-a-container/)

运行镜像：[Run Docker Hub images | Docker Docs](https://docs.docker.com/guides/walkthroughs/run-hub-images/)

运行多容器应用：[Run multi-container applications | Docker Docs](https://docs.docker.com/guides/walkthroughs/multi-container-apps/)


#### 持续化容器数据

Docker 容器内的数据与本地文件系统相互隔离，删除一个容器后，容器内的数据全部都被删除。有时可能希望持久化容器生成的数据。为此，可以使用 volumes（卷）。

若要向项目添加 volume，编辑 `compose.yaml`，然后取消以下行的注释

```yaml
todo-database:
    # ...
    volumes:
      - database:/data/db
# ...
volumes:
  database:
```

[Persist container data | Docker Docs](https://docs.docker.com/guides/walkthroughs/persist-data/)

[Persist the DB | Docker Docs](https://docs.docker.com/get-started/05_persisting_data/)

可以使用命令行和 Docker Desktop 创建 volume

**命令行**

创建一个 volume

```sh
docker volume create todo-db
```

如果容器没有挂载 volume，停止并删除容器

```sh
docker rm -f <id>
```

启动容器，加上 --mount 选项指定 volume 挂载，将其挂载在容器的 /etc/todos

```sh
docker run -dp 127.0.0.1:3000:3000 --mount type=volume,src=todo-db,target=/etc/todos getting-started
```

**Docker Desktop**

创建 volume：

1. Select **Volumes** in Docker Desktop.
2. In **Volumes**, select **Create**.
3. Specify `todo-db` as the volume name, and then select **Create**.

停止，删除容器：

1. Select **Containers** in Docker Desktop.
2. Select **Delete** in the **Actions** column for the container.

挂载 volume 启动容器：

1. Select image and then select **Run**.
2. Select **Optional settings**.
3. In **Host port**, specify the port, for example, `3000`.
4. In **Host path**, specify the name of the volume, `todo-db`.
5. In **Container path**, specify `/etc/todos`.
6. Select **Run**.

确认 volume 的储存地址：

```sh
$ docker volume inspect todo-db
[
    {
        "CreatedAt": "2019-09-26T02:18:36Z",
        "Driver": "local",
        "Labels": {},
        "Mountpoint": "/var/lib/docker/volumes/todo-db/_data",
        "Name": "todo-db",
        "Options": {},
        "Scope": "local"
    }
]
```


#### 访问本地文件

[Access a local folder from a container | Docker Docs](https://docs.docker.com/guides/walkthroughs/access-local-folder/)

默认情况下 docker 无法访问本地文件系统，但是可以通过编辑 compose.yaml 在项目加入绑定挂载，注释下面几行

```yaml
todo-app:
    # ...
    volumes:
      - ./app:/usr/src/app
      - /usr/src/app/node_modules
```

volumes 告诉 Compose 将本地文件夹 ./app 挂载到 todo-app 服务容器中的 /usr/src/app 中。这个特定的绑定挂载覆盖容器中 /usr/src/app 目录的静态内容，并创建开发容器。第二条指令 /usr/src/app/node_modules 阻止绑定挂载覆盖容器的node_modules目录，以保留容器中安装的包。

[Use bind mounts | Docker Docs](https://docs.docker.com/get-started/06_bind_mounts/)

使用绑定挂载可以访问本机地址

```sh
docker run -it --mount type=bind,src="$(pwd)",target=/src ubuntu bash
```

--mount type=bind 选项告诉 Docker 创建 bind mount，其中 src 是主机上的当前工作目录，而 target 是该目录应该出现在容器中的位置 /src。

运行命令后，Docker 在容器文件系统的根目录启动 bash：

```sh
root@ac1237fad8db:/# pwd
/
root@ac1237fad8db:/# ls
bin   dev  home  media  opt   root  sbin  srv  tmp  var
boot  etc  lib   mnt    proc  run   src   sys  usr
```

可以切换目录至 src：

```sh
root@ac1237fad8db:/# cd src
root@ac1237fad8db:/src# ls
Dockerfile  node_modules  package.json  spec  src  yarn.lock
```

本机系统操作当前工作目录，容器文件系统中的 src 文件夹会同步变化，反之相同。



使用绑定挂载在本地开发设置中很常见。其优点是开发机器不需要安装所有的构建工具和环境。通过一个简单的docker run命令，docker可以提取依赖项和工具。

以下步骤描述了如何使用绑定挂载运行开发容器，该绑定挂载执行以下操作:

+ 将源代码装入容器中

+ 安装所有依赖项

+ 启动nodemon以监视文件系统的更改

**命令行**

```sh
docker run -dp 127.0.0.1:3000:3000 \
    -w /app --mount type=bind,src="$(pwd)",target=/app \
    node:18-alpine \
    sh -c "yarn install && yarn run dev"
```

`-dp 127.0.0.1:3000:3000`：在分离(后台)模式下运行并创建端口映射

`-w /app`：设置“工作目录”或命令将运行的当前目录

`--mount type=bind,src="$(pwd)"，target=/app`： bind 将当前目录从主机挂载到容器节点的 /app 目录

`node:18-alpine`：要使用的镜像。注意，这是来自 Dockerfile sh -c "yarn install && yarn run dev" 命令的应用程序的基本镜像。使用 sh（alpine没有bash）启动 shell，运行 yarn install 来安装包，然后运行 yarn run dev 来启动开发服务器。在 package.json，dev 脚本会启动 nodemon。



**Docker Desktop**

1. Select your image and then select **Run**.
2. Select **Optional settings**.
3. In **Host path**, specify the path to the `getting-started-app` directory on your host machine.
4. In **Container path**, specify `/app`.
5. Select **Run**.


#### 应用虚拟化

当使用容器时，通常需要创建一个 Dockerfile 来定义您的镜像和 `compose.yaml` 以定义如何运行它。

为了创建这些文件，Docker Desktop 有 Docker init 命令。在项目文件夹中的终端中运行此命令，Docker init 创建容器化应用程序所需的所有文件。

```sh
docker init
```

运行项目

```sh
docker compose up
```

[Containerize your application | Docker Docs](https://docs.docker.com/guides/walkthroughs/containerize-your-app/#step-4-update-the-docker-assets)

[Containerize an application | Docker Docs](https://docs.docker.com/get-started/02_our_app/)



#### 上传镜像

**重命名镜像**

```sh
docker tag docker/welcome-to-docker YOUR-USERNAME/welcome-to-docker
```

[Share the application | Docker Docs](https://docs.docker.com/get-started/04_sharing_app/)


#### Docker Compose

Docker Compose 是一个用于定义和共享多容器应用程序的工具，可以创建一个 YAML 文件来定义服务。

Docker Compose 允许将下面这段命令写成更加易懂的 YAML 文件：

```sh
docker run -dp 127.0.0.1:3000:3000 \
  -w /app -v "$(pwd):/app" \
  --network todo-app \
  -e MYSQL_HOST=mysql \
  -e MYSQL_USER=root \
  -e MYSQL_PASSWORD=secret \
  -e MYSQL_DB=todos \
  node:18-alpine \
  sh -c "yarn install && yarn run dev"
```

运行 mysql 容器的命令为：

```sh
docker run -d \
  --network todo-app --network-alias mysql \
  -v todo-mysql-data:/var/lib/mysql \
  -e MYSQL_ROOT_PASSWORD=secret \
  -e MYSQL_DATABASE=todos \
  mysql:8.0
```

对应的 YAML 文件

```yaml
services:
  app:
    image: node:18-alpine
    command: sh -c "yarn install && yarn run dev"
    ports:
      - 127.0.0.1:3000:3000
    working_dir: /app
    volumes:
      - ./:/app
    environment:
      MYSQL_HOST: mysql
      MYSQL_USER: root
      MYSQL_PASSWORD: secret
      MYSQL_DB: todos

  mysql:
    image: mysql:8.0
    volumes:
      - todo-mysql-data:/var/lib/mysql
    environment:
      MYSQL_ROOT_PASSWORD: secret
      MYSQL_DATABASE: todos

volumes:
  todo-mysql-data:
```


编写好 compose.yaml 后，通过下面的命令执行应用：

```sh
docker compose up -d
```

-d 表示后台执行


### 针对编程语言的指南


[Language-specific guides | Docker Docs](https://docs.docker.com/guides/language/)

[C++ | Docker Docs](https://docs.docker.com/guides/language/cpp/)

[Node.js language-specific guide | Docker Docs](https://docs.docker.com/language/nodejs/)

[Python language-specific guide | Docker Docs](https://docs.docker.com/language/python/)

[Java language-specific guide | Docker Docs](https://docs.docker.com/language/java/)

[Go language-specific guide | Docker Docs](https://docs.docker.com/language/golang/)

[.NET language-specific guide | Docker Docs](https://docs.docker.com/language/dotnet/)

[Rust language-specific guide | Docker Docs](https://docs.docker.com/language/rust/)

[PHP language-specific guide | Docker Docs](https://docs.docker.com/language/php/)



### 针对应用常见的指南

#### Generative AI guide

[genai-pdf-bot](https://docs.docker.com/guides/use-case/genai-pdf-bot/)

[genai-video-bot](https://docs.docker.com/guides/use-case/genai-video-bot/)

#### Natural language processing guides

[Build a language translation app | Docker Docs](https://docs.docker.com/guides/use-case/nlp/language-translation/)

[Build a named entity recognition app | Docker Docs](https://docs.docker.com/guides/use-case/nlp/named-entity-recognition/)

[Build a sentiment analysis app | Docker Docs](https://docs.docker.com/guides/use-case/nlp/sentiment-analysis/)

[Build a text recognition app | Docker Docs](https://docs.docker.com/guides/use-case/nlp/text-classification/)

[Build a text summarization app | Docker Docs](https://docs.docker.com/guides/use-case/nlp/text-summarization/)

#### Face detection with TensorFlow.js

[Face detection with TensorFlow.js | Docker Docs](https://docs.docker.com/guides/use-case/tensorflowjs/)

#### Data science with JupyterLab

[Data science with JupyterLab | Docker Docs](https://docs.docker.com/guides/use-case/jupyter/)

#### Suppress CVEs with VEX

[Suppress image vulnerabilities with VEX | Docker Docs](https://docs.docker.com/scout/guides/vex/)


### 资源

docker in action

[Reference documentation | Docker Docs](https://docs.docker.com/reference/)

[Samples overview | Docker Docs](https://docs.docker.com/samples/)



### 镜像名 base、runtime和devel

在搜索镜像时，有时会出现以 base、runtime 和 devel 为后缀的镜像名，以 cuda 为例

**base**：从 cuda 9.0 开始，base 版本包含了部署预构建 cuda 应用程序的最低限度（libcudart）。如果用户需要自己安装 cuda 包，则可以选择使用这个版本。
**runtime**：在 base 版本中添加了 cuda 工具包中的所有共享库。如果使用多个cuda库的预构建应用程序，可使用此版本。但是如果想借助 cuda 中的头文件对自己的工程进行编译，则会出现找不到文件的错误。
**devel**：在 runtime 中添加编译器工具链，测试工具，头文件和静态库，使用此版本可以从源代码编译 cuda 应用程序。


## Docker 使用

### vscode 使用 docker

> 在 wsl 中，使用 vscode 连接 docker 中的 python 环境

启动 docker（打开 docker Desktop 即可），打开 WSL 中的 vscode：

```sh
code .
```

安装下面这三个插件：

1. [WSL - Visual Studio Marketplace](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-wsl)
2. [Dev Containers - Visual Studio Marketplace](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)
3. [Docker - Visual Studio Marketplace](https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-docker)

在侧边栏的 Docker 窗口中选择 IMAGES 下面的镜像，右键镜像，选择 run interactive，成功启动后会在终端中出现：

```
Executing task: docker run --rm -it  tensorflow/tensorflow:1.15.4-gpu-py3 


________                               _______________                
___  __/__________________________________  ____/__  /________      __
__  /  _  _ \_  __ \_  ___/  __ \_  ___/_  /_   __  /_  __ \_ | /| / /
_  /   /  __/  / / /(__  )/ /_/ /  /   _  __/   _  / / /_/ /_ |/ |/ / 
/_/    \___//_/ /_//____/ \____//_/    /_/      /_/  \____/____/|__/


WARNING: You are running this container as root, which can cause new files in
mounted volumes to be created as the root user on your host machine.

To avoid this, run the container by specifying your user's userid:

$ docker run -u $(id -u):$(id -g) args...

root@df63863c8660:/# 
```

这时可以将 docker 环境当成一个 linux 系统来操作了。

如果需要在 docker 环境中使用 vscode，可以在侧边栏中选择 CONTAINERS，右键 container 名，选择 Attach Visual Studio Code，即可打开 Vscode 窗口。



### 创建一个简单的 python 应用

编写一个简单的python脚本

```python
import numpy as np
x = np.random.randn(4, 1600)
y = np.power(x, 2).sum(axis=-1)
print(y)
```

下面编写 Dockerfile 文件

```Dockerfile
FROM docker.registry.cyou/library/python:3.8-slim
RUN pip3 install numpy -i https://pypi.tuna.tsinghua.edu.cn/simple
COPY . .
CMD ["python", "main.py"]
```

其中 `FROM` 指明使用的基础镜像，这里使用了其它镜像源的版本，library 指的是官方版本。`RUN` 后面接需要执行的命令，`COPY` 则是将文件从源地址复制到目标地址，`.` 指当前路径下所有文件，`CMD` 执行 cmd 命令，该命令在启动容器时调用。

构建镜像的命令为

```sh
docker build -t sim_py .
```


下面是一个官方的教程

首先获取 git 仓库

```sh
git clone https://github.com/estebanx64/python-docker-example
cd python-docker-example
```

初始化 docker

```sh
docker init
```

这会创建一些文件，其中需要修改 Dockerfile，删除第一行关于语法的设置（需要额外下载一些东西），设置镜像源和python版本

```Dockerfile
ARG PYTHON_VERSION=3.8
FROM docker.registry.cyou/library/python:${PYTHON_VERSION}-slim as base
```


> [!NOTE]
> 最好在 requirements.txt 的第一行添加 `-i https://pypi.tuna.tsinghua.edu.cn/simple`，否则很有可能失败
> 

构建命令

```sh
docker compose up --build
```

构建成功后，会显示 `Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)`，不要直接访问，需要访问 [localhost:8000](http://localhost:8000/)



## Docker环境下出现的问题

> 在 docker 环境下执行 apt-get install 出现下面的错误：

```txt
E: Failed to fetch http://security.ubuntu.com/ubuntu/pool/main/libx/libx11/libx11-data_1.6.4-3ubuntu0.3_all.deb  404  Not Found [IP: 91.189.91.82 80]
...
Unable to fetch some archives, maybe run apt-get update or try with --fix-missing
```

执行下面的命令，更新下载源

```sh
apt-get update
```

之后再执行下载命令。



> 在 docker 环境中下载 python 包太慢，甚至导致 read time out，需要设置下载源。

首先创建 .pip 文件夹：

```sh
mkdir ~/.pip
```

配置 .pip/pip.conf 文件：

```sh
vim ~/.pip/pip.conf
```

添加如下内容：

```ini
[global]
index-url = https://pypi.tuna.tsinghua.edu.cn/simple

[install]
trusted-host=mirrors.aliyun.com
```



> docker 创建容器没有反应 

[解决在Windows11上新安装的Docker Desktop一直显示"starting the Docker Engine"登录不上去的问题 - 知乎 (zhihu.com)](https://zhuanlan.zhihu.com/p/663821762)

