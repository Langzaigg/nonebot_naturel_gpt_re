from typing import Awaitable, Callable, Optional, Tuple
from nonebot import get_driver
from .logger import logger
from nonebot.matcher import Matcher
from nonebot.adapters import Bot, Event

from .config import *
from . import utils

global_config = get_driver().config
# logger.info(config) # 这里可以打印出配置文件的内容

from .openai_func import TextGenerator
from .persistent_data_manager import PersistentDataManager
from .chat_manager import ChatManager
from . import matcher
from . import matcher_MCRcon # noqa: F401
from .llm_tool_plugins import init_tools


def set_permission_check_func(callback:Callable[[Matcher, Event, Bot, str, str], Awaitable[Tuple[bool,Optional[str]]]]):
    """设置Matcher的权限检查函数"""
    matcher.permission_check_func = callback

# 设置默认权限检查函数，有需求时可以覆盖
set_permission_check_func(utils.default_permission_check_func)

""" ======== 读取历史记忆数据 ======== """
PersistentDataManager.instance.load_from_file()
ChatManager.instance.create_all_chat_object() # 启动时创建所有的已有Chat对象，以便被 -all 相关指令控制

# 条件加载工具（如博查搜索需配置 key 才注册）
init_tools(config)

# Anima 画图持久化恢复：若上次退出时开启，启动时尝试连接并注册；失败则自动关闭
if config.COMFYUI_ENABLED:
    from .llm_tool_plugins import anima_generate, enable_anima_tool
    ok, err = anima_generate.health_check_sync()
    if ok:
        ok2, err2 = anima_generate.fetch_schema_and_knowledge_sync()
        if ok2:
            if enable_anima_tool():
                logger.info("Anima 画图工具已从持久化状态恢复")
            else:
                logger.warning("Anima 画图 schema 已缓存但注册跳过（可能重复）")
        else:
            logger.warning(f"Anima 画图知识库加载失败，自动关闭: {err2}")
            config.COMFYUI_ENABLED = False
            save_config()
    else:
        logger.warning(f"Anima 画图服务离线，自动关闭: {err}")
        config.COMFYUI_ENABLED = False
        save_config()

# 读取 OpenAI 配置（优先使用 OPENAI_PROFILES 中的 active profile）
_profiles = config.OPENAI_PROFILES
_active = config.OPENAI_ACTIVE_PROFILE
if _profiles:
    if _active not in _profiles:
        _active = next(iter(_profiles))
    _profile = _profiles[_active]
    api_keys = _profile.get("api_keys", config.OPENAI_API_KEYS)
    _init_config = {
        'model': _profile.get("model", config.CHAT_MODEL),
        'model_mini': _profile.get("model_mini", config.CHAT_MODEL_MINI),
        'max_tokens': _profile.get("max_tokens", config.REPLY_MAX_TOKENS),
        'temperature': _profile.get("temperature", config.CHAT_TEMPERATURE),
        'top_p': _profile.get("top_p", config.CHAT_TOP_P),
        'frequency_penalty': _profile.get("frequency_penalty", config.CHAT_FREQUENCY_PENALTY),
        'presence_penalty': _profile.get("presence_penalty", config.CHAT_PRESENCE_PENALTY),
        'max_summary_tokens': _profile.get("max_summary_tokens", config.CHAT_MAX_SUMMARY_TOKENS),
        'timeout': _profile.get("timeout", config.OPENAI_TIMEOUT),
        'enable_stream': config.LLM_ENABLE_STREAM,
    }
    _init_proxy = _profile.get("proxy") or None
    _init_base_url = _profile.get("base_url", "")
    _init_use_socket_proxy = _profile.get("use_socket_proxy", False)
    _init_multimodal = _profile.get("multimodal", True)
    logger.info(f"使用 OpenAI 配置: {_active}")
else:
    api_keys = config.OPENAI_API_KEYS
    _init_config = {
        'model': config.CHAT_MODEL,
        'model_mini': config.CHAT_MODEL_MINI,
        'max_tokens': config.REPLY_MAX_TOKENS,
        'temperature': config.CHAT_TEMPERATURE,
        'top_p': config.CHAT_TOP_P,
        'frequency_penalty': config.CHAT_FREQUENCY_PENALTY,
        'presence_penalty': config.CHAT_PRESENCE_PENALTY,
        'max_summary_tokens': config.CHAT_MAX_SUMMARY_TOKENS,
        'timeout': config.OPENAI_TIMEOUT,
        'enable_stream': config.LLM_ENABLE_STREAM,
    }
    _init_proxy = config.OPENAI_PROXY_SERVER if config.OPENAI_PROXY_SERVER else None
    _init_base_url = config.OPENAI_BASE_URL if config.OPENAI_BASE_URL else ''

logger.info(f"共读取到 {len(api_keys)} 个API Key")

""" ======== 初始化对话文本生成器 ======== """
TextGenerator.instance.init(api_keys=api_keys, config=_init_config, proxy=_init_proxy, base_url=_init_base_url)
TextGenerator.instance.use_socket_proxy = _init_use_socket_proxy if _profiles else False
TextGenerator.instance.multimodal = _init_multimodal if _profiles else True


