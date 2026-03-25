enable_logging: bool - 是否启用调用日志输出，默认 false（生产环境建议关闭）
apis: template_list - API配置列表，每个元素代表一个API
    command: string - 触发指令，如 /weather
    url: string - API地址，支持 {param} 占位符
    method: string - HTTP方法（GET/POST/PUT/DELETE）
    headers: dict - 请求头（JSON对象）
    body: string - 请求体模板（JSON字符串），支持 {param} 占位符
    response_type: string - 返回格式，text 或 json