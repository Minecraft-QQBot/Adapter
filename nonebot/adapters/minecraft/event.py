from uuid import UUID
from typing_extensions import Optional, Union, override
from pydantic import BaseModel

from nonebot.adapters import Event as BaseEvent

from .message import MessageSegment, Message


class Player(BaseModel):
    name: str
    uuid: Optional[UUID]


class ServerEvent(BaseEvent):
    server_name: str  # 服务器名称

    def get_type(self) -> str:
        return 'notice'

    def is_tome(self) -> bool:
        pass

    def get_message(self) -> "Message":
        pass

    def get_session_id(self) -> str:
        pass

    def get_user_id(self) -> str:
        pass

    def get_event_description(self) -> str:
        pass

    def get_event_name(self) -> str:
        pass


class ServerStartedEvent(ServerEvent):

    def get_event_name(self) -> str:
        return 'ServerStartedEvent'

    @override
    def get_event_description(self) -> str:
        return F'Server "{self.server_name}" has started.'


class ServerShuttingEvent(ServerEvent):
    def get_event_name(self) -> str:
        return 'ServerShuttingEvent'

    @override
    def get_event_description(self) -> str:
        return F'Server "{self.server_name}" has shut down.'


class PlayerEvent(BaseEvent):
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
        raise ValueError('PlayerEvent has no message!')

    @override
    def get_session_id(self) -> str:
        # 获取事件会话 ID 的方法，根据事件具体实现，如果事件没有相关 ID，则抛出异常
        raise ValueError('PlayerEvent has no session ID!')

    @override
    def is_tome(self) -> bool:
        # 判断事件是否和机器人有关
        return False


class PlayerLeftEvent(PlayerEvent):
    def get_type(self) -> str:
        return 'notice'

    def get_event_name(self) -> str:
        return 'PlayerLeftEvent'

    @override
    def get_event_description(self) -> str:
        return F'{self.player.name} left the server "{self.server_name}".'


class PlayerDeathEvent(PlayerEvent):
    def get_type(self) -> str:
        return 'notice'

    def get_event_name(self) -> str:
        return 'PlayerDeathEvent'

    @override
    def get_event_description(self) -> str:
        return F'{self.player.name} died in the server "{self.server_name}".'


class PlayerJoinedEvent(PlayerEvent):
    def get_type(self) -> str:
        return 'notice'

    def get_event_name(self) -> str:
        return 'PlayerJoinedEvent'

    @override
    def get_event_description(self) -> str:
        return F'{self.player.name} joined the server "{self.server_name}".'


class PlayerMessageEvent(PlayerEvent):
    message: Union[MessageSegment, Message]  # 服务器发送的消息

    def get_type(self) -> str:
        return 'message'

    @override
    def get_message(self):
        return self.message

    @override
    def get_event_description(self) -> str:
        return F'{self.player.name} sent a message to the server "{self.server_name}": {self.message}'
