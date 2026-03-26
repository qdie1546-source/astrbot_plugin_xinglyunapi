from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star, register
import aiohttp
import json
import tempfile
import os
import base64
import mimetypes
import urllib.parse
import re

@register(
    "astrbot_plugin_xinglyunapi",
    "星落云",
    "自定义API管理（UI重构版）",
    "2.3.1",
)
class XingYunAPI(Star):

    def __init__(self, context: Context, config):
        super().__init__(context)
        self.config = config

    # =========================
    # 加载API
    # =========================
    def load_apis(self):
        try:
            if self.config.get("editor_mode", True):
                raw = self.config.get("api_editor", "{}")
                return json.loads(raw)
            return {}
        except:
            return {}

    # =========================
    # 工具
    # =========================
    def get_nested(self, data, path):
        if not path:
            return data
        for key in path.split("."):
            if isinstance(data, dict):
                data = data.get(key)
            elif isinstance(data, list):
                data = data[0]
            else:
                return None
        return data

    def detect_type(self, content_type, url=""):
        if not content_type:
            mime, _ = mimetypes.guess_type(url)
            content_type = mime or ""

        content_type = content_type.lower()

        if "json" in content_type:
            return "json"
        if "image" in content_type:
            return "img"
        if "audio" in content_type:
            return "audio"
        if "video" in content_type:
            return "video"
        return "text"

    def replace_url(self, url, args):
        keys = re.findall(r"{(.*?)}", url)
        for i, k in enumerate(keys):
            if i < len(args):
                url = url.replace(f"{{{k}}}", urllib.parse.quote(args[i]))
        return url

    # =========================
    # API调用
    # =========================
    async def call_api(self, api):
        url = api.get("url")
        method = api.get("method", "GET")
        params = api.get("params", {})
        headers = api.get("headers", {})

        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params, headers=headers) as resp:
                ct = resp.headers.get("Content-Type", "")
                mtype = self.detect_type(ct, url)

                if mtype in ["json", "text"]:
                    try:
                        data = await resp.json()
                    except:
                        data = await resp.text()
                else:
                    data = await resp.read()

                return data, mtype

    # =========================
    # 结果处理
    # =========================
    async def handle_result(self, event, data, mtype, api):

        path = api.get("json_path")

        if mtype == "json" and path:
            data = self.get_nested(data, path)

        # 图片URL
        if isinstance(data, str) and data.startswith("http"):
            if any(x in data.lower() for x in [".jpg",".png",".jpeg",".gif",".webp"]):
                yield event.image_result(data)
                return

        # Base64
        if isinstance(data, str) and "base64" in data:
            try:
                data = data.split("base64,")[1]
                yield event.image_result(f"base64://{data}")
                return
            except:
                pass

        # 二进制图片
        if mtype == "img" and isinstance(data, bytes):
            tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg")
            tmp.write(data)
            tmp.close()
            yield event.image_result(tmp.name)
            os.unlink(tmp.name)
            return

        # 音频
        if mtype == "audio":
            yield event.record_result(data if isinstance(data,str) else "")
            return

        # 视频
        if mtype == "video":
            yield event.video_result(data if isinstance(data,str) else "")
            return

        yield event.plain_result(str(data))

    # =========================
    # API列表
    # =========================
    @filter.command("查api")
    async def list_api(self, event: AstrMessageEvent):
        apis = self.load_apis()

        if not apis:
            yield event.plain_result("暂无API")
            return

        msg = "📡 API列表：\n\n"
        for name in apis:
            msg += f"• {name}\n"

        yield event.plain_result(msg)

    # =========================
    # 主调用
    # =========================
    @filter.command("Rapi")
    async def run_api(self, event: AstrMessageEvent):

        parts = event.message_str.strip().split()

        if len(parts) < 2:
            yield event.plain_result("用法：/Rapi 指令 参数")
            return

        key = parts[1]
        args = parts[2:]

        apis = self.load_apis()

        if key not in apis:
            yield event.plain_result("❌ API不存在")
            return

        api = apis[key]

        url = api.get("url")
        if "{" in url:
            url = self.replace_url(url, args)

        api["url"] = url

        data, mtype = await self.call_api(api)

        async for r in self.handle_result(event, data, mtype, api):
            yield r