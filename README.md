# 星落云API管理插件 v2.1.0

## 📖 功能介绍
- 支持管理员配置多个自定义API接口
- 动态参数管理，支持GET/POST请求
- 智能识别返回内容（图片/文字/JSON）
- 管理员可视化配置界面（WebUI）
- 广告位功能，方便推广

## 🚀 快速开始
1. 安装插件后，在AstrBot WebUI的插件配置中找到“自定义API管理”
2. 添加API配置，设置触发指令（如`weather`）、接口URL（支持`{参数名}`占位符）、参数定义等
3. 用户发送 `/查api` 查看所有可用指令
4. 用户发送 `/Rapi <触发指令> [参数...]` 调用接口

## 📝 更新日志
### v2.1.0 (2025-03-25)
- ✨ 新增广告位功能
- 🐛 修复参数解析问题
- 📚 完善错误提示
- 🎨 优化响应处理逻辑

### v2.0.0
- 支持多API动态管理
- 增加响应智能识别

## 💡 配置示例
在WebUI中，添加一个API配置：
- 触发指令: `weather`
- API地址: `https://api.example.com/weather?city={city}`
- 请求方式: GET
- 参数配置: `city` (必填，描述“城市名”)
- 功能描述: 查询天气

## 🔗 相关链接
- 开发者: 星落云
- 插件仓库: https://github.com/qdie1546-source/astrbot_plugin_xinglyunapi
- 接口支持: [星落云API平台](https://api.xingluoyun.com)

## ❓ 常见问题
Q: 为什么调用API后返回“参数数量错误”？
A: 请检查您输入的参数个数是否与配置中的参数定义数量一致。

Q: 支持POST请求的JSON体吗？
A: 当前版本仅支持表单参数（application/x-www-form-urlencoded），如需JSON请期待后续更新。

Q: 广告位如何关闭？
A: 在插件配置中将“启用广告”设置为false即可。