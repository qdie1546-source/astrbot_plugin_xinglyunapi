import re
import httpx
from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star


class XingYunAPI(Star):

    def __init__(self, context: Context, config: dict):
        super().__init__(context)
        self.config = config

    # ========================
    # /查api
    # ========================
    @filter.command("查api")
    async def list_api(self, event: AstrMessageEvent):
        api_list = self.config.get("api_list", [])
        ad = self.config.get("ad_text", "")

        if not api_list:
            yield event.plain_result("暂无API配置")
            return

        msg = "📡 可用API列表：\n\n"
        for api in api_list:
            msg += f"🔹 {api['trigger']} → {api['name']}\n"

        if ad:
            msg += f"\n———\n📢 {ad}"

        yield event.plain_result(msg)

    # ========================
    # /Rapi 调用
    # ========================
    @filter.command("Rapi")
    async def call_api(self, event: AstrMessageEvent):
        text = event.message_str.strip()

        parts = text.split()
        if len(parts) < 2:
            yield event.plain_result("用法：/Rapi 指令 参数")
            return

        trigger = parts[1]
        args = parts[2:]

        api_list = self.config.get("api_list", [])

        target_api = None
        for api in api_list:
            if api["trigger"] == trigger:
                target_api = api
                break

        if not target_api:
            yield event.plain_result("未找到该API")
            return

        url = target_api["url"]
        method = target_api.get("method", "GET")
        params_keys = target_api.get("params", [])

        # 参数映射
        params = {}
        for i, key in enumerate(params_keys):
            if i < len(args):
                params[key] = args[i]

        try:
            async with httpx.AsyncClient(timeout=15) as client:
                if method == "GET":
                    resp = await client.get(url, params=params)
                else:
                    resp = await client.post(url, data=params)

            content = resp.text.strip()

            # 自动解析
            await self.handle_response(event, content)

        except Exception as e:
            yield event.plain_result(f"请求失败：{str(e)}")

    # ========================
    # 响应处理核心
    # ========================
    async def handle_response(self, event, content: str):

        # JSON解析
        if content.startswith("{"):
            try:
                import json
                data = json.loads(content)

                # 常见字段 msg / data
                for key in ["msg", "data", "url"]:
                    if key in data:
                        content = str(data[key])
                        break
            except:
                pass

        # 提取URL
        url_match = re.findall(r'https?://[^\s]+', content)
        if url_match:
            url = url_match[0]

            if self.is_image(url):
                yield event.image_result(url)
                return

            if self.is_audio(url):
                yield event.record_result(url)
                return

            if self.is_video(url):
                yield event.video_result(url)
                return

            yield event.plain_result(url)
            return

        # fallback
        yield event.plain_result(content)

    def is_image(self, url):
        return any(url.endswith(x) for x in [".jpg", ".png", ".jpeg", ".gif"])

    def is_audio(self, url):
        return any(url.endswith(x) for x in [".mp3", ".wav"])

    def is_video(self, url):
        return any(url.endswith(x) for x in [".mp4", ".m3u8"])