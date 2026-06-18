<div align="center">

# 🎨 ComfyUI-AnimaTool

**ComfyUI 二次元图片生成插件**

让 AI Agent 通过 MCP 或 HTTP API 直接调用 ComfyUI 生成图片，原生显示在聊天窗口中。

[安装](#安装) · [使用方法](#使用方法) · [参数说明](#参数说明) · [故障排查](#故障排查)

</div>

---

> 本目录是 [Naturel GPT Re](../README.md) 仓库的 ComfyUI 画图组件，也可独立部署到 `ComfyUI/custom_nodes/` 中使用。

<p align="center">
  <img src="assets/hero.webp" alt="ComfyUI-AnimaTool Demo" width="100%">
</p>

<p align="center">
  <b>Cursor / Claude / Gemini / OpenAI → MCP / HTTP API → ComfyUI → Anima 模型</b>
</p>

---

## 功能特性

| 特性 | 说明 |
|------|------|
| **MCP Server** | 图片原生显示在 Cursor / Claude 等支持 MCP 的客户端聊天窗口 |
| **HTTP API** | 随 ComfyUI 启动自动注册，无需额外服务 |
| **结构化提示词** | 按 Anima 规范自动拼接质量、画师、标签、角色、环境等字段 |
| **多比例预设** | 支持 21:9 到 9:21 共 14 种长宽比 |
| **批量生成** | `repeat` 提交多次独立任务，`batch_size` 在单任务内生成多张 |
| **Reroll / 历史记录** | 基于历史记录重新生成，可覆盖部分参数（换画师、加 LoRA 等） |
| **十连抽 / 换卡池** | 支持多图连抽与 UNET / CLIP / VAE 模型切换 |

---

## 文档

- [Wiki & Prompt Guide](https://github.com/Moeblack/ComfyUI-AnimaTool/wiki) - 提示词指南、安装教程与 API 文档
- [CURSOR_SKILL.md](CURSOR_SKILL.md) - Cursor / Windsurf 用户 Skill，用于生成高质量提示词

---

## 安装

### 方式一：ComfyUI Manager（推荐）

1. 打开 ComfyUI Manager
2. 搜索 "Anima Tool"
3. 点击 Install
4. 重启 ComfyUI

### 方式二：手动安装

```bash
cd ComfyUI/custom_nodes
git clone https://github.com/Moeblack/ComfyUI-AnimaTool.git
pip install -r ComfyUI-AnimaTool/requirements.txt
```

### 依赖模型

确保以下模型文件已放置到 ComfyUI 对应目录：

| 文件 | 路径 | 说明 |
|------|------|------|
| `anima-preview.safetensors` | `models/diffusion_models/` | Anima UNET |
| `qwen_3_06b_base.safetensors` | `models/text_encoders/` | Qwen3 CLIP |
| `qwen_image_vae.safetensors` | `models/vae/` | VAE |

模型下载：[circlestone-labs/Anima on Hugging Face](https://huggingface.co/circlestone-labs/Anima)

---

## 使用方法

### 方式 0：独立 MCP（云端 / 远程 ComfyUI）

如果你不想把本仓库放进 `ComfyUI/custom_nodes/`，只想连接一台正在运行的 ComfyUI（本机或云端），可以使用独立 PyPI 包 [`comfyui-animatool`](https://github.com/Moeblack/animatool-mcp)（命令 `animatool-mcp`）。

**uvx（推荐，无需安装）**：

```json
{
  "mcpServers": {
    "anima-tool": {
      "command": "uvx",
      "args": ["--from", "comfyui-animatool", "animatool-mcp"],
      "env": {
        "COMFYUI_URL": "http://127.0.0.1:8188",
        "ANIMATOOL_CHECK_MODELS": "false"
      }
    }
  }
}
```

云端鉴权（可选）：`ANIMATOOL_BEARER_TOKEN` 或 `ANIMATOOL_HEADERS_JSON`。

> 该方式不依赖安装本 custom node，只要 `COMFYUI_URL` 可访问即可。

---

### 方式 1：MCP Server（推荐，原生图片显示）

在项目根目录创建 `.cursor/mcp.json`：

```json
{
  "mcpServers": {
    "anima-tool": {
      "command": "C:\\ComfyUI\\.venv\\Scripts\\python.exe",
      "args": ["C:\\ComfyUI\\custom_nodes\\ComfyUI-AnimaTool\\servers\\mcp_server.py"]
    }
  }
}
```

安装依赖：

```bash
pip install mcp
```

确保 ComfyUI 运行在 `http://127.0.0.1:8188`，重启 Cursor 后即可使用：

> 画一个穿白裙的少女在花园里，竖屏 9:16，safe

图片会**原生显示**在聊天窗口中。

---

### 方式 2：ComfyUI 内置 HTTP API

启动 ComfyUI 后，以下路由自动注册：

| 路由 | 方法 | 说明 |
|------|------|------|
| `/anima/health` | GET | 健康检查 |
| `/anima/schema` | GET | Tool Schema |
| `/anima/knowledge` | GET | 专家知识 |
| `/anima/generate` | POST | 执行生成（支持 `repeat` 批量） |
| `/anima/history` | GET | 查看最近生成历史 |
| `/anima/reroll` | POST | 基于历史记录重新生成 |

**curl 示例**：

```bash
curl -X POST http://127.0.0.1:8188/anima/generate \
  -H "Content-Type: application/json" \
  -d '{"aspect_ratio":"3:4","quality_meta_year_safe":"masterpiece, best quality, newest, year 2025, sensitive","count":"1girl","artist":"@rurudo","tags":"upper body, smile, white dress","neg":"worst quality, low quality, blurry, bad hands, nsfw"}'
```

---

### 方式 3：独立 FastAPI Server

```bash
cd ComfyUI-AnimaTool
pip install fastapi uvicorn
python -m servers.http_server
```

访问 `http://127.0.0.1:8000/docs` 查看 Swagger UI。

---

## 参数说明

### 必填参数

| 参数 | 类型 | 说明 |
|------|------|------|
| `quality_meta_year_safe` | string | 质量 / 年份 / 安全标签（必须包含 `safe` / `sensitive` / `nsfw` / `explicit`） |
| `count` | string | 人数（如 `1girl`, `2girls`, `1boy`） |
| `artist` | string | 画师，**必须带 `@`**，如 `@fkey, @jima` |
| `tags` | string | Danbooru 标签 |
| `neg` | string | 负面提示词 |

### 可选参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `aspect_ratio` | string | - | 长宽比（自动计算分辨率） |
| `width` / `height` | int | - | 直接指定分辨率 |
| `character` | string | `""` | 角色名 |
| `series` | string | `""` | 作品名 |
| `appearance` | string | `""` | 外观描述 |
| `style` | string | `""` | 画风 |
| `environment` | string | `""` | 环境 / 光影 |
| `steps` | int | 25 | 步数 |
| `cfg` | float | 4.5 | CFG |
| `seed` | int | 随机 | 种子 |
| `sampler_name` | string | `er_sde` | 采样器 |
| `repeat` | int | 1 | 提交几次独立生成任务（queue 模式，每次独立 seed） |
| `batch_size` | int | 1 | 单次任务内生成几张（latent batch 模式，更吃显存） |
| `loras` | array | `[]` | 追加 LoRA（仅 UNET），`name` 为 `models/loras/` 下相对路径 |

### 支持的长宽比

```text
横屏: 21:9, 2:1, 16:9, 16:10, 5:3, 3:2, 4:3
方形: 1:1
竖屏: 3:4, 2:3, 3:5, 10:16, 9:16, 1:2, 9:21
```

---

## LoRA 使用

当前版本只在 UNET 上链式注入 `LoraLoaderModelOnly`，不影响 CLIP。

1. 将 LoRA 放入 `ComfyUI/models/loras/`
2. 请求中传入 `loras` 参数，例如：

```json
{
  "loras": [
    { "name": "_Anima/cosmic_kaguya_lokr_epoch4_comfyui.safetensors", "weight": 0.9 }
  ]
}
```

为了让 MCP 的 `list_anima_models` 工具能列出 LoRA，需要存在同名 `.json` sidecar 元数据文件，并设置 `COMFYUI_MODELS_DIR` 指向 models 根目录。

> 参考：`examples/loras/_Anima/cosmic_kaguya_lokr_epoch4_comfyui.safetensors.json`

---

## 重要规则

1. **画师必须带 `@`**：如 `@fkey, @jima`，否则几乎无效
2. **必须明确安全标签**：`safe` / `sensitive` / `nsfw` / `explicit`
3. **推荐画师组合**：`@fkey, @jima`（效果稳定）
4. **分辨率约 1MP**：Anima preview 版本更稳定
5. **提示词不分行**：单行逗号连接

---

## 目录结构

```text
ComfyUI-AnimaTool/
├── __init__.py                 # ComfyUI extension（注册 /anima/* 路由）
├── executor/                   # 核心执行器
│   ├── anima_executor.py
│   ├── config.py
│   ├── history.py              # 生成历史管理器
│   └── workflow_template.json
├── knowledge/                  # 专家知识库
│   ├── anima_expert.md
│   ├── artist_list.md
│   └── prompt_examples.md
├── schemas/                    # Tool Schema
│   └── tool_schema_universal.json
├── servers/                    # 服务入口
│   ├── mcp_server.py           # MCP Server
│   ├── http_server.py          # 独立 FastAPI
│   └── cli.py                  # 命令行工具
├── assets/                     # 截图等资源
├── outputs/                    # 生成的图片（gitignore）
├── README.md
├── LICENSE
├── CHANGELOG.md
├── pyproject.toml
└── requirements.txt
```

---

## 配置

### 环境变量

| 环境变量 | 默认值 | 说明 |
|----------|--------|------|
| `COMFYUI_URL` | `http://127.0.0.1:8188` | ComfyUI 服务地址 |
| `ANIMATOOL_TIMEOUT` | `600` | 生成超时（秒） |
| `ANIMATOOL_DOWNLOAD_IMAGES` | `true` | 是否保存图片到本地 |
| `ANIMATOOL_OUTPUT_DIR` | `./outputs` | 图片输出目录 |
| `ANIMATOOL_TARGET_MP` | `1.0` | 目标像素数（MP） |
| `ANIMATOOL_ROUND_TO` | `16` | 分辨率对齐倍数 |
| `ANIMATOOL_UNET_NAME` | `anima-preview.safetensors` | UNET 模型文件名 |
| `ANIMATOOL_CLIP_NAME` | `qwen_3_06b_base.safetensors` | CLIP 模型文件名 |
| `ANIMATOOL_VAE_NAME` | `qwen_image_vae.safetensors` | VAE 模型文件名 |
| `ANIMATOOL_CHECK_MODELS` | `true` | 是否启用模型预检查 |
| `COMFYUI_MODELS_DIR` | - | ComfyUI models 目录，用于模型预检查与 LoRA sidecar 读取 |

### 远程 / Docker 配置

```bash
# 局域网其他电脑
export COMFYUI_URL=http://192.168.1.100:8188

# Docker 容器访问宿主机
export COMFYUI_URL=http://host.docker.internal:8188

# WSL 访问 Windows
export COMFYUI_URL=http://$(cat /etc/resolv.conf | grep nameserver | awk '{print $2}'):8188
```

---

## 故障排查

### 无法连接到 ComfyUI

1. 确认 ComfyUI 已启动：浏览器访问 `http://127.0.0.1:8188`
2. 确认端口正确：默认 8188，如果改过需要设置 `COMFYUI_URL`
3. 确认防火墙未阻止（Windows Defender / 企业防火墙）
4. 如果 ComfyUI 在远程 / Docker，设置正确的 `COMFYUI_URL`

### H,W should be divisible by spatial_patch_size

原因：分辨率不是 16 的倍数。

解决：使用预设的 `aspect_ratio`；如果手动指定 `width`/`height`，确保是 16 的倍数（如 512、768、1024）。

### 模型文件不存在

确认以下文件存在：

| 文件 | 位置 |
|------|------|
| `anima-preview.safetensors` | `ComfyUI/models/diffusion_models/` |
| `qwen_3_06b_base.safetensors` | `ComfyUI/models/text_encoders/` |
| `qwen_image_vae.safetensors` | `ComfyUI/models/vae/` |

下载地址：[circlestone-labs/Anima](https://huggingface.co/circlestone-labs/Anima)

### MCP Server 没加载

1. Cursor Settings → MCP → `anima-tool` 应显示绿色
2. 点击 "Show Output" 查看错误
3. Python 和脚本路径必须是**绝对路径**
4. 确认依赖：`pip install mcp`
5. 修改配置后必须重启 Cursor

### 生成超时

- 增加超时：`export ANIMATOOL_TIMEOUT=1200`
- 降低步数：`steps: 25`（默认值）
- 检查 ComfyUI 控制台是否有错误

---

## 相关项目

- [SillyTavern MCP Client](https://github.com/Moeblack/sillytavern-mcp-client) - 酒馆 MCP 客户端
- [SillyTavern Tool Use Fix](https://github.com/Moeblack/sillytavern-tooluse-fix) - 工具调用体验修复
- [AnimaLoraToolkit](https://github.com/Moeblack/AnimaLoraToolkit) - LoRA / LoKr 训练工具
- [ComfyUI-AnimaTool 原版](https://github.com/Moeblack/ComfyUI-AnimaTool)

---

## 系统要求

- **Python**: 3.10+
- **ComfyUI**: 最新版本
- **GPU**: 推荐 8GB+ 显存（Anima 模型较大）
- **依赖**：`mcp`（MCP Server）、`requests`（HTTP 请求）

---

## License

AGPL-3.0 License - see [LICENSE](LICENSE) for details.

---

<p align="center">
  <a href="../README.md">← 返回项目根目录</a>
</p>
