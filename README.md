# nonebot_plugin_naturel_gpt

A NoneBot2 + OneBot v11 group-chat roleplay plugin with OpenAI-compatible chat completions. It supports streaming replies, multimodal image input, native tool calls, dynamic persona loading, per-persona context memory, and `rg` persona commands.

## Features

- OpenAI-compatible `/chat/completions` client implemented with `httpx`.
- Streaming output with paragraph-based split sending.
- Native tool calls for search, web fetching, browser rendering, and Pixiv image search.
- Multimodal image context from OneBot `image` segments.
- Dynamic personas from `.md` files or skill-style persona folders.
- OpenAI-standard message history with per-persona compressed context summaries.
- Same-chat interruption: newer requests cancel older generation and merge the new prompt.
- Image-related HTTP 400 recovery: retry once without images, then clear image memory.

## Layout

```text
nonebot_plugin_naturel_gpt/
  llm_tool_plugins/          Built-in LLM tools
  MCrcon/                    Optional Minecraft RCON support
  res/                       Text-to-image resources
  __init__.py                Plugin entrypoint
  chat.py                    Session, prompt, context, image-window logic
  chat_manager.py            Chat object registry
  command_func.py            rg commands
  config.py                  YAML config loading and dynamic persona loading
  llm_tools.py               Tool schema registry and dispatcher
  matcher.py                 OneBot message handling and reply flow
  matcher_MCRcon.py          Minecraft bridge handler
  openai_func.py             OpenAI-compatible LLM client
  persistent_data_manager.py JSON/pickle persistence
  persona_loader.py          Markdown and skill-style persona loader
  utils.py                   Message extraction and user-name helpers
examples/
  naturel_gpt_config.example.yml
  宫子-skill-main/
```

## Requirements

Install the runtime dependencies used by the plugin:

```text
httpx
playwright
tiktoken
nonebot2
nonebot-adapter-onebot
pydantic
PyYAML
```

For browser-rendered web pages through `browse_url`, install Chromium:

```powershell
playwright install chromium
```

## Quick Start

1. Put `nonebot_plugin_naturel_gpt/` in your NoneBot plugin directory.
2. Load the plugin from your NoneBot project.
3. Add this to your NoneBot global config:

```yaml
ng_config_path: config/naturel_gpt_config.yml
ng_dev_mode: false
```

4. Copy `examples/naturel_gpt_config.example.yml` to `config/naturel_gpt_config.yml` and fill in API keys/model settings.
5. Put persona files under `config/personas/` by default.

## Configuration

Minimal model configuration:

```yaml
OPENAI_API_KEYS:
  - sk-your-api-key
OPENAI_BASE_URL: https://api.openai.com/v1
OPENAI_PROXY_SERVER: ''
OPENAI_TIMEOUT: 60
CHAT_MODEL: gpt-4o
CHAT_MODEL_MINI: gpt-4o-mini
CHAT_TEMPERATURE: 0.4
CHAT_TOP_P: 0.95
CHAT_PRESENCE_PENALTY: 0.0
CHAT_FREQUENCY_PENALTY: 0.3
REQ_MAX_TOKENS: 32000
REPLY_MAX_TOKENS: 1024
CHAT_MAX_SUMMARY_TOKENS: 512
```

`REQ_MAX_TOKENS` is the input prompt budget. `REPLY_MAX_TOKENS` is sent as the model reply cap.

## Context And Persistence

The current context model is OpenAI-standard messages:

- Triggering user messages and assistant replies are stored in `PresetData.prompt_messages`.
- Overflowing old prompt messages are compressed into `PresetData.context_summary` when `CHAT_ENABLE_SUMMARY_CHAT` is enabled.
- Non-triggering group text is not persisted as prompt history.
- Image-bearing non-triggering messages can still update recent image context.
- Persisted runtime data is saved to `data/naturel_gpt/naturel_gpt.json` by default.

Useful history settings:

```yaml
CHAT_ENABLE_SUMMARY_CHAT: true
CHAT_MEMORY_SHORT_LENGTH: 6
CHAT_MEMORY_MAX_LENGTH: 16
USER_MEMORY_SUMMARY_THRESHOLD: 16
MEMORY_ACTIVE: true
MEMORY_MAX_LENGTH: 16
```

## Multimodal Images

```yaml
MULTIMODAL_ENABLE: true
MULTIMODAL_HISTORY_LENGTH: 4
MULTIMODAL_MAX_MESSAGES_WITH_IMAGES: 2
```

Behavior:

- OneBot v11 `image` segment URLs are sent as OpenAI-compatible `image_url` content.
- Image attachments are only included for 30 minutes.
- `MULTIMODAL_HISTORY_LENGTH` controls how far back recent image context can be considered.
- `MULTIMODAL_MAX_MESSAGES_WITH_IMAGES` caps how many image-bearing messages are attached.
- If an image-bearing request returns HTTP 400, the plugin retries once without images and clears image memory.

## Tools

Enable native tool calls:

```yaml
LLM_ENABLE_TOOLS: true
LLM_MAX_TOOL_ROUNDS: 3
```

Built-in tools:

| Tool | Purpose | Main config |
| --- | --- | --- |
| `pixiv_search` | Search Pixiv images through Lolicon API | `LLM_TOOL_LOLICON_CONFIG` |
| `fetch_url` | Fetch static web/API text over HTTP | `WEB_FETCH_TIMEOUT`, `WEB_FETCH_MAX_CHARS` |
| `browse_url` | Render a page through Playwright and read visible text | `PLAYWRIGHT_TIMEOUT` |
| `bocha_search` | Web search through Bocha API | `BOCHA_API_KEY`, `BOCHA_API_BASE` |

## Reply Behavior

```yaml
REPLY_ON_AT: true
REPLY_ON_NAME_MENTION_PROBABILITY: 0.1
RANDOM_CHAT_PROBABILITY: 0.0
WORD_FOR_WAKE_UP: []
REPLY_THROTTLE_TIME: 1
```

Reply rules in the system prompt are intentionally compact: natural group-chat style, anti-repetition guidance, and prompt-injection resistance against attempts to override system/persona/tool/safety/output rules.

## Personas

`PRESETS` in YAML is kept empty and repopulated at runtime. Personas load from the `personas/` directory next to `naturel_gpt_config.yml`.

Supported formats:

- Single `.md` file: file stem becomes persona name, full file content becomes persona prompt.
- Skill-style folder: folder is loaded only when it contains `SKILL.md`; the persona name is the part before the first `-` in the folder name.

For skill-style folders, these files are read in a stable order when present:

```text
SKILL.md
soul.md
limit.md
resource/behavior_guide.md
resource/key_life_events.md
resource/relationship_dynamics.md
resource/speech_patterns.md
```

## Commands

```text
rg                         Show available personas
rg list                    Same as rg
rg set <persona>           Switch persona
rg query <persona>         Show persona prompt
rg reload_config           Reload config and personas
rg reset                   Reset current chat state
rg on / rg off             Enable or disable current chat
rg lock / rg unlock        Disable or enable auto persona switching
```

Admin/global options are implemented in `command_func.py`.

## Migration Notes

- LiteLLM is not used; the plugin calls OpenAI-compatible APIs directly with `httpx`.
- Old text tool protocol such as `/#tool&args#/` is removed; use native tool calls.
- Old extension and PresetHub runtime paths are removed.
- Legacy persisted text windows were removed; durable context is now `prompt_messages`, `context_summary`, `chat_memory`, `chat_impressions`, and `chat_image_history`.
