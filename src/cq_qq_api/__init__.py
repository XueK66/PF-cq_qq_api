from .constant import *
from .websocket import QQWebSocketConnector
from mcdreforged.api.types import PluginServerInterface

connector = None

def on_load(server: PluginServerInterface, old_module):
    # 加载配置文件
    config = server.load_config_simple("config.json", DEFAULT_CONFIG)
    _ = server.load_config_simple("config_note.json", DEFAULT_TRANSLATION)
    move_data(server)

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
    
def move_data(server):
    import os
    if os.path.exists("./config/cq_qq_api/config.yml"):
        old_config = server.load_config_simple("config.yml", DEFAULT_CONFIG)
        config = old_config
        server.save_config_simple(config)
        os.remove("./config/cq_qq_api/config.yml")
    