from repo.crud_logic import ArticleBotCrud

from common_entities.logs import logger


def check_blacklist(func):
    """Check whether user is in our black list"""
    async def wrapper(*args):
        telegram_request = args[-1]
        results = ArticleBotCrud().check_user(str(telegram_request["message"]["from"]["id"]))
        if results:
            return await logger.user_is_banned(user_id=telegram_request["message"]["from"]["id"],
                                               first_name=telegram_request["from"]["first_name"],
                                               last_name=telegram_request["from"]["last_name"],
                                               text_message=telegram_request["message"]["text"])
        return await func(*args)
    return wrapper

