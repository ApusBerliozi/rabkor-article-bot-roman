from repo.crud_logic import ArticleBotCrud

import common_methods.logs as logger


def check_blacklist(user_id: int):
    results = ArticleBotCrud().check_user(str(user_id))
    if results:
        logger.user_is_banned(user_id=user_id)
    else:
        return "User is clean"
