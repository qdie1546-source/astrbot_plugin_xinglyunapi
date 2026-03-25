import json
import aiohttp
from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star
from astrbot.api import logger

class XinglyunApiPlugin(Star):
    def __init__(self, context: Context, config: dict):
        super().__init__(context)
        self.config = config
        self.enable_logging = config.get("enable_logging", False)
        self.apis = config.get("apis", [])

    @filter.event_message_type(filter.EventMessageType.ALL)
    async def on_message(self, event: AstrMessageEvent):
        message = event.message_str.strip()
        if not message:
            return
        # 遍历API配置，检查指令匹配
        for api in self.apis:
            command = api.get("command", "").strip()
            if not command:
                continue
            if message.startswith(command):
                param_str = message[len(command):].strip()
                await self.call_api(event, api, param_str)
                return

    async def call_api(self, event: AstrMessageEvent, api: dict, param_str: str):
        # 替换URL中的占位符
        url = api["url"]
        if "{param}" in url:
            url = url.replace("{param}", param_str)

        method = api.get("method", "GET").upper()
        headers = api.get("headers", {})

        # 处理请求体（仅POST/PUT）
        body_json = None
        body_template = api.get("body", "")
        if body_template and method in ["POST", "PUT"]:
            body_str = body_template.replace("{param}", param_str)
            try:
                body_json = json.loads(body_str)
            except json.JSONDecodeError:
                body_json = body_str

        if self.enable_logging:
            logger.info(f"[星落云API] 请求: {method} {url}, 参数: {param_str}")

        async with aiohttp.ClientSession() as session:
            try:
                if method == "GET":
                    async with session.get(url, headers=headers) as resp:
                        response_text = await resp.text()
                elif method == "POST":
                    async with session.post(
                        url,
                        json=body_json if isinstance(body_json, dict) else None,
                        data=body_json if isinstance(body_json, str) else None,
                        headers=headers
                    ) as resp:
                        response_text = await resp.text()
                elif method == "PUT":
                    async with session.put(
                        url,
                        json=body_json if isinstance(body_json, dict) else None,
                        data=body_json if isinstance(body_json, str) else None,
                        headers=headers
                    ) as resp:
                        response_text = await resp.text()
                elif method == "DELETE":
                    async with session.delete(url, headers=headers) as resp:
                        response_text = await resp.text()
                else:
                    response_text = f"不支持的HTTP方法: {method}"

                if self.enable_logging:
                    logger.info(f"[星落云API] 响应状态码: {resp.status}")

                # 根据配置格式化响应
                resp_type = api.get("response_type", "text")
                if resp_type == "json":
                    try:
                        data = json.loads(response_text)
                        result = json.dumps(data, ensure_ascii=False, indent=2)
                    except:
                        result = response_text
                else:
                    result = response_text

                await event.send(event.plain_result(result))

            except Exception as e:
                logger.error(f"[星落云API] 调用失败: {e}")
                await event.send(event.plain_result(f"API调用失败: {str(e)}"))

    async def terminate(self):
        """插件卸载时清理（可选）"""
        pass