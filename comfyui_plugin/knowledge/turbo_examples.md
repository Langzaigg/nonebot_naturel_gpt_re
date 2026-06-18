# Turbo Prompt JSON 示例

> Turbo 模式使用英文自然语言描述 tags，不要用逗号分隔的 Danbooru 标签。

## 1) 单角色竖构图，已知角色半身

```json
{
  "aspect_ratio": "2:3",
  "quality_meta_year_safe": "masterpiece, best quality, highres, newest, year 2025, sensitive",
  "count": "1girl",
  "character": "shiroko (blue archive)",
  "series": "blue archive",
  "tags": "Shiroko with medium-length silver hair and bright blue eyes is sitting on a classroom desk, wearing a white sailor uniform with a blue scarf, her wolf ears perked up attentively. She is looking at the viewer with a gentle smile, one hand resting on the desk. The composition is an upper body shot from the front. Soft warm sunlight streams through the window behind her, creating a cozy atmosphere with gentle lens flare.",
  "neg": "worst quality, low quality, score_1, score_2, score_3, blurry, jpeg artifacts, bad anatomy, bad hands, bad feet, extra fingers, missing fingers, extra toes, text, watermark, logo, nsfw, explicit"
}
```

## 2) 双角色 1:1，已知角色

```json
{
  "aspect_ratio": "1:1",
  "quality_meta_year_safe": "masterpiece, best quality, highres, newest, year 2025, sensitive",
  "count": "2girls",
  "character": "shiroko (blue archive), serika (blue archive)",
  "series": "blue archive",
  "tags": "Two girls are sitting together on a classroom bench, looking at the viewer with friendly smiles. Shiroko has medium-length silver hair and blue eyes with wolf ears, wearing a white sailor uniform with a blue scarf. Serika has long black hair tied in a low ponytail and red eyes with cat ears, wearing a black sailor uniform with a blue ribbon. They are leaning slightly towards each other, showing their close friendship. The composition is an upper body shot from the front. Soft warm sunlight streams through the classroom window, creating a cozy atmosphere with gentle shadows on the wall.",
  "neg": "worst quality, low quality, score_1, score_2, score_3, blurry, jpeg artifacts, bad anatomy, bad hands, bad feet, extra fingers, missing fingers, extra toes, text, watermark, logo, nsfw, explicit"
}
```

## 3) 原创角色纯自然语言，双角色

```json
{
  "aspect_ratio": "3:2",
  "quality_meta_year_safe": "masterpiece, best quality, highres, newest, year 2025, safe",
  "count": "2girls",
  "character": "",
  "series": "",
  "artist": "@makihitsuji",
  "tags": "Two girls stand side by side in an ancient forest clearing. The beastgirl warrior has short crimson red hair and amber golden eyes, with large wolf ears on top of her head, wearing dark leather armor with fur trim and heavy boots, wielding a large battle axe over her shoulder with a fierce determined grin. The elven mage has long silver-white hair flowing down her back and bright emerald green eyes with pointed ears, wearing an elegant blue and white robe with glowing magical runes and pointed shoes, holding a crystal staff with both hands and a calm serene smile. The composition is a full body shot from a slightly elevated angle. Dappled sunlight filters through the ancient tree canopy, creating a magical atmosphere with floating golden particles and gentle morning mist.",
  "neg": "worst quality, low quality, score_1, score_2, score_3, blurry, jpeg artifacts, bad anatomy, bad hands, bad feet, extra fingers, missing fingers, extra toes, text, watermark, logo, nsfw, explicit"
}
```
