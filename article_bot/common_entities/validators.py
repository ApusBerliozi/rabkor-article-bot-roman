from common_entities.logs import logger
from config import config


def check_admin_message(func):
    """Ensures that admins had sent a proper message to the bot"""
    async def wrapper(*args):
        cls = args[-1]
        if str(cls.user_chat_id) != config.writers_chat_id:
            return await logger.permission_denied(user_id=cls.user_id)
        if cls.message_text == "" or cls.message_text == len(cls.message_text) * cls.message_text[0]:
            return await cls._empty_message()
        open_bracket = cls.message_text.find("[")
        close_bracket = cls.message_text.find("]")
        if close_bracket == -1 or open_bracket == -1:
            return await cls._missing_brackets()
        return await func(*args)
    return wrapper


def check_user_message(func):
    """Ensures that user had sent a message that doesn't contain Russian swear words in the writers' chat"""
    async def wrapper(*args):
        swear_list = ["хуй",
                      "пизд",
                      "трах",
                      "еба",
                      "сука",
                      "суки",
                      "долбоёб",
                      "долбое",
                      "пидр",
                      "пидар",
                      "залупа",
                      "сраный",
                      "жопа",
                      "пенис",
                      "хер",
                      "хрен",
                      "ебля",
                      "ссаный",
                      "обосраный",
                      "срань",
                      "ёба"]
        cls = args[-1]
        if cls.message_text:
            if cls.message_text == "" or cls.message_text == len(cls.message_text) * cls.message_text[0]:
                return await cls._empty_message()
            for word in swear_list:
                if word in cls.message_text:
                    return await cls._moderate()
            return await func(*args)
        elif cls.caption_text:
            for word in swear_list:
                if word in cls.message_text:
                    return await cls._moderate()
        return await func(*args)
    return wrapper
