## 安装

>如果使用Windows系统，建议在wsl2上安装

1. 首先安装node，已安装跳过
先安装nvm，命令如下：

```bash
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/master/install.sh | bash
```

完成后重启终端

```bash
source ~/.bashrc
```

安装node.js
```bash
nvm install --lts
```


2. 为wsl2启动systemd
在wsl2终端中执行如下命令（注意下面的命令需要一行一行输入）
```bash
sudo tee /etc/wsl.conf >/dev/null <<'EOF'
[boot]
systemd=true
EOF
```

然后在powershell执行
```ps
wsl --shutdown
```

重新打开wsl2，检查是否正常输出信息

```bash
systemctl --user status
```

3. 使用cnpm安装openclaw
直接用npm安装大概率会失败，所以使用cnpm
```bash
npm install -g cnpm --registry=https://registry.npmmirror.com
cnpm install -g openclaw@latest
```

4. 初始化openclaw

```bash
openclaw onboard --install-daemon
```

配置时可以跳过的先跳过，大模型可以选择openrouter，里面可能会有免费的模型用

5. 验证状态

在wsl2中验证状态

```bash
openclaw gateway status
openclaw status
openclaw health
```

在Windows的浏览器里面打开 http://127.0.0.1:18789/ ，确定是否显示正常网页。

如果出现unauthorized: gateway token missing (open the dashboard url and paste the token in control ui settings)这种报错，可以在wsl2终端中输入
```bash
openclaw dashboard --no-open
```

这条命令可以获取到token，再输入就可以解决这个问题了。

## 模型

### 添加新模型

在 `~\.openclaw\openclaw.json`中配置

```json
{
  "agents": {
    "defaults": {
      "model": {
        "primary": "openrouter/stepfun/step-3.5-flash:free"
      },
      "models": {
        "openrouter/auto": {
          "alias": "OpenRouter"
        },
        "openrouter/stepfun/step-3.5-flash:free": {},
        "openrouter/nvidia/nemotron-nano-12b-v2-vl:free": {}  // 新添加
      },
    },
    "list": [
      {
        "id": "main",
        "model": "openrouter/stepfun/step-3.5-flash:free"
      },
      // 新添加
      {
        "id": "image",
        "model": "openrouter/nvidia/nemotron-nano-12b-v2-vl:free"
      }
    ]
  },
}

```

### 查看模型

使用下面这条命令查看模型

```bash
openclaw models list
```

### 切换模型

在openclaw的对话框内输入 `/model model_name`切换模型

```bash
/model openrouter/nvidia/nemotron-nano-12b-v2-vl:free
```


## Skills

[VoltAgent/awesome-openclaw-skills: The awesome collection of OpenClaw skills. 5,400+ skills filtered and categorized from the official OpenClaw Skills Registry.🦞](https://github.com/VoltAgent/awesome-openclaw-skills?tab=readme-ov-file#table-of-contents) 这个网站上有许多skills

openclaw中有一些内置的skills，部分需要输入额外的信息才能使用

### ClawHub

[ClawHub](https://clawhub.ai/) 是OpenClaw 的公共 Skills 注册中心，Skills 就是一个包含 `SKILL.md` 文件（以及辅助文本文件）的文件夹。你可以在网页应用中浏览 Skills，也可以使用 CLI 来搜索、安装、更新和发布 Skills。

安装clawhub的命令为

```bash
cnpm i -g clawhub
```

登录clawhub，使用下面这条命令可以登录

```bash
clawhub login
```

但是如果在wsl2环境中可能会报错，可以直接先在浏览器中登录然后生成api token，复制token，作为命令行参数登录

```bash
clawhub login --token <token>
```

使用clawhub搜索skills，如搜索可以实现网页搜索的skill

```bash
clawhub search "search"
```

>上面这条命令似乎容易出错，可以先在网页寻找想要的skill，然后记住名字再下载

下载skill，以[DuckDuckGo Web Search]([DuckDuckGo Web Search — ClawHub](https://clawhub.ai/JakeLin/ddg-web-search))为例

```bash
clawhub install ddg-web-search
```

确认有哪些skill可用
```bash
openclaw skills list
```

### 配置环境变量

一些skill需要用到api key，这时候需要设置环境变量。

以[baidu search](https://console.bce.baidu.com/qianfan/tools/toolsCenter/web_search/detail)为例，首先申请一个api key，地址为[百度千帆 - 百度智能云控制台](https://console.bce.baidu.com/qianfan/ais/console/apiKey)

使用clawhub下载对应的skill

```bash
clawhub install baidu-search
```

在`~/.openclaw/openclaw.json`中设置

```json
{
"skills": {
    "load": {
      "watch": true,
      "watchDebounceMs": 20
    },
    "install": {
      "nodeManager": "pnpm"
    },
    "entries": {
      "baidu-search": {
        "enabled": true, // true表示启用
        "env": {
          "BAIDU_API_KEY": "API-Key"  // 填入对应值
        }
      }
    }
  },
}
```

最后重启openclaw服务

```bash
openclaw gateway restart
```


## channels

### QQ

点击[QQ开放平台｜机器人列表](https://q.qq.com/qqbot/openclaw/)，创建机器人

在openclaw中执行下列命令（配置一下npm，不然容易失败）

```bash
npm config set registry https://registry.npmmirror.com
openclaw plugins install @tencent-connect/openclaw-qqbot@latest
openclaw channels add --channel qqbot --token "AppID:AppSecret"
openclaw gateway restart
```

执行完后，可以直接在QQ上和机器人对话，相当于和openclaw对话。

## 用例

一些GitHub库

[hesamsheikh/awesome-openclaw-usecases: A community collection of OpenClaw use cases for making life easier.](https://github.com/hesamsheikh/awesome-openclaw-usecases)

[clawdbot-ai/awesome-openclaw-skills-zh: OpenClaw 中文官方技能库 | 翻译自 Clawdbot 官方技能，按场景分类整理，支持中文自然语言调用](https://github.com/clawdbot-ai/awesome-openclaw-skills-zh)

[xianyu110/awesome-openclaw-tutorial: 从零开始玩转OpenClaw：最全面的中文教程，涵盖安装、配置、实战案例和避坑指南（github版）](https://github.com/xianyu110/awesome-openclaw-tutorial)

[cogine-ai/awesome-openclaw-zh: OpenClaw 中文实战库：176 个可复制使用场景，从部署到5分钟上手到完全精通。案例覆盖自动化、内容创作、运营增长与安全使用。](https://github.com/cogine-ai/awesome-openclaw-zh)


### 搜索新闻

先安装并配置baidu-search，具体步骤可以参考[如何在OpenClaw调用官方工具 - 百度千帆·大模型服务及Agent开发平台](https://cloud.baidu.com/doc/qianfan/s/Mmlda41a2#3-skills-%E5%AE%89%E8%A3%85)

输入命令

```
使用baidu-search skill搜索今日新闻
```

得到输出

```
好的，我来帮您使用 baidu-search 技能搜索今日新闻。✅ 配置正常。现在执行搜索今日新闻：✅ **搜索完成！** 以下是今日（2026年3月10-11日）新闻速览：

...
```

查看baidu search的余量：[百度千帆 - 百度智能云控制台](https://console.bce.baidu.com/qianfan/studio/resource)


### 查询百度百科

使用[baidu baike search](https://clawhub.ai/ide-rea/baidu-baike-data)搜索，首先在[百度智能云控制台](https://console.bce.baidu.com/qianfan/ais/console/apiKey)申请api key。

安装对应技能

```bash
clawhub install baidu-baike-data
```

配置技能需要的环境变量，前面说过在`~/.openclaw/openclaw.json`中配置环境变量，还可以利用可视化ui进行配置。在web页面[OpenClaw Control](http://127.0.0.1:18789/skills)上搜索baidu-baike-data，此时如果没有配置环境变量，会发现存在配置的输入框，直接填写即可。

完成配置后，可以输入命令观察结果

```
使用baidu-baike-data技能搜索openclaw
```

### 语音合成（简单）

使用[Edge TTS](https://clawhub.ai/i3130002/edge-tts)技能

```bash
clawhub install edge-tts
```

输入命令

```
使用edge-tts技能合成一段中文语音并直接播放，内容为：这是一条测试语音
```


### 语音合成（进阶）

下载[Qwen3-TTS-12Hz-0.6B-CustomVoice](https://www.modelscope.cn/models/Qwen/Qwen3-TTS-12Hz-0.6B-CustomVoice)模型，配置python环境

编写一个skill，包括脚本和`SKILL.md`，GitHub地址位于[openclaw-skills/qwen-tts at master · Xiang-M-J/openclaw-skills](https://github.com/Xiang-M-J/openclaw-skills/tree/master/qwen-tts)

脚本中使用fastapi启用服务，通过curl来调用服务

```bash
alias tts-say='function _tts(){ curl -s -X POST "http://127.0.0.1:8000/generate" -H "Content-Type: application/json" -d "{\"text\":\"$1\", \"output_path\":\"$2\"}"; }; _tts'
tts-say "这是一条测试语音" "~/output_zh.wav"
```

在`~\.openclaw\openclaw.json`中启用qwen-tts

```json
"skills": {
    "load": {
      "watch": true,
      "watchDebounceMs": 20
    },
    "install": {
      "nodeManager": "pnpm"
    },
    "entries": {
      "qwen3-tts": {
        "enabled": true
      }
    }
  }
```


