"""AstrBot Bridge 插件

在 ON_START 时注册 WS 自定义消息处理器（tool_sync / tool_result），
接收 AstrBot 推送的工具定义并动态注册代理 BaseTool 类。
"""

from typing import List, Tuple, Type, Union

from src.plugin_system import (
    BasePlugin,
    register_plugin,
    ComponentInfo,
    EventHandlerInfo,
    ToolInfo,
)
from src.plugin_system.base.base_events_handler import BaseEventHandler
from src.plugin_system.base.base_tool import BaseTool
from src.plugin_system.base.config_types import ConfigField

from .astrbot_bridge_handler import AstrBotBridgeInitHandler


@register_plugin
class AstrBotBridgePlugin(BasePlugin):
    """AstrBot Bridge 插件 — 将 AstrBot 工具注入到 MaiBot"""

    plugin_name: str = "astrbot_bridge"
    enable_plugin: bool = True
    dependencies: list[str] = []
    python_dependencies: list[str] = []
    config_file_name: str = "config.toml"

    config_schema: dict = {
        "bridge": {
            "astrbot_platform": ConfigField(
                type=str,
                default="astrbot",
                description="AstrBot 平台标识，用于消息路由",
            ),
            "tool_call_timeout": ConfigField(
                type=float,
                default=30.0,
                description="远程工具调用超时时间（秒）",
            ),
            "log_tool_calls": ConfigField(
                type=bool,
                default=True,
                description="是否记录工具调用的详细日志",
            ),
        },
    }

    def get_plugin_components(
        self,
    ) -> List[Tuple[Union[EventHandlerInfo, ToolInfo], Type[Union[BaseEventHandler, BaseTool]]]]:
        """返回插件组件列表"""
        return [
            (AstrBotBridgeInitHandler.get_handler_info(), AstrBotBridgeInitHandler),
        ]
