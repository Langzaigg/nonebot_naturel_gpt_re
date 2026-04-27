from typing import Any, Dict, List, Tuple

from .common import clean_text

schema = {
    "type": "function",
    "function": {
        "name": "remember",
        "description": "在对话中自然地记住重要信息。根据信息类型选择合适的scope：关于用户个人的信息（如名字、偏好、习惯）用user，关于群的信息（如群规、群内话题、共同事项）用group。不要告诉用户你在记住什么，也不要主动询问用户想让你记住什么。",
        "parameters": {
            "type": "object",
            "properties": {
                "scope": {"type": "string", "enum": ["group", "user"], "description": "记忆范围：group=群记忆（所有人共享），user=用户记忆（仅对该用户有效）"},
                "key": {"type": "string", "description": "记忆的名称，如'用户名'、'喜欢的颜色'、'群规'"},
                "value": {"type": "string", "description": "记忆的内容，为空则删除该记忆"},
            },
            "required": ["scope", "key"],
        },
    },
}


async def run(args: Dict[str, Any], config) -> Tuple[str, List[Dict[str, Any]]]:
    scope = str(args.get("scope") or "group").strip()
    key = str(args.get("key") or "").strip()
    value = str(args.get("value") or "").strip()

    if not key:
        return "请提供要记住的内容名称。", []

    # 获取当前会话
    from ..openai_func import TextGenerator
    from ..persistent_data_manager import PersistentDataManager
    from ..chat_manager import ChatManager

    tg = TextGenerator.instance
    chat_key = tg._current_chat_key
    trigger_userid = tg._current_trigger_userid

    if not chat_key:
        return "无法获取当前会话信息。", []

    chat = ChatManager.instance.get_or_create_chat(chat_key=chat_key)
    preset = chat.chat_preset

    if scope == "user":
        # 用户个人记忆
        if not trigger_userid:
            return "无法获取用户信息。", []
        
        if trigger_userid not in preset.user_memories:
            preset.user_memories[trigger_userid] = {}
        user_memory = preset.user_memories[trigger_userid]
        
        if not value:
            if key in user_memory:
                del user_memory[key]
                return f"已忘记你的「{key}」。", []
            else:
                return f"没有关于你的「{key}」的记忆。", []
        
        if key in user_memory:
            del user_memory[key]
        user_memory[key] = value
        
        # 检查限制
        if len(user_memory) > config.MEMORY_MAX_LENGTH:
            oldest_key = next(iter(user_memory))
            del user_memory[oldest_key]
        
        return f"已记住你的「{key}」。", []
    
    else:
        # 群记忆
        if not value:
            if key in preset.chat_memory:
                del preset.chat_memory[key]
                return f"已忘记「{key}」。", []
            else:
                return f"没有关于「{key}」的记忆。", []
        
        if key in preset.chat_memory:
            del preset.chat_memory[key]
        preset.chat_memory[key] = value
        
        # 检查限制
        if len(preset.chat_memory) > config.MEMORY_MAX_LENGTH:
            important_keywords = {"重要", "关键", "记住", "名字", "身份", "偏好"}
            memory_items = list(preset.chat_memory.items())
            for del_key, del_value in memory_items:
                if not any(kw in del_value for kw in important_keywords):
                    del preset.chat_memory[del_key]
                    break
        
        return f"已记住「{key}」。", []
