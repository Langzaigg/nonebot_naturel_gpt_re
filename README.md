# nonebot_plugin_naturel_gpt

基于 NoneBot2 + OneBot v11 的群聊人格聊天插件。支持流式响应、多模态图片输入、原生工具调用、动态人格加载和 `rg` 指令切换人格。

## 目录结构

```text
naturel_gpt/
├── nonebot_plugin_naturel_gpt/     # NoneBot2 插件
│   ├── llm_tool_plugins/           # 内置 LLM 工具
│   ├── MCrcon/                     # Minecraft RCON 集成
│   ├── res/                        # 文生图资源
│   └── *.py                        # 插件核心代码
├── comfyui_plugin/                 # ComfyUI AnimaTool 画图插件
│   ├── executor/                   # 执行器
│   ├── knowledge/                  # 知识库
│   ├── schemas/                    # Schema 定义
│   ├── servers/                    # 服务端
│   └── ...
├── examples/                       # 配置示例
└── README.md
```

## 内置工具

| 工具 | 说明 | 配置项 |
|------|------|--------|
| `pixiv_search` | Pixiv 搜图（Lolicon API） | `LLM_TOOL_LOLICON_CONFIG` |
| `fetch_url` | HTTP 轻量抓取网页文本 | `WEB_FETCH_TIMEOUT` / `WEB_FETCH_MAX_CHARS` |
| `browse_url` | Playwright 浏览器渲染抓取 | `PLAYWRIGHT_TIMEOUT` |
| `bocha_search` | 博查联网搜索 | `BOCHA_API_KEY` / `BOCHA_SEARCH_COUNT` |
| `remember` | 记忆工具（群记忆/用户记忆） | `MEMORY_ACTIVE` / `MEMORY_MAX_LENGTH` |
| `generate_anima_image` | ComfyUI Anima 画图 | `COMFYUI_BASE_URL`（通过 `rg draw on` 启用） |

### 记忆工具

支持两种 scope：
- `group`：群记忆，所有人共享，注入到 `[群记忆]`
- `user`：用户记忆，仅对该用户有效，注入到 `[你的记忆]`

记忆与人格关联，每个人格有独立记忆空间。LLM 会在对话中自然识别重要信息并主动记住，对用户透明。

### ComfyUI 画图工具

通过 `rg draw on` 命令启用。需要先部署 ComfyUI 服务和 AnimaTool 插件。

详见 [comfyui_plugin/README.md](comfyui_plugin/README.md)

## 快速开始

### 1. 部署 NoneBot2

```bash
# 安装 NoneBot2
pip install nonebot2 nonebot-adapter-onebot

# 创建项目
nb create
```

### 2. 安装插件依赖

```bash
pip install httpx tiktoken playwright
playwright install chromium  # 如需 browse_url 工具
```

### 3. 放置插件

将 `nonebot_plugin_naturel_gpt/` 复制到 NoneBot2 项目的插件目录下。

### 4. 配置

在 NoneBot2 全局配置中指定插件配置路径：

```yaml
# .env.prod 或 bot.py
ng_config_path: config/naturel_gpt_config.yml
```

创建配置文件 `config/naturel_gpt_config.yml`：

```yaml
# LLM 配置
OPENAI_API_KEYS:
  - sk-your-api-key
OPENAI_BASE_URL: https://api.openai.com/v1
OPENAI_TIMEOUT: 60
CHAT_MODEL: gpt-4o
CHAT_MODEL_MINI: gpt-4o-mini

# 上下文管理
CONTEXT_TOKEN_BUDGET: 32768
CONTEXT_WINDOW_SIZE: 20
CONTEXT_SUMMARY_ENABLED: true

# 工具调用
LLM_ENABLE_TOOLS: true
LLM_MAX_TOOL_ROUNDS: 7

# 博查搜索（可选）
BOCHA_API_KEY: your-bocha-api-key
BOCHA_SEARCH_COUNT: 10

# ComfyUI 画图（可选）
COMFYUI_BASE_URL: http://127.0.0.1:8188
```

### 5. 添加人格

创建 `config/personas/` 目录，添加人格文件：

```bash
mkdir config/personas
```

支持两种格式：
- **单文件人格**：`config/personas/兔酱.md`（文件名即人格名）
- **Skill 文件夹**：`config/personas/兔酱-skill/SKILL.md`（文件夹名第一个 `-` 前的部分即人格名）

### 6. 启动

```bash
nb run
```

## 部署 ComfyUI 画图（可选）

### 1. 部署 ComfyUI

```bash
# 克隆 ComfyUI
git clone https://github.com/comfyanonymous/ComfyUI.git
cd ComfyUI

# 安装依赖
pip install -r requirements.txt
```

### 2. 安装 AnimaTool 插件

将 `comfyui_plugin/` 复制到 ComfyUI 的 `custom_nodes/` 目录下：

```bash
cp -r comfyui_plugin/ ComfyUI/custom_nodes/ComfyUI-AnimaTool
```

安装插件依赖：

```bash
cd ComfyUI/custom_nodes/ComfyUI-AnimaTool
pip install -r requirements.txt
```

### 3. 启动 ComfyUI

```bash
cd ComfyUI
python main.py --listen 0.0.0.0 --port 8188
```

### 4. 在 NoneBot2 中启用

发送指令：

```
rg draw on
```

这会：
1. 检查 ComfyUI 连接
2. 拉取画图 Schema 和知识库
3. 注册画图工具

## 配置参考

### LLM 配置

| 配置项 | 说明 | 默认值 |
|--------|------|--------|
| `OPENAI_API_KEYS` | API Key 列表（支持轮换） | - |
| `OPENAI_BASE_URL` | API 基础 URL | `https://api.openai.com/v1` |
| `OPENAI_TIMEOUT` | 请求超时（秒） | `60` |
| `CHAT_MODEL` | 聊天模型 | `gpt-4o` |
| `CHAT_MODEL_MINI` | 轻量模型（摘要用） | `gpt-4o-mini` |
| `CHAT_TEMPERATURE` | 温度 | `0.4` |

### 上下文管理

| 配置项 | 说明 | 默认值 |
|--------|------|--------|
| `CONTEXT_TOKEN_BUDGET` | 上下文 token 预算 | `3072` |
| `CONTEXT_WINDOW_SIZE` | 滑动窗口大小（消息条数） | `16` |
| `CONTEXT_SUMMARY_ENABLED` | 启用摘要压缩 | `false` |

### 多模态

| 配置项 | 说明 | 默认值 |
|--------|------|--------|
| `MULTIMODAL_ENABLE` | 启用图片输入 | `true` |
| `MULTIMODAL_HISTORY_LENGTH` | 图片历史视野 | `4` |
| `MULTIMODAL_MAX_MESSAGES_WITH_IMAGES` | 最大图片消息数 | `2` |
| `MULTIMODAL_IMAGE_FRESH_MINUTES` | 图片有效期（分钟） | `30` |

### 工具

| 配置项 | 说明 | 默认值 |
|--------|------|--------|
| `LLM_ENABLE_TOOLS` | 启用工具调用 | `true` |
| `LLM_MAX_TOOL_ROUNDS` | 最大工具调用轮数 | `3` |
| `BOCHA_API_KEY` | 博查搜索 API Key | - |
| `BOCHA_SEARCH_COUNT` | 搜索结果数量 | `10` |
| `COMFYUI_BASE_URL` | ComfyUI 服务地址 | `http://127.0.0.1:8188` |

### 记忆

| 配置项 | 说明 | 默认值 |
|--------|------|--------|
| `MEMORY_ACTIVE` | 启用记忆功能 | `true` |
| `MEMORY_MAX_LENGTH` | 最大记忆条数 | `16` |

## rg 指令

```text
rg              # 刷新并展示人格列表
rg list         # 同上
rg set <人格名>  # 切换人格
rg query <人格名> # 查看人格详情
rg draw on      # 启用 ComfyUI 画图
rg draw off     # 禁用 ComfyUI 画图
```

## 迁移说明

- 旧版扩展系统已移除（`NG_EXT_*`）
- 不再支持模型输出 `/#tool&args#/` 调用工具
- 工具统一在 `llm_tool_plugins/` 中，通过原生工具调用执行
- 人格统一从配置文件同级 `personas/` 子目录加载

## License

MIT
