from uuid import UUID
from typing_extensions import override
from pydantic import BaseModel

from nonebot.adapters import Event as BaseEvent


class Player(BaseModel):
    name: str
    uuid: UUID


class Event(BaseEvent):
    player: Player  # 玩家对象
    server_name: str  # 服务器名称

    def get_type(self) -> str:
        pass

    def get_event_description(self) -> str:
        pass

    @override
    def get_event_name(self) -> str:
        # 返回事件的名称，用于日志打印
        pass

    @override
    def get_user_id(self) -> str:
        # 获取用户 ID 的方法，根据事件具体实现，如果事件没有用户 ID，则抛出异常
        return self.player.uuid.hex

    @override
    def get_message(self):
        # 获取事件消息的方法，根据事件具体实现，如果事件非消息类型事件，则抛出异常
        raise ValueError('Event has no message!')

    @override
    def get_session_id(self) -> str:
        # 获取事件会话 ID 的方法，根据事件具体实现，如果事件没有相关 ID，则抛出异常
        raise ValueError('Event has no session ID!')

    @override
    def is_tome(self) -> bool:
        # 判断事件是否和机器人有关
        return False


class PlayerLeftEvent(Event):
    def get_type(self) -> str:
        return 'notice'

    def get_event_name(self) -> str:
        return 'PlayerLeftEvent'

    @override
    def get_event_description(self) -> str:
        return F'{self.player.name} left the server "{self.server_name}".'


class PlayerJoinedEvent(Event):
    def get_type(self) -> str:
        return 'notice'

    def get_event_name(self) -> str:
        return 'PlayerJoinedEvent'

    @override
    def get_event_description(self) -> str:
        return F'{self.player.name} joined the server "{self.server_name}".'


class PlayerMessageEvent(Event):
    message: str  # 玩家发送的消息
