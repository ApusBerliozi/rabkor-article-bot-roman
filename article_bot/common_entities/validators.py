
def check_admin_message(func):
    """Ensures that admins had sent a proper message to the bot"""
    async def wrapper(*args):
        cls = args[-1]
        message = cls.message_text
        if message == len(message) * message[0]:
            return await cls._empty_message()
        open_bracket = message.find("[")
        close_bracket = message.find("]")
        if close_bracket == -1:
            return await cls._missing_brackets()
        if open_bracket == -1:
            return await cls._missing_brackets()
        return await func(*args)
    return wrapper


def censure_message(func):
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
        message = cls.message_text
        for word in swear_list:
            if word in message:
                return await cls._censure()
        return await func(*args)
    return wrapper
