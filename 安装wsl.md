## 安装 WSL

在 powershell 中执行 `wsl --install`，之后会在 C 盘中默认安装一个 Linux 系统。使用下面的命令可以不安装系统：

```powershell
wsl --install --no-distribution
```



选择在其他盘中安装 Linux 系统[Win10自定义路径位置安装WSL2 (Ubuntu 20.04) 并配置CUDA_wsl安装路径-CSDN博客](https://blog.csdn.net/weixin_41973774/article/details/117223425)

1. 先去 Windows Store 中下载 Ubuntu 20.04，下载下来后不用管它
2. 以管理员模式打开 powershell，进入 Ubuntu 20.04 的安装位置（无法直接进入）

```powershell
cd "C:\Program Files\WindowsApps"
```

3. dir 找到 Ubuntu 20.04 可能的文件夹位置

```powershell
dir CanonicalGroupLimited*
```

4. 通过 Tab 键选择需要查看的文件夹，直到看到出现 **ubuntu<版本号>.exe**

```sh
dir .\CanonicalGroupLimited.Ubuntu20.04LTS_2004.6.16.0_x64__79rhkp1fndgsc\

    目录: C:\Program Files\WindowsApps\CanonicalGroupLimited.Ubuntu20.04LTS_2004.6.16.0_x64__79rhkp1fndgsc


Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
d-----          2024/3/9      9:12                AppxMetadata
d-----          2024/3/9      9:12                Assets
d-----          2024/3/9      9:12                Terminal
-a----          2024/3/9      9:12         523852 AppxBlockMap.xml
-a----          2024/3/9      9:12           3677 AppxManifest.xml
-a----          2024/3/9      9:12          12035 AppxSignature.p7x
-a----          2024/3/9      9:13      567587703 install.tar.gz
-a----          2024/3/9      9:13           3648 resources.pri
-a----          2024/3/9      9:13         598016 ubuntu2004.exe
```

5. 将安装包复制到想安装的位置：

```sh
cp .\CanonicalGroupLimited.Ubuntu20.04LTS_2004.6.16.0_x64__79rhkp1fndgsc\* E:\Ubuntu2004
```

安装目录中的**ubuntu<版本号>.exe**就是 Ubuntu 的启动程序，直接双击安装，安装完之后可以选择将其添加到开始菜单。



> 安装完 WSL，每次使用 wsl 命令进入时都会进入当前路径，不方便操作。可以在 ~/.bashrc 或者 ~/.zashrc 加上 cd ~ 来在每次进入系统时回到主目录。
>
> ```bash
> cd ~
> ```



## WSL 的一些命令

```powershell
wsl --list --online  # 列出可用的 Linux 版本
wsl --list --verbose # 列出已经安装的 linux 版本
wsl --shutdown       # 关闭 Linux
wsl --unregister <DistributionName>  # 注销并卸载 WSL 发行版
```







### 在 WSL 中使用 Vscode

[开始通过 WSL 使用 VS Code | Microsoft Learn](https://learn.microsoft.com/zh-cn/windows/wsl/tutorials/wsl-vscode)

- 访问 [VS Code 安装页](https://code.visualstudio.com/download)，选择 32 位或 64 位安装程序。 在 Windows 上（不是在 WSL 文件系统中）安装 Visual Studio Code。
- 当在安装过程中系统提示“选择其他任务”时，请务必选中“添加到 PATH”选项，以便可以使用代码命令在 WSL 中轻松打开文件夹。
- 安装[远程开发扩展包](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.vscode-remote-extensionpack)。 除了 Remote - SSH 和 Dev Containers 扩展之外，此扩展包还包含 WSL 扩展，使你能够打开容器中、远程计算机上或 WSL 中的任何文件夹。

如果想要打开 vscode，直接在 WSL 的命令行中输入 `code .` 即可

如果该命令报错，可以选择在 Windows 中打开 vscode，Ctrl+Shift+P 打开命令面板，选择 `WSL:Connect to WSL in New Window`

然后在新的窗口中打开终端，输入 `code .` ，打开对应的文件夹。



### 在 WSL 中使用 Git

一般 Linux 中都有 Git，需要对 Git 进行配置：

```sh
git config --global user.name "Your Name"
git config --global user.email "youremail@domain.com"
```



### 在 WSL 中使用 Cuda

[CUDA on WSL (nvidia.com)](https://docs.nvidia.com/cuda/wsl-user-guide/index.html#getting-started-with-cuda-on-wsl)

保证 WSL 最新：

```powershell
wsl.exe --update
```

删除旧的 GPG key：

```sh
sudo apt-key del 7fa2af80
```

确定需要安装的cuda版本 [CUDA Toolkit Archive | NVIDIA Developer](https://developer.nvidia.com/cuda-toolkit-archive)，选择合适的版本。以 11.8.0 为例：

```sh
wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/cuda-ubuntu2004.pin
sudo mv cuda-ubuntu2004.pin /etc/apt/preferences.d/cuda-repository-pin-600
wget https://developer.download.nvidia.com/compute/cuda/11.8.0/local_installers/cuda-repo-ubuntu2004-11-8-local_11.8.0-520.61.05-1_amd64.deb
sudo dpkg -i cuda-repo-ubuntu2004-11-8-local_11.8.0-520.61.05-1_amd64.deb
sudo cp /var/cuda-repo-ubuntu2004-11-8-local/cuda-*-keyring.gpg /usr/share/keyrings/
sudo apt-get update
sudo apt-get -y install cuda
```



> 编译 kaldi 的 GPU 版本时报错 configure failed: CUDA 10_1 does not support c++ (g++-9). Only versions strictly older than 9.0 are supported. 

```sh
 if [ ! -d "$CUDATKDIR" ]; then
     for base in /usr/ /usr/local/share/cuda /usr/local/cuda ; do
 	    if [ -f $base/bin/nvcc ]; then
	         CUDATKDIR=$base
        fi
     done
 fi
```

> 注意configure 中的 `use_cuda` 默认为 false，需要改为 true





> 当脚本没有按照预想的生成结果，如提示`mkgraph.sh: expected data/graph/lang/L_disambig.fst to exist`，应该检查一下在数据处理的时候是否出现了下面的报错  
>
> sh: 1: export: Files/WindowsApps/CanonicalGroupLimited.Ubuntu20.04LTS_2004.6.16.0_x64__79rhkp1fndgsc:/mnt/c/Program: bad variable name

在 `kaldi/egs/thchs30/s5/utils/validate_lang.pl` 中注释掉检查 olabel sorted 的部分代码

```perl6
# Check oov -------------------------------
check_txt_int("$lang/oov", \%wsymtab, 0); print "\n";

# Check if L.fst is olabel sorted.
# if (-e "$lang/L.fst") {
#   $cmd = "fstinfo $lang/L.fst | grep -E 'output label sorted.*y' > /dev/null";
#   $res = system(". ./path.sh; $cmd");
#   if ($res == 0) {
#     print "--> $lang/L.fst is olabel sorted\n";
#   } else {
#     print "--> ERROR: $lang/L.fst is not olabel sorted\n";
#     $exit = 1;
#   }
# }

# # Check if L_disambig.fst is olabel sorted.
# if (-e "$lang/L_disambig.fst") {
#   $cmd = "fstinfo $lang/L_disambig.fst | grep -E 'output label sorted.*y' > /dev/null";
#   $res = system(". ./path.sh; $cmd");
#   if ($res == 0) {
#     print "--> $lang/L_disambig.fst is olabel sorted\n";
#   } else {
#     print "--> ERROR: $lang/L_disambig.fst is not olabel sorted\n";
#     $exit = 1;
#   }
# }

# if (-e "$lang/G.fst") {
#   # Check that G.fst is ilabel sorted and nonempty.
#   $text = `. ./path.sh; fstinfo $lang/G.fst`;
#   if ($? != 0) {
#     print "--> ERROR: fstinfo failed on $lang/G.fst\n";
#     $exit = 1;
#   }
#   if ($text =~ m/input label sorted\s+y/) {
#     print "--> $lang/G.fst is ilabel sorted\n";
#   } else {
#     print "--> ERROR: $lang/G.fst is not ilabel sorted\n";
#     $exit = 1;
#   }
#   if ($text =~ m/# of states\s+(\d+)/) {
#     $num_states = $1;
#     if ($num_states == 0) {
#       print "--> ERROR: $lang/G.fst is empty\n";
#       $exit = 1;
#     } else {
#       print "--> $lang/G.fst has $num_states states\n";
#     }
#   }

#   # Check that G.fst is determinizable.
#   if (!$skip_det_check) {
#     # Check determinizability of G.fst
#     # fstdeterminizestar is much faster, and a more relevant test as it's what
#     # we do in the actual graph creation recipe.
#     if (-e "$lang/G.fst") {
#       $cmd = "fstdeterminizestar $lang/G.fst /dev/null";
#       $res = system(". ./path.sh; $cmd");
#       if ($res == 0) {
#         print "--> $lang/G.fst is determinizable\n";
#       } else {
#         print "--> ERROR: fail to determinize $lang/G.fst\n";
#         $exit = 1;
#       }
#     }
#   }

#   # Check that G.fst does not have cycles with only disambiguation symbols or
#   # epsilons on the input, or the forbidden symbols <s> and </s> (and a few
#   # related checks

#   if (-e "$lang/G.fst") {
#     system("utils/lang/check_g_properties.pl $lang");
#     if ($? != 0) {
#       print "--> ERROR: failure running check_g_properties.pl\n";
#       $exit = 1;
#     } else {
#       print("--> utils/lang/check_g_properties.pl succeeded.\n");
#     }
#   }
# }


# if (!$skip_det_check) {
#   if (-e "$lang/G.fst" && -e "$lang/L_disambig.fst") {
#     print "--> Testing determinizability of L_disambig . G\n";
#     $output = `. ./path.sh; fsttablecompose $lang/L_disambig.fst $lang/G.fst | fstdeterminizestar | fstinfo 2>&1 `;
#     if ($output =~ m/# of states\s*[1-9]/) {
#       print "--> L_disambig . G is determinizable\n";
#     } else {
#       print "--> ERROR: fail to determinize L_disambig . G.  Output is:\n";
#       print "$output\n";
#       $exit = 1;
#     }
#   }
# }

# if ($exit == 1) {
#   print "--> ERROR (see error messages above)\n"; exit 1;
# } else {
#   if ($warning == 1) {
#     print "--> WARNING (check output above for warnings)\n"; exit 0;
#   } else {
#     print "--> SUCCESS [validating lang directory $lang]\n"; exit 0;
#   }
# }

```

