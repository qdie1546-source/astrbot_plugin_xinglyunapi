import re
import tempfile
import os
import httpx

async def handle_response(self, event, content, api):
    """
    响应处理（可靠发送图片、音频、视频）
    """
    # JSON路径提取
    json_path = api.get("json_path", "")
    if json_path:
        content = self.extract_json(content, json_path)

    # 提取 URL
    urls = re.findall(r'https?://[^\s]+', content)
    if urls:
        url = urls[0]

        # ========================
        # 图片直接发送（可靠方法：下载本地临时文件）
        # ========================
        if self.is_image(url):
            try:
                async with httpx.AsyncClient(timeout=15) as client:
                    resp = await client.get(url)
                    resp.raise_for_status()
                    # 保存到临时文件
                    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg")
                    tmp.write(resp.content)
                    tmp.close()
                    # 发送图片
                    yield event.image_result(tmp.name)
                    # 删除临时文件
                    os.unlink(tmp.name)
                    return
            except Exception as e:
                yield event.plain_result(f"图片下载失败: {e}")
                return

        # ========================
        # 音频直接发送
        # ========================
        if self.is_audio(url):
            yield event.record_result(url, type="url")
            return

        # ========================
        # 视频直接发送
        # ========================
        if self.is_video(url):
            yield event.video_result(url, type="url")
            return

        # fallback
        yield event.plain_result(url)
        return

    # fallback 文本
    yield event.plain_result(content)