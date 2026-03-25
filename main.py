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
        self.apis = {api["name"]: api for api in config.get("apis", [])}

    @filter.command("Rapi")
    async def handle_rapi(self, event: AstrMessageEvent):
        """统一入口指令，格式: /Rapi <api_name> [参数]"""
        parts = event.message_str.strip().split(maxsplit=2)
        if len(parts) < 2:
            yield event.plain_result("用法：/Rapi <API名称> [参数]")
            return

        api_name = parts[1]
        param_str = parts[2] if len(parts) > 2 else ""

        if api_name not in self.apis:
            yield event.plain_result(f"未找到名为 {api_name} 的 API 配置")
            return

        api = self.apis[api_name]
        await self.call_api(event, api, param_str)

    async def call_api(self, event: AstrMessageEvent, api: dict, param_str: str):
        url = api["url"]
        if "{param}" in url:
            url = url.replace("{param}", param_str)

        method = api.get("method", "GET").upper()
        headers = api.get("headers", {})

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
        pass