import inspect
from functools import wraps

from src.api.enum import NTYPE
from src.config import GLOBAL_CONFIG
from src.core.notification import Event, sender, sys_notification


def fish_ball_trigger(func) -> None:
    @wraps(func)
    def wrapper(*args, **kwargs):
        api = kwargs.get('api', args[0] if len(args) > 0 else None)
        message = kwargs.get('message', args[1] if len(args) > 1 else None)
        if isinstance(message, dict) and 'userName' in message and 'md' in message:
            if message['userName'] == 'sevenSummer' and '天降鱼丸, [0,10] 随机个数. 限时 1 min. 冲鸭~' in message['md']:
                api.chatroom.send(GLOBAL_CONFIG.chat_config.fish_ball)
        return func(*args, **kwargs)
    return wrapper


def at_notification(api, message: dict) -> None:
    if message["userName"] != api.current_user and message["md"].__contains__(f'@{api.current_user}'):
        sender(Event(type=NTYPE.FROM_CHATROOM, sender=message["userName"],
                     content=message['md']), sys_notification)


def kw_notification(api, message: dict) -> None:
    if len(GLOBAL_CONFIG.chat_config.kw_notification) == 0:
        return
    if message["userName"] != api.current_user and any(
            i for i in GLOBAL_CONFIG.chat_config.kw_notification if message["md"].__contains__(i)):
        sender(Event(type=NTYPE.FROM_KEYWORD, sender=message["userName"],
                     content=message['md']), sys_notification)


def notifi(types: list[NTYPE]):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            sig = inspect.signature(func)
            bound_args = sig.bind(*args, **kwargs)
            api = bound_args.arguments.get('api')
            message = bound_args.arguments.get('message')
            for type in types:
                if type == NTYPE.FROM_CHATROOM:
                    at_notification(api, message)
                elif type == NTYPE.FROM_KEYWORD:
                    kw_notification(api, message)
                else:
                    pass
            return func(*args, **kwargs)
        return wrapper
    return decorator
