# XingYunAPI 插件文档 & 更新日志

## 开源声明 / Open Source Notice
本插件自定义API管理为开源项目，遵循 **MIT License**，欢迎在 GitHub 使用、修改和分发。

This plugin "XingYunAPI Custom API Management" is open source under the **MIT License**. You are welcome to use, modify, and distribute it on GitHub.

## 插件简介 / Plugin Overview
*   插件名称 / Plugin Name: 自定义API管理 / Custom API Management
*   开发者 / Author: 星落云 / XingLuoYun
*   版本 / Version: v2.3.1
*   项目链接 / GitHub: [点击访问](https://github.com/qdie1546-source/astrbot_plugin_xinglyunapi.git)
*   功能 / Features: 管理自定义 API，多参数接口调用，自动识别图片/音频/视频并发送 / Manage custom APIs, multiple parameters, automatically send images/audio/video

## 安装说明 / Installation
*   在 AstrBot 后台插件市场搜索 "自定义API管理" / Search "Custom API Management" in AstrBot Plugin Market
*   点击安装 / Click Install
*   插件配置可在 `_conf_schema.json` 中管理 API / Manage APIs in `_conf_schema.json`

## JSON 配置示例 / JSON Configuration Example
```
{
  "_说明": "示例：QQ头像查询API / Example: QQ Avatar API",
  "qq_avatar": {
    "name": "QQ头像查询 / QQ Avatar",
    "url": "https://uapis.cn/api/v1/social/qq/userinfo",
    "method": "GET",
    "params": ["qq"],
    "json_path": "avatar_url",
    "description": "插件自动提取 avatar_url 并发送图片 / Auto extract avatar_url and send image"
  }
}
```

## 使用方法 / Usage
*   `/查api` - 查看已配置 API 列表 / List all configured APIs
*   `/Rapi <指令> [参数...]` - 调用 API 并直接返回结果，图片直接显示 / Call API and return result, images displayed directly
*   `/调试api <指令> [参数...]` - 调试 API 调用 / Debug API call
*   默认用户调用冷却时间为 3 秒 / Default cooldown 3s, configurable in `_conf_schema.json`

## 插件逻辑关键点 / Key Implementation Points
### 安全解析命令 / Safe Command Parsing
```
parts = event.message_str.strip().split(maxsplit=2)
if len(parts) < 2:
    yield event.plain_result("用法：/Rapi 指令 参数 / Usage: /Rapi key args")
    return

trigger = parts[1].lower()
args = parts[2].split() if len(parts) == 3 else []
```

### 图片直接发送 / Direct Image Send
```
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
```

### 音频和视频发送 / Audio and Video
```
if self.is_audio(url):
    yield event.record_result(url, type="url")
    return

if self.is_video(url):
    yield event.video_result(url, type="url")
    return
```

## 更新记录 / Changelog


## v2.3.1（2026-03-26）

### 🔥 UI重构版
- 改为JSON编辑器管理API
- 修复UI无法点击问题
- 新增 /查api 指令
- 优化图片识别逻辑
- 支持Base64图片发送
- 修复返回链接不显示图片问题
- 修复JSON解析异常问题

---

## v2.3.0
- API架构重构
- 支持媒体自动识别
- 支持参数替换

### v2.2.8 (2026-03-26)
*   修复 `/Rapi` 和 `/调试api` 可能触发 `list index out of range` 的问题 / Fix list index out of range issue
*   图片 API 调用现在能直接显示图片，而不是只显示链接 / Image API now sends direct image
*   保留冷却时间、JSON 路径解析、API列表等功能 / Keep cooldown, JSON path extraction, API list
*   音频和视频可通过 URL 发送 / Audio/Video can be sent via URL

### v2.2.2
*   完善 API 编辑器 / Enhance API editor
*   合并多个 API 到单编辑器管理 / Merge multiple APIs in one editor
*   修复触发指令逻辑，保证 /Rapi 正常解析参数 / Fix command parsing

### v2.2.1
*   修复 array 类型配置导致加载失败的问题 / Fix array type config loading issue
*   支持后台动态添加、删除 API 参数 / Support dynamic add/delete API parameters

### v2.2.0
*   重构 JSON 配置逻辑，支持多 API 和多参数 / Refactor JSON config, support multiple APIs
*   添加 /查api 指令 / Add /查api command
*   实现 JSON 路径提取功能 / JSON path extraction support
*   初步实现媒体类型识别（图片/音频/视频） / Initial media type recognition

## 注意事项 / Notes
*   图片通过下载到本地临时文件发送，确保插件运行环境支持访问临时文件 / Ensure environment supports temp file access
*   音频/视频默认通过 URL 发送，可按需改成下载本地发送 / Audio/Video sent via URL by default
*   JSON 路径解析功能保持原样 / JSON path extraction remains functional