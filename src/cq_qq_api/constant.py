DEFAULT_CONFIG = {
    "host": "127.0.0.1",
    "port": 8080,
    "post_path": "",
    "token": "",
    "language": "zh"
}

LANGUAGE = {
    "zh":{
        "close_success": "~~ cq_qq_api 服务已关闭 ~~",
        "close_connect": "尝试关闭 cq_qq_api 服务",
        "close_info": "cq_qq_api 连接已关闭且线程已终止。",
        "error_connect": "cq_qq_api 错误: {}",
        "error_close": "关闭 cq_qq_api 时出错: {}",
        "language_not_found": "未找到语言包: {}",
        "received_message": "收到消息: {}",
        "retry_connect": "尝试发送消息，但连接尚未建立，正在重试",
        "send_message": "发送消息到 QQ\n{}",
        "start_connect": "~~ 开始连接 ~~",
        "try_connect": "服务器准备链接 {}",
    },
    "en":{
        "close_success": "~~ cq_qq_api server is closed ~~",
        "close_connect": "Try to close cq_qq_api server",
        "close_info": "cq_qq_api connection closed and threads terminated.",
        "error_connect": "cq_qq_api error: {}",
        "error_close": "Got error when closing cq_qq_api: {}",
        "language_not_found": "Language pack not found: {}",
        "received_message": "Received message: {}",
        "retry_connect": "Try to send message, but the connection is not established, retrying",
        "send_message": "Send message to QQ\n{}",
        "start_connect": "~~ Start connection ~~",
        "try_connect": "Server is ready to connect {}",
    }
}