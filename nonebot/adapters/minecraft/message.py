from typing import Type, Iterable
from typing_extensions import override

from nonebot.adapters import Message as BaseMessage
from nonebot.adapters import MessageSegment as BaseMessageSegment


class MessageSegment(BaseMessageSegment["Message"]):
    @classmethod
    @override
    def get_message_class(cls) -> Type["Message"]:
        return Message

    @override
    def __str__(self) -> str:
        return ''.join([data['text'] for data in self.data.values()])

    @override
    def is_text(self) -> bool:
        return True

    @classmethod
    def text(cls, text: str, color: str = None) -> "MessageSegment":
        return cls(type='text', data={'text': text, 'color': color if color else 'white'})


class Message(BaseMessage[MessageSegment]):
    @classmethod
    @override
    def get_segment_class(cls) -> Type[MessageSegment]:
        # 返回适配器的 MessageSegment 类型本身
        return MessageSegment

    @staticmethod
    @override
    def _construct(msg: str) -> Iterable[MessageSegment]:
        # 实现从字符串中构造消息数组，如无字符串嵌入格式可直接返回文本类型 MessageSegment
        return [MessageSegment.text(msg)]

    def to_dict(self):
        # 实现消息数组转 tellraw 格式
        return {'text': [segment.data for segment in self]}
