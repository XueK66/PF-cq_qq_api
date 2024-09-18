from .constant import *
from .websocket import QQWebSocketConnector
from mcdreforged.api.types import PluginServerInterface

connector = None

def on_load(server: PluginServerInterface, old_module):
    # 加载配置文件
    config = server.load_config_simple("config.yml", DEFAULT_CONFIG)

    global connector
    connector = QQWebSocketConnector(server, config)
    connector.connect()

def on_unload(server: PluginServerInterface):
    global connector
    if connector:
        connector.close()
        server.logger.info(LANGUAGE[connector.language]["close_success"])

def get_bot():
    if connector:
        return connector.bot