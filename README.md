
# 星落云 - 自定义API插件

通过WebUI灵活配置API和指令，实现任意外部API的动态调用，无需修改代码。支持多API管理、参数占位符、自定义请求头和请求体，并提供可选的日志输出开关，方便调试与生产环境灵活切换。

## ✨ 特性

- **动态配置**：在WebUI中管理API列表，支持添加、修改、删除，配置即时生效（需重载插件）。
- **多API支持**：可配置多个API，每个API绑定独立的触发指令。
- **灵活的参数传递**：URL或请求体中使用 `{param}` 占位符，用户输入自动替换。
- **请求方法**：支持 GET、POST、PUT、DELETE。
- **自定义请求头/体**：支持JSON格式的请求头配置，请求体模板支持占位符。
- **响应格式化**：可选择返回纯文本或格式化JSON。
- **错误处理**：友好的错误提示，避免插件崩溃。
- **调用日志开关**：可配置是否记录API请求与响应日志，生产环境关闭以提升性能。

## 📦 安装

1. 克隆本仓库到 AstrBot 的插件目录：
   ```bash
   cd AstrBot/data/plugins
   git clone https://github.com/qdie1546-source/astrbot_plugin_xinglyunapi.git

1. 重启 AstrBot 或在 WebUI 中启用插件。
2. 如需安装依赖，AstrBot 会自动读取 requirements.txt 并安装。

⚙️ 配置

插件通过 _conf_schema.json 定义配置项，您可以在 WebUI 的插件管理页面直接配置。

配置项说明

```
enable_logging: bool - 是否启用调用日志输出，默认 false（生产环境建议关闭）
apis: template_list - API配置列表，每个元素代表一个API
    command: string - 触发指令，如 /weather
    url: string - API地址，支持 {param} 占位符
    method: string - HTTP方法（GET/POST/PUT/DELETE）
    headers: dict - 请求头（JSON对象）
    body: string - 请求体模板（JSON字符串），支持 {param} 占位符
    response_type: string - 返回格式，text 或 json
```

配置示例

假设要添加一个天气查询API：

· 指令：/weather
· URL：https://api.weather.com/current?city={param}
· 方法：GET
· 响应类型：json

在 WebUI 中添加一条配置即可。

🚀 使用示例

配置完成后，在聊天中发送指令并携带参数即可触发：

```
/weather 北京
```

插件将自动请求 https://api.weather.com/current?city=北京，并返回JSON格式的天气信息。

更复杂的 POST 示例

配置一个 POST 请求，使用请求体模板：

· 指令：/echo
· URL：https://httpbin.org/post
· 方法：POST
· 请求体：{"message": "{param}"}

发送 /echo Hello World，插件会 POST 数据 {"message": "Hello World"} 并返回响应。

📝 注意事项

· {param} 占位符会替换为用户输入中指令后的全部内容。
· 请求体模板需为合法的 JSON 字符串。
· 插件会监听所有消息，建议按需启用/禁用插件。
· 修改配置后需在 WebUI 中“重载插件”才能生效。
· 调用日志开关默认关闭，开启后会在控制台输出请求URL、参数、响应状态等信息，便于调试。

🔧 更新日志

v2.1.0 - 2026-03-25

· 新增 调用日志开关（enable_logging），生产环境可关闭以提升性能。
· 优化 调整日志输出级别，仅当开关开启时记录。
· 修复 部分请求体格式错误导致的异常捕获。
· 重构 代码结构更清晰，便于后续扩展。

👥 开发者

· 作者：星落云
· 项目地址：GitHub
· 许可证：MIT

📚 更多文档

· AstrBot 插件开发指南
· 插件配置指南

---

<!-- 广告位预留（后续可在此处展示推广信息） -->

<!-- 示例：想推广你的API？联系我们获取专属广告位！ -->

---

注：此插件由星落云开发维护，欢迎 Star ⭐ 和反馈 Issues。

```

---