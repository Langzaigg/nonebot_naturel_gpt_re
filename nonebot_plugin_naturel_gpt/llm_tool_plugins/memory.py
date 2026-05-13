from typing import Any, Dict, List, Tuple

from .common import clean_text

schema = {
    "type": "function",
    "function": {
        "name": "remember",
        "description": (
            "记忆工具，用于主动保存和删除对话中的重要信息。"
            "你应该积极使用此工具，不要等到用户明确要求才记录。"
            "当对话中出现以下情况时应立即调用：用户提到自己的名字、称呼、偏好、习惯、生日等个人信息；"
            "群内讨论的规则、约定、重要决定、共同话题；任何你觉得以后会用到的关键信息。宁可多记不可遗漏。"
            "scope 选择：个人信息用 user，群信息用 group。"
            "当记忆接近上限时，系统会要求你整理记忆：将现有记忆合并、去重、精简后通过 memories 参数整体提交，控制在上限一半以内。"
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "action": {
                    "type": "string",
                    "enum": ["save", "delete"],
                    "description": "操作类型：save=保存记忆，delete=删除指定记忆"
                },
                "scope": {
                    "type": "string",
                    "enum": ["group", "user"],
                    "description": "记忆范围：group=群记忆（所有人共享），user=用户记忆（仅对该用户有效）"
                },
                "key": {
                    "type": "string",
                    "description": "（save/delete）记忆的名称，如'用户名'、'喜欢的颜色'、'群规'"
                },
                "value": {
                    "type": "string",
                    "description": "（save）记忆的内容"
                },
                "memories": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "key": {"type": "string"},
                            "value": {"type": "string"}
                        },
                        "required": ["key", "value"]
                    },
                    "description": "（save 整理模式）整理后的完整记忆列表。接近上限时使用，传入此参数将替换该 scope 下全部记忆"
                }
            },
            "required": ["action", "scope"],
        },
    },
}


def _get_memories(preset, scope: str, trigger_userid: str = None) -> Dict[str, str]:
    """获取指定 scope 的记忆字典。"""
    if scope == "user":
        if not trigger_userid:
            return {}
        return preset.user_memories.get(trigger_userid, {})
    return preset.chat_memory


def _set_memories(preset, scope: str, memories: Dict[str, str], trigger_userid: str = None) -> None:
    """设置指定 scope 的记忆字典。"""
    if scope == "user":
        if not trigger_userid:
            return
        preset.user_memories[trigger_userid] = memories
    else:
        preset.chat_memory.clear()
        preset.chat_memory.update(memories)


async def run(args: Dict[str, Any], config) -> Tuple[str, List[Dict[str, Any]]]:
    action = str(args.get("action") or "save").strip()
    scope = str(args.get("scope") or "group").strip()
    key = str(args.get("key") or "").strip()
    value = str(args.get("value") or "").strip()
    memories_raw = args.get("memories") or []

    from ..openai_func import TextGenerator
    from ..chat_manager import ChatManager

    tg = TextGenerator.instance
    chat_key = tg._current_chat_key
    trigger_userid = tg._current_trigger_userid

    if not chat_key:
        return "无法获取当前会话信息。", []

    chat = ChatManager.instance.get_or_create_chat(chat_key=chat_key)
    preset = chat.chat_preset
    max_len = config.MEMORY_MAX_LENGTH
    target = max_len // 2
    scope_label = "你的" if scope == "user" else ""

    # ── delete ──
    if action == "delete":
        if not key:
            return "请提供要删除的记忆名称。", []
        mem = _get_memories(preset, scope, trigger_userid)
        if key in mem:
            del mem[key]
            return f"已删除{scope_label}记忆「{key}」。", []
        return f"{scope_label}记忆中没有「{key}」。", []

    # ── save（含整理模式） ──
    mem = _get_memories(preset, scope, trigger_userid)

    # 整理模式：传入 memories 参数，整体替换
    if memories_raw:
        new_memories: Dict[str, str] = {}
        for item in memories_raw:
            k = str(item.get("key", "")).strip()
            v = str(item.get("value", "")).strip()
            if k and v:
                new_memories[k] = v
        if len(new_memories) > target:
            return f"整理后的记忆数量（{len(new_memories)}）超过了上限一半（{target}），请进一步精简后重试。", []
        _set_memories(preset, scope, new_memories, trigger_userid)
        return f"{scope_label}记忆已整理完成，当前共 {len(new_memories)} 条记忆。", []

    # 普通保存
    if not key:
        return "请提供记忆名称（key）。", []

    is_update = key in mem
    mem[key] = value

    result = f"已{'更新' if is_update else '记住'}{scope_label}记忆：「{key}」=「{value}」"

    # 接近上限时要求整理，给出当前记忆列表供 LLM 精简后重新提交
    current_count = len(mem)
    if current_count >= max_len * 4 // 5:
        current_list = [{"key": k, "value": v} for k, v in mem.items()]
        result += (
            f"\n⚠️ 当前{scope_label}记忆已有 {current_count}/{max_len} 条，即将达到上限。"
            f"请立即将全部记忆合并、去重、精简后通过 memories 参数重新提交，控制在 {target} 条以内。"
            f"\n当前记忆列表：{current_list}"
        )

    return result, []
