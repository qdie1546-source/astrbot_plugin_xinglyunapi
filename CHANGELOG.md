<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>自定义API管理插件说明</title>
    <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; padding: 20px; background: #f9f9f9; color: #333; }
        h1, h2, h3 { color: #2c3e50; }
        pre { background: #eee; padding: 10px; border-radius: 5px; overflow-x: auto; }
        code { font-family: Consolas, monospace; color: #c7254e; }
        table { border-collapse: collapse; width: 100%; margin-bottom: 20px; }
        th, td { border: 1px solid #ccc; padding: 8px; text-align: left; }
        th { background: #f0f0f0; }
        a { color: #3498db; text-decoration: none; }
        a:hover { text-decoration: underline; }
        .section { margin-bottom: 30px; }
    </style>
</head>
<body>

    <h1>自定义API管理插件（XingYun API Manager） v2.2.2</h1>

    <div class="section">
        <h2>1. 插件简介</h2>
        <p><strong>插件名称：</strong>自定义API管理</p>
        <p><strong>版本：</strong>v2.2.2</p>
        <p><strong>开发者：</strong>星落云</p>
        <p><strong>项目链接：</strong><a href="https://github.com/qdie1546-source/astrbot_plugin_xinglyunapi.git" target="_blank">GitHub 仓库</a></p>
        <p>该插件用于在 AstrBot 中灵活管理自定义 API，支持多 API、多参数接口、JSON路径解析、自动识别媒体类型、调试接口以及防刷冷却机制。</p>
    </div>

    <div class="section">
        <h2>2. 功能说明</h2>
        <h3>2.1 多 API 管理</h3>
        <ul>
            <li>所有 API 配置集中在 JSON 编辑器中管理</li>
            <li>支持无限添加 API</li>
            <li>支持多参数接口</li>
            <li>支持为不同 API 定义不同触发指令</li>
        </ul>

        <h3>2.2 媒体类型自动识别</h3>
        <ul>
            <li>图片：.jpg, .png, .gif, .webp</li>
            <li>音频：.mp3, .wav, .aac</li>
            <li>视频：.mp4, .m3u8, .flv</li>
            <li>自动发送对应媒体内容，不仅仅返回链接</li>
        </ul>

        <h3>2.3 调试接口</h3>
        <ul>
            <li>使用 <code>/调试api</code> 可即时测试接口返回内容</li>
            <li>支持输入参数，查看接口返回结果</li>
        </ul>

        <h3>2.4 冷却机制</h3>
        <ul>
            <li>插件内置用户冷却，防止接口被刷</li>
            <li>冷却时间可在插件配置中调整（默认 3 秒）</li>
        </ul>
    </div>

    <div class="section">
        <h2>3. 安装说明</h2>
        <ol>
            <li>在 AstrBot 后台插件市场搜索 <strong>自定义API管理</strong></li>
            <li>点击 <strong>安装</strong></li>
            <li>安装完成后，插件会自动生成默认 JSON 编辑器配置</li>
            <li>在插件配置中可以看到一个 <strong>JSON 编辑器</strong>，用于管理 API</li>
        </ol>
        <p>⚠️ 目前 UI 使用单编辑器方案，不支持点击 API 切换编辑器，但可以通过分块/分隔管理多个 API。</p>
    </div>

    <div class="section">
        <h2>4. 配置说明</h2>
        <p>插件使用单 JSON 编辑器管理所有 API，推荐结构如下：</p>

        <pre><code>{
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
}</code></pre>

        <h3>JSON 字段说明</h3>
        <table>
            <tr><th>字段</th><th>类型</th><th>说明</th></tr>
            <tr><td>key</td><td>string</td><td>触发指令（用户调用 <code>/Rapi key</code>）</td></tr>
            <tr><td>name</td><td>string</td><td>API 显示名称</td></tr>
            <tr><td>url</td><td>string</td><td>接口地址</td></tr>
            <tr><td>method</td><td>string</td><td>请求方法：GET / POST</td></tr>
            <tr><td>params</td><td>array</td><td>参数名称数组</td></tr>
            <tr><td>json_path</td><td>string</td><td>可选 JSON 路径，用于提取返回结果</td></tr>
        </table>
    </div>

    <div class="section">
        <h2>5. 使用方法</h2>
        <h3>5.1 查看已配置 API</h3>
        <pre><code>/查api</code></pre>
        <p>输出示例：</p>
        <pre><code>📡 API列表：

🔹 weather → 天气查询
🔹 image → 随机图片</code></pre>

        <h3>5.2 调用 API</h3>
        <pre><code>/Rapi weather 北京
/Rapi image 88888888 88888888</code></pre>
        <p>插件会根据 JSON 配置发送请求，并自动返回结果（图片/文本/音频/视频）。</p>

        <h3>5.3 调试接口</h3>
        <pre><code>/调试api weather 北京</code></pre>
        <p>用于即时查看接口返回内容，不经过媒体解析。</p>
    </div>

    <div class="section">
        <h2>6. JSON 编辑技巧</h2>
        <h3>6.1 分块管理 API</h3>
        <pre><code>{
  "_天气类": {},
  "weather": { ... },

  "_娱乐类": {},
  "image": { ... }
}</code></pre>
        <p>这些伪字段不会被解析成 API，可用于视觉分隔。</p>

        <h3>6.2 避免常见问题</h3>
        <ul>
            <li>API不存在：确认 JSON 键名和触发指令一致</li>
            <li>返回文本而不是图片：确认 URL 结尾标准，如 .jpg</li>
            <li>请求失败：确认接口地址和参数正确</li>
            <li>调用过快：冷却时间未过，等待或调整 cooldown</li>
        </ul>
    </div>

    <div class="section">
        <h2>7. 注意事项</h2>
        <ul>
            <li>插件 UI 是单编辑器方案，不支持动态点击切换 API</li>
            <li>推荐使用 <code>_说明</code> 或 <code>_分类名</code> 分隔不同 API</li>
            <li>JSON 配置务必合法，否则插件无法解析</li>
        </ul>
    </div>

    <div class="section">
        <h2>8. 版本更新记录</h2>
        <h3>v2.2.2</h3>
        <ul>
            <li>修复 async_generator can't be used in await 问题</li>
            <li>handle_response 正确使用 async for</li>
            <li>call_api / debug_api 均可稳定返回图片/音频/视频</li>
            <li>优化 JSON 解析，支持分隔块管理多个 API</li>
        </ul>
        <h3>v2.2.1</h3>
        <ul>
            <li>初步 JSON 编辑器方案</li>
            <li>多 API + 多参数 + JSON路径解析</li>
            <li>图片/音频/视频自动发送</li>
        </ul>
        <h3>v2.1.0</h3>
        <ul>
            <li>插件初版发布</li>
            <li>支持单 API 配置和触发指令</li>
        </ul>
    </div>

    <div class="section">
        <h2>9. 联系方式</h2>
        <p>开发者：<strong>星落云</strong></p>
        <p>GitHub 仓库：<a href="https://github.com/qdie1546-source/astrbot_plugin_xinglyunapi.git" target="_blank">astrbot_plugin_xinglyunapi</a></p>
    </div>

</body>
</html>