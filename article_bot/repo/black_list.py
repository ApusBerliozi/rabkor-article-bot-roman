from repo.crud_logic import ArticleBotCrud

from common_entities.logs import logger


def check_blacklist(func):
    """Check whether user is in our black list"""
    async def wrapper(*args):
        cls = args[-1]
        results = ArticleBotCrud().check_user(str(cls.user_id))
        if results:
            return await logger.user_is_banned(user_id=cls.user_id,
                                               first_name=cls.user_first_name,
                                               last_name=cls.user_last_name,
                                               text_message=cls.message_text)
        return await func(*args)
    return wrapper
