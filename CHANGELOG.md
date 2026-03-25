# 自定义API管理插件（XingYun API Manager） v2.2.2

## 1. 插件简介

- **插件名称**：自定义API管理
- **版本**：v2.2.2
- **开发者**：星落云
- **项目链接**：[GitHub 仓库](https://github.com/qdie1546-source/astrbot_plugin_xinglyunapi.git)

该插件用于在 AstrBot 中灵活管理自定义 API，支持多 API、多参数接口、JSON 路径解析、自动识别媒体类型、调试接口以及防刷冷却机制。

---

## 2. 功能说明

### 2.1 多 API 管理
- 所有 API 配置集中在 JSON 编辑器中管理
- 支持无限添加 API
- 支持多参数接口
- 支持为不同 API 定义不同触发指令

### 2.2 媒体类型自动识别
- 图片：`.jpg, .png, .gif, .webp`
- 音频：`.mp3, .wav, .aac`
- 视频：`.mp4, .m3u8, .flv`
- 自动发送对应媒体内容，不仅仅返回链接

### 2.3 调试接口
- 使用 `/调试api` 可即时测试接口返回内容
- 支持输入参数，查看接口返回结果

### 2.4 冷却机制
- 插件内置用户冷却，防止接口被刷
- 冷却时间可在插件配置中调整（默认 3 秒）

---

## 3. 安装说明

1. 在 AstrBot 后台插件市场搜索 **自定义API管理**
2. 点击 **安装**
3. 安装完成后，插件会自动生成默认 JSON 编辑器配置
4. 在插件配置中可以看到一个 **JSON 编辑器**，用于管理 API

> ⚠️ 目前 UI 使用单编辑器方案，不支持点击 API 切换编辑器，但可以通过分块/分隔管理多个 API。

---

## 4. 配置说明

插件使用单 JSON 编辑器管理所有 API，推荐结构如下：

```json
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
## JSON 字段说明

| 字段      | 类型    | 说明 |
|-----------|--------|------|
| key       | string | 触发指令（用户调用 `/Rapi key`） |
| name      | string | API 显示名称 |
| url       | string | 接口地址 |
| method    | string | 请求方法：GET / POST |
| params    | array  | 参数名称数组 |
| json_path | string | 可选 JSON 路径，用于提取返回结果 |