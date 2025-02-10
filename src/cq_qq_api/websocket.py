import json
import logging
import threading
import websocket

from .bot import bot
from .constant import LANGUAGE
from .info import QQInfo

logging.getLogger("websocket").setLevel(logging.WARNING)

class QQWebSocketConnector:
    def __init__(self, server, config):
        self.config = config
        self.server = server

        self.ws = None
        self.listener_thread = None

        self.language = config.get("language", "zh")
        if self.language not in LANGUAGE:
            server.logger.warning(LANGUAGE["en"]["language_not_found"].format(self.language))
            self.language = "en"
        
        host = self.config.get("host")
        port = self.config.get("port")
        post_path = self.config.get("post_path")
        token = self.config.get("token")
        
        self.url = f"ws://{host}:{port}"
        if post_path:
            self.url += f"/{post_path}"

        self.headers = {"Authorization": f"Bearer {token}"} if token else None

        self.bot = bot(self.send_message, max_wait_time=self.config.get("max_wait_time", 10))

    def connect(self):
        self.server.logger.info(LANGUAGE[self.language]["try_connect"].format(self.url))
        self.ws = websocket.WebSocketApp(
            self.url,
            header=self.headers,
            on_message=self.on_message,
            on_error=self.on_error,
            on_close=self.on_close
        )

        self.listener_thread = threading.Thread(target=self.ws.run_forever, kwargs={'reconnect': 5})
        self.listener_thread.start()

        self.server.logger.info(LANGUAGE[self.language]["start_connect"])

    def on_message(self, ws, message):
        self.server.logger.debug(LANGUAGE[self.language]["received_message"].format(message))

        message = json.loads(message)

        if "echo" in message:
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
