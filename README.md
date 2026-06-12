# Naturel GPT 插件

基于 NoneBot2 + OneBot v11 的群聊人格聊天插件，支持流式响应、多模态图片输入、原生工具调用和动态人格加载。

## 功能特性

- **多模型支持**：通过 OpenAI-compatible API 调用各种大模型
- **流式响应**：实时生成并分段发送回复
- **多模态输入**：支持图片消息，可识别图片内容
- **工具调用**：原生工具调用，支持搜索、网页抓取、Pixiv 搜索等
- **动态人格**：支持 Markdown 文件和 Skill 文件夹两种人格格式
- **记忆系统**：群记忆和用户记忆，支持记忆整理
- **上下文管理**：智能上下文压缩和摘要生成
- **ComfyUI 画图**：集成 Anima 画图工具

## 目录结构

```
nonebot_plugin_naturel_gpt/
├── __init__.py              # 插件入口
├── matcher.py               # 消息匹配和处理
├── chat.py                  # 会话管理
├── chat_history.py          # 对话历史管理
├── chat_memory.py           # 记忆管理
├── chat_prompt.py           # Prompt 构造
├── chat_summary.py          # 摘要生成
├── config.py                # 配置管理
├── openai_func.py           # LLM 调用
├── llm_tools.py             # 工具管理
├── llm_tool_plugins/        # 工具插件目录
│   ├── anima_generate.py    # ComfyUI 画图
│   ├── bocha_search.py      # 博查搜索
│   ├── browse_url.py        # 浏览器抓取
│   ├── fetch_url.py         # HTTP 抓取
│   ├── memory.py            # 记忆工具
│   ├── pixiv_search.py      # Pixiv 搜索
│   └── tavily_search.py     # Tavily 搜索
├── image_cache.py           # 图片缓存
├── persistent_data_manager.py # 持久化数据管理
├── command_func.py          # 指令处理
├── persona_loader.py        # 人格加载
├── draw_db.py               # 绘图数据库
└── utils.py                 # 工具函数

config/
├── naturel_gpt_config.yml   # 主配置文件
└── personas/                # 人格目录
    ├── SOUL.md              # 简易人格示例
    └── 宫子-skill-main/     # Skill 人格示例
        ├── SKILL.md
        ├── soul.md
        ├── limit.md
        └── resource/

comfyui_plugin/              # ComfyUI AnimaTool
├── executor/                # 执行器
└── servers/                 # 服务器
```

## 快速开始

### 1. 安装依赖

```bash
pip install httpx tiktoken playwright
playwright install chromium  # 可选，用于 browse_url 工具
```

### 2. 配置文件

复制 `config/naturel_gpt_config.yml.example` 为 `config/naturel_gpt_config.yml`，并填入你的配置：

```yaml
OPENAI_PROFILES:
  default:
    api_keys:
      - sk-your-api-key-here
    base_url: https://api.openai.com/v1
    model: gpt-4o
```

### 3. 配置人格

将人格文件放入 `config/personas/` 目录：

- **简易人格**：创建 `.md` 文件，文件名即人格名
- **Skill 人格**创建文件夹，格式为 `人格名-skill-main/`

### 4. 启动插件

```bash
nb run
```

## 人格系统

### 简易人格

创建一个 `.md` 文件，内容即为系统提示词：

```markdown
# SOUL

你是一个活泼可爱的群聊 AI 助手...
```

文件名为 `SOUL.md`，则人格名为 `SOUL`。

### Skill 人格

创建一个文件夹，格式为 `人格名-skill-main/`，包含以下文件：

- `SKILL.md`：角色设定（必需）
- `soul.md`：灵魂设定
- `limit.md`：限制设定
- `resource/behavior_guide.md`：行为指南
- `resource/key_life_events.md`：重要事件
- `resource/relationship_dynamics.md`：人际关系
- `resource/speech_patterns.md`：说话模式

### 人格生成器

使用 [GalgameCharacterSkills](https://github.com/Langzaigg/GalgameCharacterSkills) 生成器可以快速创建高质量的 Skill 人格。

## 指令说明

- `rg` 或 `rg list`：查看可用人格列表
- `rg set <人格名>`：切换到指定人格
- `rg reset`：重置当前会话上下文
- `rg mem`：查看记忆
- `rg mem clear <scope>`：清除记忆
- `rg model`：查看/切换模型配置
- `rg draw [force/on/auto/off]`：画图模式设置

## 工具说明

### 内置工具

- **tavily_search**：Tavily 网页搜索（主搜索工具）
- **bocha_search**：博查网页搜索（备用）
- **fetch_url**：HTTP 网页抓取
- **browse_url**：浏览器渲染抓取
- **pixiv_search**：Pixiv 图片搜索
- **memory**：记忆管理工具
- **anima_generate**：ComfyUI 画图工具

### 工具配置

在配置文件中设置相关参数：

```yaml
# 搜索工具
TAVILY_API_KEY: []
BOCHA_API_KEY: ''

# 网页抓取
WEB_FETCH_TIMEOUT: 20
WEB_FETCH_MAX_CHARS: 6000

# Pixiv 搜索
LLM_TOOL_LOLICON_CONFIG:
  proxy: null
  r18: 0

# ComfyUI 画图
COMFYUI_BASE_URL: http://127.0.0.1:8188
```

## 配置说明

### OpenAI 配置

```yaml
OPENAI_PROFILES:
  default:
    api_keys:
      - sk-xxx
    base_url: https://api.openai.com/v1
    proxy: ''
    timeout: 60
    model: gpt-4o
    model_mini: gpt-4o-mini
    temperature: 0.4
    max_tokens: 1024
    multimodal: true
```

### 上下文管理

```yaml
CONTEXT_TOKEN_BUDGET: 4096      # 上下文 token 预算
CONTEXT_WINDOW_SIZE: 16         # 上下文窗口大小
CONTEXT_SUMMARY_ENABLED: false  # 是否启用摘要压缩
```

### 多模态设置

```yaml
MULTIMODAL_ENABLE: true
MULTIMODAL_MAX_MESSAGES_WITH_IMAGES: 2
MULTIMODAL_IMAGE_FRESH_MINUTES: 120
```

## 相关项目

- [GalgameCharacterSkills](https://github.com/Langzaigg/GalgameCharacterSkills) - 人格生成器
- [ComfyUI-AnimaTool](https://github.com/Langzaigg/ComfyUI-AnimaTool) - ComfyUI 画图工具

## 许可证

MIT License
