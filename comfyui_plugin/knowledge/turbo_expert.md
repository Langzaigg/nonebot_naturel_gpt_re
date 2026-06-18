# Anima Turbo 提示词规范

## 核心规则

1. **tags 字段使用英文自然语言**：不要用逗号分隔的 Danbooru 标签，直接用完整的英文句子描述场景。

2. **自然语言要充分**：tags 至少写 3-5 句话，描述清楚角色外观、动作、构图、氛围。过短的描述会产生意外结果。

3. **安全标签必须明确**：`safe / sensitive / nsfw / explicit` 必须在 quality_meta_year_safe 中明确出现。

4. **画师标签必须以 @ 开头**（如 `@wlop`），仅在用户明确要求时添加，否则留空。

5. **默认不追求写实**：除非用户明确要求。

## tags 字段写法要点

tags 是唯一的主体内容字段，必须承担起描述画面所有细节的责任。写法要求：

### 必须包含的信息（缺一不可）

1. **角色外观**：发色、发型、瞳色、服装（从上到下：头饰→发型→眼睛→上衣→下装→鞋袜→饰品）
2. **动作/姿势**：站立、坐着、奔跑、回头、伸懒腰等
3. **表情**：微笑、严肃、惊讶、害羞等
4. **构图**：全身 / 半身 / 特写 / 远景，视角（正面/侧面/俯视/仰视）

### 建议包含的信息

5. **画面氛围**：温暖、梦幻、阴暗、明亮等
6. **光影方向**：逆光、侧光、顶光等
7. **画面风格关键词**：anime illustration, vibrant colors, soft shading 等（如果用户没指定 artist，可以在这里补充风格）

### 写法示例

**❌ 差的写法（太短、缺乏细节）：**
> a girl standing in a field

**✅ 好的写法（外观+动作+表情+构图+氛围）：**
> A girl with long flowing silver hair and bright blue eyes is standing in a vast sunflower field, wearing a white summer dress with lace trim and straw sandals. She is smiling gently at the viewer with a soft expression. The composition is a full body shot from a slightly low angle. The atmosphere is warm and dreamy with soft golden light.

**✅ 好的写法（多角色）：**
> Two girls are standing side by side under a cherry blossom tree. The girl on the left has short crimson red hair and amber eyes, wearing dark leather armor with a fur-lined cape and heavy boots, holding a large battle axe over her shoulder with a confident grin. The girl on the right has long flowing silver-white hair and emerald green eyes, wearing an elegant blue and white robe with glowing runes and pointed shoes, holding a crystal staff with both hands and a serene expression.

## 多角色场景

当画面有多个人物时，tags 中必须明确描述每个角色的外观归属，避免混淆。

### 关键原则

- **每个角色必须描述**：发色、发型、瞳色、服装至少四项
- **使用共处式描述**，不要用位置分割词把画面切成两半
  - ❌ "On the left... On the right..."
  - ✅ "Two girls stand side by side... The warrior has... Beside her, the mage has..."
- **character 字段**：多个角色名用逗号分隔，如 `"shiroko (blue archive), serika (blue archive)"`
- **角色与外观的对应关系必须在 tags 中明确**：用 "The girl with [特征] wears [服装]" 的句式

### 多角色范例

**三角色（已知角色）：**
```json
{
  "quality_meta_year_safe": "masterpiece, best quality, highres, newest, year 2025, sensitive",
  "count": "3girls",
  "character": "hatsune miku (vocaloid), kagamine rin (vocaloid), kagamine len (vocaloid)",
  "series": "vocaloid",
  "artist": "",
  "tags": "Three singers are performing together on a concert stage, singing into headset microphones with energetic expressions. Hatsune Miku has long aqua twintails and aqua eyes, wearing a teal sleeveless dress with black thighhighs and futuristic accessories. Kagamine Rin has short blonde hair with a white bow and blue eyes, wearing an orange sleeveless top with white shorts. Kagamine Len has short blonde hair and blue eyes, wearing a white button-up shirt with black shorts and a yellow necktie. The composition is a wide shot showing all three on stage. Colorful stage lights illuminate them against a dark background with vibrant light beams.",
  "neg": "worst quality, low quality, score_1, score_2, score_3, blurry, jpeg artifacts, bad anatomy, bad hands, bad feet, extra fingers, missing fingers, extra toes, text, watermark, logo"
}
```

## 安全标签与负面提示词

- 安全标签为 `safe` 或 `sensitive` 时，负面需要追加：`nsfw, explicit`
- 安全标签为 `nsfw` 或 `explicit` 时，负面需要追加：`safe, sensitive`，并且加入无码相关的反咒：`uncensored, mosaic censoring, pixel censoring, bar censoring`（避免生成时出现不自然的遮挡）

## 宽高比

仅支持 3 种比例（默认 1:1）：
- `1:1` — 正方形，适合头像、半身、插画
- `3:2` — 横构图，适合场景、全身横版
- `2:3` — 竖构图，适合全身竖版、角色立绘
