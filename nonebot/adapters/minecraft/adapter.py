import asyncio
import contextlib
from typing import Optional, List, Dict, Any, override

from nonebot import Bot
from nonebot.exception import WebSocketClosed
from nonebot.drivers import WebSocketServerSetup, WebSocket, ASGIMixin, Driver, URL
from nonebot.adapters import Adapter as BaseAdapter
from nonebot import get_plugin_config

from .config import Config
from .logger import log
from nonebot.adapters.onebot.v11 import Adapter as OneBotV11Adapter


class Adapter(BaseAdapter):
    config: Optional[Config] = None
    server_connections: Dict[str, Any] = {}

    @override
    def __init__(self, driver: Driver, **kwargs):
        BaseAdapter.__init__(self, driver, **kwargs)
        self.config = get_plugin_config(Config)
        self.setup()

    @classmethod
    @override
    def get_name(cls) -> str:
        return 'minecraft'

    def setup(self) -> None:
        if not isinstance(self.driver, ASGIMixin):
            raise RuntimeError(
                F'Current driver {self.config.driver} does not support websocket client connections!'
                F'Minecraft Adapter need a WebSocket Client Driver to work.'
            )
        self.driver.on_startup(self.on_startup)
        self.driver.on_shutdown(self.on_shutdown)

    async def on_startup(self):
        server_setup = WebSocketServerSetup(URL('minecraft'), 'minecraft', self._handle_websocket)
        self.setup_websocket_server(server_setup)

    async def on_shutdown(self):
        pass

    async def _call_api(self, bot: Bot, api: str, **data: Any) -> Any:
        pass

    async def _handle_websocket(self, websocket: WebSocket):
        name = websocket.request.headers.get('name')
        if websocket.request.headers.get('token') != self.config.minecraft_token:
            log('warning', F'Invalid token from server "{name}".')
            await websocket.close(403, 'Invalid token.')
            return None
        if not name:
            log('warning', F'No name provided from server "{name}".')
            await websocket.close(403, 'No name provided.')
            return None
        if name in self.server_connections:
            log('warning', F'Name "{name}" has already occupied.')
            await websocket.close(403, F'Name "{name}" has already occupied.')
            return None
        await websocket.accept()
        log('success', F'The server "{name}" has connected.')
        try:
            pass
        except WebSocketClosed:
            log('warning', F'The server "{name}" has disconnected.')
        finally:
            with contextlib.suppress(Exception):
                await websocket.close()
            self.server_connections.pop(name, None)
            self.bot_disconnect(name)
