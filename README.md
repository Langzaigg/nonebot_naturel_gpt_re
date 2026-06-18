<div align="center">

# 🐰 Naturel GPT Re

**NoneBot2 群聊人格插件 + ComfyUI 画图插件 的重新整理版**

[快速开始](#快速开始) · [目录结构](#目录结构) · [nonebot 插件](#nonebot插件) · [comfyui 插件](#comfyui插件)

</div>

---

本仓库重新整理并维护了基于 `nonebot_plugin_naturel_gpt` 的 QQ 群聊人格聊天插件，以及配套使用的 `ComfyUI-AnimaTool` 画图插件。

两个插件可以独立使用，也可以组合成完整的"群聊 AI + 主动画图"工作流。

| 子项目 | 路径 | 说明 |
|--------|------|------|
| **Naturel GPT 插件** | `nonebot_plugin_naturel_gpt/` | NoneBot2 群聊人格对话插件，支持流式响应、多模态图片、工具调用、人格热加载 |
| **AnimaTool 画图插件** | `comfyui_plugin/` | ComfyUI 自定义节点，通过 MCP / HTTP API 让 AI Agent 直接生成二次元图片 |
| **公共配置** | `config/` | 人格文件、主配置文件示例 |

---

## 快速开始

### 1. 安装依赖

```bash
pip install httpx tiktoken playwright
playwright install chromium  # 可选，用于 browse_url 工具
```

ComfyUI 画图插件依赖见其 [`comfyui_plugin/README.md`](comfyui_plugin/README.md)。

### 2. 配置文件

复制 `config/naturel_gpt_config.yml.example` 为 `config/naturel_gpt_config.yml`，填入你的配置：

```yaml
OPENAI_PROFILES:
  default:
    api_keys:
      - sk-your-api-key-here
    base_url: https://api.openai.com/v1
    model: gpt-4o
```

更多配置项见 [`nonebot_plugin_naturel_gpt/README.md`](nonebot_plugin_naturel_gpt/README.md)。

### 3. 配置人格

将人格文件放入 `config/personas/`：

- **简易人格**：创建 `.md` 文件，文件名即人格名
- **Skill 人格**：创建文件夹，格式为 `人格名-skill-main/`

### 4. 启动

```bash
nb run
```

---

## 目录结构

```text
.
├── nonebot_plugin_naturel_gpt/   # QQ 群聊人格插件
│   ├── matcher.py                 # 消息匹配与处理
│   ├── chat.py                    # 会话管理
│   ├── chat_history.py            # 对话历史
│   ├── chat_prompt.py             # Prompt 构造
│   ├── chat_summary.py            # 上下文摘要
│   ├── openai_func.py             # LLM 调用
│   ├── llm_tool_plugins/          # 工具插件目录
│   └── ...
├── comfyui_plugin/               # ComfyUI 画图插件
│   ├── executor/                  # 核心执行器
│   ├── servers/                   # MCP / HTTP 服务
│   ├── knowledge/                 # 专家知识库
│   └── ...
├── config/                       # 配置与人格
│   ├── naturel_gpt_config.yml     # 主配置文件
│   └── personas/                  # 人格目录
└── README.md                       # 本文件
```

---

## nonebot 插件

基于 NoneBot2 + OneBot v11 的群聊人格聊天插件，支持：

- 流式响应与分段发送
- 多模态图片输入
- 原生工具调用（搜索、网页抓取、Pixiv、Bangumi 等）
- 动态人格加载（`.md` 单文件 / `skill` 文件夹）
- 智能上下文压缩与摘要
- 用户印象与群记忆
- 多 OpenAI 配置切换

详细文档：[nonebot_plugin_naturel_gpt/README.md](nonebot_plugin_naturel_gpt/README.md)

---

## comfyui 插件

ComfyUI 自定义节点，提供 Anima 模型的二次元图片生成能力。

- 支持 MCP Server（Cursor / Claude 等原生显示图片）
- 支持 ComfyUI 内置 HTTP API
- 支持批量生成、reroll、历史记录
- 提供 14 种长宽比预设

详细文档：[comfyui_plugin/README.md](comfyui_plugin/README.md)

---

## 相关项目

- [GalgameCharacterSkills](https://github.com/Langzaigg/GalgameCharacterSkills) - 人格生成器
- [ComfyUI-AnimaTool 原版](https://github.com/Moeblack/ComfyUI-AnimaTool) - ComfyUI 画图工具原版
- [AnimaLoraToolkit](https://github.com/Moeblack/AnimaLoraToolkit) - Anima LoRA / LoKr 训练工具

---

## 许可证

- `nonebot_plugin_naturel_gpt/`：MIT License
- `comfyui_plugin/`：AGPL-3.0 License
