from repo.crud_logic import BlackListTable

import common_methods.logs as logger


def check_blacklist(user_id: int):
    results = BlackListTable().check_user(str(user_id))
    if results:
        logger.user_is_banned(user_id=user_id)
    else:
        return "User is clean"
