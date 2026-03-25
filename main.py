import aiohttp
import json
from typing import Dict, Any, Optional

from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.star import Context, Star
from astrbot.api import AstrBotConfig, logger

class XinglyunAPI(Star):
    def __init__(self, context: Context, config: AstrBotConfig):
        super().__init__(context)
        self.config = config  # 插件配置实例

    @filter.command("Rapi")
    async def handle_api_call(self, event: AstrMessageEvent):
        """处理/Rapi指令，格式：/Rapi <触发指令> [参数...]"""
        parts = event.message_str.strip().split()
        if len(parts) < 2:
            yield event.plain_result("用法：/Rapi <触发指令> [参数...]\n输入 /查api 查看可用指令")
            return
        
        trigger = parts[1]
        params_values = parts[2:]

        apis = self.config.get("apis", {})
        if trigger not in apis:
            yield event.plain_result(f"未找到触发指令 '{trigger}'，请检查配置或使用 /查api 查看可用指令")
            return
        
        api_config = apis[trigger]
        url_template = api_config.get("url", "")
        method = api_config.get("method", "GET").upper()
        headers = api_config.get("headers", {})
        params_schema = api_config.get("params", {})

        param_names = list(params_schema.keys())
        if len(params_values) != len(param_names):
            required_count = len([p for p in params_schema.values() if p.get("required", True)])
            optional_count = len(param_names) - required_count
            yield event.plain_result(f"参数数量错误：需要 {len(param_names)} 个参数（{required_count}个必填，{optional_count}个可选），实际提供了 {len(params_values)} 个")
            return

        request_params = {}
        for name, value in zip(param_names, params_values):
            request_params[name] = value

        for name, schema in params_schema.items():
            if schema.get("required", True) and name not in request_params:
                yield event.plain_result(f"缺少必填参数: {name}")
                return

        url = url_template
        for name, value in request_params.items():
            url = url.replace(f"{{{name}}}", str(value))

        try:
            response_data = await self._make_request(url, method, request_params, headers)
            result = await self._process_response(response_data, event)
            ad_result = await self._append_ad(event)
            if ad_result:
                yield result
                yield ad_result
            else:
                yield result
        except Exception as e:
            logger.error(f"API调用失败: {e}")
            yield event.plain_result(f"请求失败: {str(e)}")

    @filter.command("查api")
    async def list_apis(self, event: AstrMessageEvent):
        """列出所有已配置的API"""
        apis = self.config.get("apis", {})
        if not apis:
            yield event.plain_result("暂未配置任何API，请联系管理员添加。")
            return

        msg = "📋 **可用API列表**\n\n"
        for trigger, info in apis.items():
            desc = info.get("description", "无描述")
            params = info.get("params", {})
            param_desc = ", ".join([f"{n}({'必填' if p.get('required',True) else '可选'})" for n, p in params.items()])
            msg += f"🔹 **/{trigger}** - {desc}\n"
            if param_desc:
                msg += f"   参数: {param_desc}\n"
            msg += "\n"
        msg += "使用方式：/Rapi <触发指令> [参数...]"
        yield event.plain_result(msg)

    async def _make_request(self, url: str, method: str, params: Dict[str, Any], headers: Dict[str, str]) -> Any:
        timeout = aiohttp.ClientTimeout(total=self.config.get("global_timeout", 10))
        async with aiohttp.ClientSession(timeout=timeout) as session:
            if method == "GET":
                async with session.get(url, params=params, headers=headers) as resp:
                    return await self._parse_response(resp)
            elif method == "POST":
                async with session.post(url, data=params, headers=headers) as resp:
                    return await self._parse_response(resp)
            else:
                raise ValueError(f"不支持的请求方法: {method}")

    async def _parse_response(self, response: aiohttp.ClientResponse) -> Any:
        content_type = response.headers.get("Content-Type", "").lower()
        if "application/json" in content_type:
            return await response.json()
        elif "image/" in content_type:
            return await response.read()
        elif "audio/" in content_type:
            return await response.read()
        elif "video/" in content_type:
            return await response.read()
        else:
            return await response.text()

    async def _process_response(self, response_data: Any, event: AstrMessageEvent) -> MessageEventResult:
        if isinstance(response_data, bytes):
            # 二进制数据暂不支持直接发送，返回文本提示
            return event.plain_result("返回了二进制内容，但无法直接展示。")

        if isinstance(response_data, dict):
            # 检查错误码
            if "code" in response_data and response_data["code"] != 200:
                return event.plain_result(f"❌ API错误: {response_data.get('msg', '未知错误')}")

            # 尝试提取媒体URL
            for key, value in response_data.items():
                if isinstance(value, str) and (value.startswith("http://") or value.startswith("https://")):
                    if any(value.lower().endswith(ext) for ext in [".jpg", ".jpeg", ".png", ".gif", ".webp"]):
                        return event.image_result(value)
                    elif any(value.lower().endswith(ext) for ext in [".mp3", ".wav", ".flac"]):
                        return event.record_result(value)
                    elif any(value.lower().endswith(ext) for ext in [".mp4", ".avi", ".mov"]):
                        return event.video_result(value)

            # 普通JSON返回格式化文本
            return event.plain_result(json.dumps(response_data, ensure_ascii=False, indent=2))

        if isinstance(response_data, str):
            if response_data.startswith("http://") or response_data.startswith("https://"):
                if any(response_data.lower().endswith(ext) for ext in [".jpg", ".jpeg", ".png", ".gif", ".webp"]):
                    return event.image_result(response_data)
                elif any(response_data.lower().endswith(ext) for ext in [".mp3", ".wav", ".flac"]):
                    return event.record_result(response_data)
                elif any(response_data.lower().endswith(ext) for ext in [".mp4", ".avi", ".mov"]):
                    return event.video_result(response_data)
            return event.plain_result(response_data)

        return event.plain_result(str(response_data))

    async def _append_ad(self, event: AstrMessageEvent) -> Optional[MessageEventResult]:
        ad_config = self.config.get("ad_banner", {})
        if not ad_config.get("enabled", True):
            return None
        ad_text = ad_config.get("text", "")
        ad_image = ad_config.get("image_url", "")
        if ad_image:
            return event.image_result(ad_image)
        elif ad_text:
            return event.plain_result(f"\n---\n{ad_text}")
        return None

    async def terminate(self):
        """插件卸载时清理"""
        pass