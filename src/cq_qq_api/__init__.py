from .constant import *
from .websocket import QQWebSocketConnector
from mcdreforged.api.types import PluginServerInterface

connector = None

def on_load(server: PluginServerInterface, old_module):
    # 加载配置文件
    config = server.load_config_simple("config.json", DEFAULT_CONFIG)
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
    return connector.bot if connector else None
    
def move_data(server):
    import os
    old_config_path = "./config/cq_qq_api/config.yml"
    if os.path.exists(old_config_path):
        old_config = server.load_config_simple("config.yml", DEFAULT_CONFIG)
        server.save_config_simple(old_config)
        os.remove(old_config_path)
    