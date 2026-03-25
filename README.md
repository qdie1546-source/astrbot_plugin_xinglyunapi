 自定义API管理插件说明 

# 自定义API管理插件（XingYun API Manager） v2.2.2

## 1\. 插件简介

__插件名称：__自定义API管理

__版本：__v2.2.2

__开发者：__星落云

__项目链接：__[GitHub 仓库](https://github.com/qdie1546-source/astrbot_plugin_xinglyunapi.git)

该插件用于在 AstrBot 中灵活管理自定义 API，支持多 API、多参数接口、JSON路径解析、自动识别媒体类型、调试接口以及防刷冷却机制。

## 2\. 功能说明

### 2.1 多 API 管理

*   所有 API 配置集中在 JSON 编辑器中管理
*   支持无限添加 API
*   支持多参数接口
*   支持为不同 API 定义不同触发指令

### 2.2 媒体类型自动识别

*   图片：.jpg, .png, .gif, .webp
*   音频：.mp3, .wav, .aac
*   视频：.mp4, .m3u8, .flv
*   自动发送对应媒体内容，不仅仅返回链接

### 2.3 调试接口

*   使用 `/调试api` 可即时测试接口返回内容
*   支持输入参数，查看接口返回结果

### 2.4 冷却机制

*   插件内置用户冷却，防止接口被刷
*   冷却时间可在插件配置中调整（默认 3 秒）

## 3\. 安装说明

1.  在 AstrBot 后台插件市场搜索 __自定义API管理__
2.  点击 __安装__
3.  安装完成后，插件会自动生成默认 JSON 编辑器配置
4.  在插件配置中可以看到一个 __JSON 编辑器__，用于管理 API

⚠️ 目前 UI 使用单编辑器方案，不支持点击 API 切换编辑器，但可以通过分块/分隔管理多个 API。

## 4\. 配置说明

插件使用单 JSON 编辑器管理所有 API，推荐结构如下：

```
{
  "_说明": "在这里写备注或分块说明",

  "weather": {
    "name": "天气查询",
    "url": "https://cn.apihz.cn/api/weather.php",
    "method": "GET",
    "params": ["city"],
    "json_path": "data.url"
  },

  "image": {
    "name": "随机图片",
    "url": "https://cn.apihz.cn/api/img/qqtx.php",
    "method": "GET",
    "params": ["id", "key"],
    "json_path": ""
  }
}
```

### JSON 字段说明

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| 字段 | 类型 | 说明 |
| key | string | 触发指令（用户调用 /Rapi key） |
| name | string | API 显示名称 |
| url | string | 接口地址 |
| method | string | 请求方法：GET / POST |
| params | array | 参数名称数组 |
| json_path | string | 可选 JSON 路径，用于提取返回结果 |

## 5\. 使用方法

### 5.1 查看已配置 API

```
/查api
```

输出示例：

```
📡 API列表：

🔹 weather → 天气查询
🔹 image → 随机图片
```

### 5.2 调用 API

```
/Rapi weather 北京
/Rapi image 88888888 88888888
```

插件会根据 JSON 配置发送请求，并自动返回结果（图片/文本/音频/视频）。

### 5.3 调试接口

```
/调试api weather 北京
```

用于即时查看接口返回内容，不经过媒体解析。

## 6\. JSON 编辑技巧

### 6.1 分块管理 API

```
{
  "_天气类": {},
  "weather": { ... },

  "_娱乐类": {},
  "image": { ... }
}
```

这些伪字段不会被解析成 API，可用于视觉分隔。

### 6.2 避免常见问题

*   API不存在：确认 JSON 键名和触发指令一致
*   返回文本而不是图片：确认 URL 结尾标准，如 .jpg
*   请求失败：确认接口地址和参数正确
*   调用过快：冷却时间未过，等待或调整 cooldown

## 7\. 注意事项

*   插件 UI 是单编辑器方案，不支持动态点击切换 API
*   推荐使用 `_说明` 或 `_分类名` 分隔不同 API
*   JSON 配置务必合法，否则插件无法解析

## 8\. 版本更新记录

# XingYunAPI 插件更新日志 v2.2.6

## 版本号
**v2.2.6**

## 更新日期
2026-03-26

## 更新内容

### 1️⃣ 核心改动
- 修复了 API 返回图片仅显示链接的问题，现在插件会**直接发送图片内容**到聊天。
- 支持图片、音频、视频直接发送，避免用户手动点击 URL。
- 改进 URL 类型判断，支持带参数的链接（如 `.jpg?size=640`）。
- `/Rapi` 和 `/调试api` 命令支持 async generator 正确发送消息。
- JSON 路径解析逻辑保持原样，但增加了容错处理。

### 2️⃣ 主要修改文件
- `main.py`

#### 核心代码示例
```python
# 下载图片并发送
if self.is_image(url):
    try:
        async with httpx.AsyncClient(timeout=15) as client:
            resp = await client.get(url)
            resp.raise_for_status()
            tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg")
            tmp.write(resp.content)
            tmp.close()
            yield event.image_result(tmp.name)
            os.unlink(tmp.name)
            return
    except Exception as e:
        yield event.plain_result(f"图片下载失败: {e}")
        return

### v2.2.2

*   修复 async\_generator can't be used in await 问题
*   handle\_response 正确使用 async for
*   call\_api / debug\_api 均可稳定返回图片/音频/视频
*   优化 JSON 解析，支持分隔块管理多个 API

### v2.2.1

*   初步 JSON 编辑器方案
*   多 API + 多参数 + JSON路径解析
*   图片/音频/视频自动发送

### v2.1.0

*   插件初版发布
*   支持单 API 配置和触发指令

## 9\. 联系方式

开发者：__星落云__

GitHub 仓库：[astrbot\_plugin\_xinglyunapi](https://github.com/qdie1546-source/astrbot_plugin_xinglyunapi.git)