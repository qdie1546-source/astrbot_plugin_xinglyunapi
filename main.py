{
  "editor_mode": {
    "type": "bool",
    "title": "启用API编辑器",
    "default": true,
    "description": "开启后使用JSON编辑器统一管理API"
  },
  "api_editor": {
    "type": "text",
    "title": "API管理编辑器",
    "description": "使用JSON格式配置所有API",
    "default": "{\n  \"qq_avatar\": {\n    \"url\": \"https://uapis.cn/api/v1/social/qq/userinfo?qq={qq}\",\n    \"method\": \"GET\",\n    \"json_path\": \"avatar_url\"\n  }\n}"
  }
}