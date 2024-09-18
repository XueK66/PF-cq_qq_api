import websocket
import threading
import json
from .bot import bot
from .constant import LANGUAGE
from .info import QQInfo

class QQWebSocketConnector:
    def __init__(self, server, config):
        self.ws = None
        self.listener_thread = None

        self.config = config
        self.language = config.get("language", "zh")
        if self.language not in LANGUAGE:
            server.logger.warning(LANGUAGE["en"]["language_not_found"].format(self.language))
            self.language = "en"
        self.server = server

        host = self.config.get("host")
        port = self.config.get("port")
        post_path = self.config.get("post_path")
        token = self.config.get("token")
        self.headers = None

        self.url = f"ws://{host}:{port}"

        if post_path:
            self.url += f"/{post_path}"
        if token:
            self.headers = {
                "Authorization": f"Bearer {token}"
            } 

        self.bot = bot(self.send_message)

    def connect(self):
        self.server.logger.info(LANGUAGE[self.language]["try_connect"].format(self.url))
        if self.headers:
            self.ws = websocket.WebSocketApp(
                self.url,
                header=self.headers,
                on_message=self.on_message,
                on_error=self.on_error,
                on_close=self.on_close
            )
        else:
            self.ws = websocket.WebSocketApp(
                self.url,
                on_message=self.on_message,
                on_error=self.on_error,
                on_close=self.on_close
            )

        # 创建并启动监听线程
        self.listener_thread = threading.Thread(target=self.ws.run_forever)
        self.listener_thread.start()

        self.server.logger.info(LANGUAGE[self.language]["start_connect"])


    def on_message(self, ws, message):
        # 处理接收到的消息
        self.server.logger.debug(LANGUAGE[self.language]["received_message"].format(message))

        message = json.loads(message)

        if message.get("echo", ""):
            self.bot.function_return[message["echo"]] = message
            return

        QQInfo(message, self.server, self.bot)

    def on_error(self, ws, error):
        self.server.logger.error(LANGUAGE[self.language]["error_connect"].format(error))

    def on_close(self, ws, close_status_code, close_msg):
        self.server.logger.debug(LANGUAGE[self.language]["close_connect"])
        self.close()

    def send_message(self, message):
        if self.ws and self.ws.sock and self.ws.sock.connected:
            self.ws.send(json.dumps(message))

            self.server.logger.debug(LANGUAGE[self.language]["send_message"].format(message))
        else:
            self.server.logger.warning(LANGUAGE[self.language]["retry_connect"])

    def close(self):
        try:
            if self.ws:
                self.ws.close()
            if self.listener_thread:
                self.listener_thread.join()
            self.server.logger.info(LANGUAGE[self.language]["close_info"])
        except Exception as e:
            self.server.logger.warning(LANGUAGE[self.language]["error_close"].format(e))