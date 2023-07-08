from logging import log


class Logs(object):
    """Logger class. Contains basic setting for loggers and logging process"""
    logger = ...

    async def user_is_banned(self, user_id: str, first_name: str, last_name: str, text_message: str) -> None:
        """Informs you that user who is trying to send a message is banned"""
        ...

    def user_was_banned(self, user_id: str) -> None:
        """Informs you that user was banned"""
        ...

    def user_was_unbanned(self, user_id: str) -> None:
        """Informs you that user was unbanned"""
        ...

    def user_sent_article(self, user_id: str, first_name: str, last_name: str, message: str) -> None:
        """Informs you that user sent an article"""
        ...

    def admin_replied(self, user_id: str, first_name: str, last_name: str, message: str) -> None:
        """Informs you that admin replied to user"""
        ...


logger = Logs()

