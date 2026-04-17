# nonebot_plugin_naturel_gpt

基于 NoneBot2 + OneBot v11 的群聊人格聊天插件。支持流式响应、多模态图片输入、原生工具调用、动态人格加载和 `rg` 指令切换人格。

## 目录结构

```text
nonebot_plugin_naturel_gpt/     # 插件代码
├── llm_tool_plugins/           # 内置 LLM 工具
├── MCrcon/                     # Minecraft RCON 集成
├── res/                        # 文生图资源
├── __init__.py
├── chat.py                     # 聊天核心（人格、记忆、prompt 构建）
├── chat_manager.py
├── command_func.py             # rg 指令
├── config.py                   # 配置加载
├── llm_tools.py                # 工具注册与调度
├── matcher.py                  # OneBot v11 消息处理
├── matcher_MCRcon.py
├── openai_func.py              # LLM 调用（流式、工具调用轮次）
├── persistent_data_manager.py  # 数据持久化
├── persona_loader.py           # 人格文件加载
├── utils.py                    # 消息提取、用户名解析
├── text_func.py / text_to_image.py / store.py / singleton.py / logger.py
└── README.md

examples/
├── naturel_gpt_config.example.yml   # 配置示例
└── persona.example.md               # 人格示例
```

## 依赖

```text
httpx
playwright
tiktoken
```

如需 `browse_url` 浏览器抓取工具，还需安装 Chromium：

```powershell
playwright install chromium
```

## 快速开始

### 1. 安装插件

将 `nonebot_plugin_naturel_gpt/` 放到 NoneBot2 项目的插件目录下，并在 `pyproject.toml` 或 `bot.py` 中加载。

### 2. 配置

在 NoneBot 全局配置中指定配置文件路径：

```yaml
ng_config_path: config/naturel_gpt_config.yml
```

参考 `examples/naturel_gpt_config.example.yml` 创建配置文件。

### 3. 人格

将人格文件放到配置文件同级的 `personas/` 目录下。参考 `examples/persona.example.md`。

支持两种格式：
- `.md` 单文件人格（文件名即人格名）
- skill 文件夹人格（文件夹名第一个 `-` 前的部分即人格名）

## 功能说明

### 大模型配置

```yaml
OPENAI_API_KEYS:
  - sk-xxx
OPENAI_BASE_URL: https://api.openai.com/v1
OPENAI_PROXY_SERVER: ''
OPENAI_TIMEOUT: 60
CHAT_MODEL: gpt-4o
CHAT_MODEL_MINI: gpt-4o-mini
```

- `CHAT_MODEL` 用于正常聊天
- `CHAT_MODEL_MINI` 用于摘要和用户印象总结
- `OPENAI_BASE_URL` 支持 OpenAI-compatible API
- 支持多 API Key 轮换

### 流式响应

```yaml
LLM_ENABLE_STREAM: true
LLM_SHOW_REASONING: false
```

### 分段发送

检测双换行 `\n\n` 自动切段，每段间隔 `REPLY_SEGMENT_INTERVAL` 秒，最多 `REPLY_MAX_SEGMENTS` 段。

```yaml
NG_ENABLE_MSG_SPLIT: true
REPLY_SEGMENT_INTERVAL: 1.0
REPLY_MAX_SEGMENTS: 5
```

### 多模态图片输入

```yaml
MULTIMODAL_ENABLE: true
MULTIMODAL_HISTORY_LENGTH: 4
MULTIMODAL_MAX_MESSAGES_WITH_IMAGES: 2
```

读取 OneBot `image` 消息段的 URL，作为 `image_url` 传给模型。模型需支持视觉输入。

### 工具调用

使用原生 OpenAI-compatible 工具调用。

```yaml
LLM_ENABLE_TOOLS: true
LLM_MAX_TOOL_ROUNDS: 3
```

内置工具：

| 工具 | 说明 | 配置 |
|------|------|------|
| `pixiv_search` | Lolicon API 搜图 | `LLM_TOOL_LOLICON_CONFIG` |
| `fetch_url` | HTTP 抓取网页文本 | `WEB_FETCH_TIMEOUT` / `WEB_FETCH_MAX_CHARS` |
| `browse_url` | Playwright 浏览器渲染 | `PLAYWRIGHT_TIMEOUT` |
| `bocha_search` | 博查联网搜索 | `BOCHA_API_KEY` / `BOCHA_API_BASE` |

### 唤醒与回复

```yaml
REPLY_ON_AT: true
REPLY_ON_NAME_MENTION_PROBABILITY: 0.1
RANDOM_CHAT_PROBABILITY: 0.0
WORD_FOR_WAKE_UP: []
```

- `@bot` 触发回复
- 消息中提及 bot 昵称，按概率回复
- 消息句首包含唤醒词或当前角色名，无条件触发
- 随机概率主动回复

### rg 指令

```text
rg              # 刷新并展示人格列表
rg list         # 同上
rg set <人格名>  # 切换人格
rg query <人格名> # 查看人格详情
rg reload_config # 重载配置
```

新增/修改人格后无需重启，`rg` 或 `rg set` 即可触发动态加载。

### 数据持久化

聊天数据默认保存到 `data/naturel_gpt/naturel_gpt.json`，日志保存到 `data/naturel_gpt/logs/`。

## 迁移说明

- 旧版扩展系统已移除（`NG_EXT_*`）
- 不再支持模型输出 `/#tool&args#/` 调用工具
- 工具统一在 `llm_tool_plugins/` 中，通过原生工具调用执行
- 人格统一从配置文件同级 `personas/` 子目录加载
