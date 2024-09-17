from json import dumps
from typing import override, Optional, Union, Any

from nonebot import Bot as BaseBot
from nonebot.adapters import Adapter
from nonebot.drivers import WebSocket
from nonebot.exception import ActionFailed
from nonebot.message import handle_event

from .utils import parse_response, dump
from .playerevent import PlayerMessageEvent, Player
from .message import Message, MessageSegment


class Server(BaseBot):
    websocket: WebSocket = None

    @override
    def __init__(self, adapter: Adapter, name: str, websocket: WebSocket):
        BaseBot.__init__(self, adapter, name)
        self.websocket = websocket

    @override
    async def send(
            self,
            event: PlayerMessageEvent,
            message: Union[str, Message, MessageSegment] = None,
            **kwargs
    ) -> None:
        await self.send_message(event.player, message)

    async def handle_event(self, event_type: int, data: Any):

        await handle_event(self, event_type, data)

    async def get_occupation(self) -> list:
        response = await self._send_data(3, [])
        if not response:
            raise ActionFailed(F'Failed to get server occupation of the server "{self.self_id}".')
        return [round(float(data), 1) for data in response]

    async def get_player_list(self) -> list:
        response = await self._send_data(1, [])
        if not response:
            raise ActionFailed(F'Failed to get player list of the server "{self.self_id}".')
        return response

    async def get_player_info(self, player_name: str) -> dict:
        response = await self._send_data(2, [player_name])
        if not response:
            raise ActionFailed(F'Failed to get player info of "{player_name}" in the server "{self.self_id}".')
        *coordinate, level, world = response
        return {
            'world': world,
            'level': level,
            'coordinate': coordinate,
        }

    async def execute_command(self, command: str) -> Optional[str]:
        response = await self._send_data(4, [command])
        if not response:
            raise ActionFailed(F'Failed to execute command "{command}" in the server "{self.self_id}".')
        return response[0] if response[0] else None

    async def execute_mcdr_command(self, command: str) -> Optional[str]:
        response = await self._send_data(5, [command])
        if not response:
            raise ActionFailed(F'Failed to execute mcdr command "{command}" in the server "{self.self_id}".')
        return response[0] if response[0] else None

    async def broadcast(self, message: Union[str, Message, MessageSegment]) -> None:
        if isinstance(message, str):
            message = MessageSegment.text(message)
        elif isinstance(message, Message):
            message = message.to_dict()
        await self._send_data(6, [message], False)

    async def send_message(self, player: Union[Player, str], message: Union[str, Message, MessageSegment]) -> None:
        if isinstance(player, Player):
            player = player.name
        if isinstance(message, str):
            message = MessageSegment.text(message)
        elif isinstance(message, Message):
            message = message.to_dict()
        await self._send_data(8, [player, message], False)

    async def _send_data(self, flag: int, data: list, has_response: bool = True) -> Optional[list]:
        await self.websocket.send(dump(flag, data))
        if not has_response: return
        success, response = parse_response(await self.websocket.receive())
        return response if success else None
