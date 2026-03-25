import re
import json
import time
from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star


class XingYunAPI(Star):

    def __init__(self, context: Context, config: dict):
        super().__init__(context)
        self.config = config
        self.user_cd = {}
        self.api_data = {}
        self.load_all_api()

    # ========================
    # 加载所有API配置
    # ========================
    def load_all_api(self):
        try:
            text = self.config.get("api_json", "{}")
            self.api_data = json.loads(text)
        except Exception as e:
            print("API配置解析失败:", e)
            self.api_data = {}

    # ========================
    # API列表
    # ========================
    @filter.command("查api")
    async def list_api(self, event: AstrMessageEvent):
        if not self.api_data:
            yield event.plain_result("暂无API配置")
            return

        msg = "📡 API列表：\n\n"
        for key, api in self.api_data.items():
            if not isinstance(api, dict):
                continue
            name = api.get("name", "未命名")
            msg += f"🔹 {key} → {name}\n"

        yield event.plain_result(msg)

    # ========================
    # 限流检测
    # ========================
    def check_cd(self, user_id):
        cd = self.config.get("cooldown", 3)
        now = time.time()
        if user_id in self.user_cd:
            if now - self.user_cd[user_id] < cd:
                return False
        self.user_cd[user_id] = now
        return True

    # ========================
    # API调用
    # ========================
    @filter.command("Rapi")
    async def call_api(self, event: AstrMessageEvent):
        user_id = event.get_sender_id()
        if not self.check_cd(user_id):
            yield event.plain_result("请求过快，请稍后再试")
            return

        parts = event.message_str.strip().split()
        if len(parts) < 2:
            yield event.plain_result("用法：/Rapi 指令 参数")
            return

        trigger = parts[1].lower()
        args = parts[2:]
        api = self.find_api(trigger)
        if not api:
            yield event.plain_result("API不存在")
            return

        content = await self.request_api(api, args)
        async for r in self.handle_response(event, content, api):
            yield r

    # ========================
    # 调试API
    # ========================
    @filter.command("调试api")
    async def debug_api(self, event: AstrMessageEvent):
        parts = event.message_str.strip().split()
        if len(parts) < 2:
            yield event.plain_result("用法：/调试api 指令 参数")
            return

        trigger = parts[1].lower()
        args = parts[2:]
        api = self.find_api(trigger)
        if not api:
            yield event.plain_result("API不存在")
            return

        content = await self.request_api(api, args)
        async for r in self.handle_response(event, content, api):
            yield r

    # ========================
    # 查找API
    # ========================
    def find_api(self, trigger):
        api = self.api_data.get(trigger)
        if not isinstance(api, dict):
            return None
        return api

    # ========================
    # 请求API
    # ========================
    async def request_api(self, api, args):
        params = {}
        keys = api.get("params", [])
        for i, key in enumerate(keys):
            if i < len(args):
                params[key] = args[i]

        import httpx
        try:
            async with httpx.AsyncClient(timeout=15) as client:
                method = api.get("method", "GET").upper()
                resp = await client.request(
                    method,
                    api.get("url"),
                    params=params if method == "GET" else None,
                    data=params if method == "POST" else None
                )
            return resp.text.strip()
        except Exception as e:
            return json.dumps({"error": f"请求失败: {str(e)}"})

    # ========================
    # JSON路径解析
    # ========================
    def extract_json(self, content, path):
        try:
            data = json.loads(content)
            for key in path.replace("]", "").split("."):
                if "[" in key:
                    k, i = key.split("[")
                    data = data[k][int(i)]
                else:
                    data = data[key]
            return str(data)
        except Exception:
            return content

    # ========================
    # 响应处理
    # ========================
    async def handle_response(self, event, content, api):
        # JSON路径提取
        json_path = api.get("json_path", "")
        if json_path:
            content = self.extract_json(content, json_path)

        # 提取URL
        urls = re.findall(r'https?://[^\s]+', content)
        if urls:
            url = urls[0]

            # 图片直接发送（网络 URL）
            if self.is_image(url):
                yield event.image_result(url, type="url")
                return

            # 音频直接发送
            if self.is_audio(url):
                yield event.record_result(url, type="url")
                return

            # 视频直接发送
            if self.is_video(url):
                yield event.video_result(url, type="url")
                return

            # fallback
            yield event.plain_result(url)
            return

        # fallback
        yield event.plain_result(content)

    # ========================
    # 类型判断
    # ========================
    def is_image(self, url):
        url = url.split("?")[0].lower()
        return any(url.endswith(x) for x in [".jpg", ".png", ".jpeg", ".gif", ".webp"])

    def is_audio(self, url):
        url = url.split("?")[0].lower()
        return any(url.endswith(x) for x in [".mp3", ".wav", ".aac"])

    def is_video(self, url):
        url = url.split("?")[0].lower()
        return any(url.endswith(x) for x in [".mp4", ".m3u8", ".flv"])