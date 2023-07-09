import logging

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")


class Logs(object):
    """Logger class. Contains basic setting for loggers and logging process"""
    @staticmethod
    async def user_is_banned(user_id: str, first_name: str, last_name: str, text_message: str) -> None:
        """Informs you that user who is trying to send a message is banned"""
        logging.info(f"Пользователь {first_name} {last_name} с id {user_id} является забаненным. Он пытался отправить следующее сообщение: {text_message}")

    @staticmethod
    async def permission_denied(user_id: str) -> None:
        """Informs you that user that doesn't have permissions tried to use admins' toolkit"""
        logging.info(f"Пользователь с id {user_id} пытался отправлять команды вне админского чата")

    @staticmethod
    def user_was_banned(user_id: str) -> None:
        """Informs you that user was banned"""
        logging.info(f"Пользователь с id {user_id} был забанен")

    @staticmethod
    def user_was_unbanned(user_id: str) -> None:
        """Informs you that user was unbanned"""
        logging.info(f"Пользователь с id {user_id} был разбанен")

    @staticmethod
    def user_sent_article(user_id: str, first_name: str, last_name: str, message: str) -> None:
        """Informs you that user sent an article"""
        logging.info(f"Пользователь {first_name} {last_name} с id {user_id} отправил статью. Текст: {message}")

    @staticmethod
    def admin_replied(user_id: str, first_name: str, last_name: str, message: str) -> None:
        """Informs you that admin replied to user"""
        logging.info(f"Администратор {first_name} {last_name} с id {user_id} ответил пользователю. Текст: {message}")

    @staticmethod
    def empty_message_error(user_id: str) -> None:
        """Informs you that someone tried to send an empty message"""
        logging.error(f"Пользователь {user_id} отправил пустое сообщение")

    @staticmethod
    def brackets_error(user_id: str) -> None:
        """Informs you that someone tried to send an empty message"""
        logging.error(f"Админ {user_id} отправил id пользователя без квадратных скобок")

    @staticmethod
    def swear_words(user_id: str, message: str) -> None:
        """Informs you that user sent a message with swear words"""
        logging.warning(f"Пользователь {user_id} отправил нам сообщение с матом! Вот текст: {message}")

    @staticmethod
    def documentation_was_requested(user_id: str) -> None:
        """Informs you that someone requested documentation"""
        logging.warning(f"Пользователь {user_id} запросил документацию")

    @staticmethod
    def news_were_sent(user_id: str, first_name: str, last_name: str) -> None:
        """Informs you that user sent piece of news"""
        logging.info(f"Пользователь {first_name} {last_name} с id {user_id} отправил нам сообщение с новостями")

    @staticmethod
    def easter_egg_was_found(user_id: str, first_name: str, last_name: str):
        """Informs you that someone had found an easter egg!"""
        logging.info(f"Пользователь {first_name} {last_name} с id {user_id} нашёл пасхальное яйцо! Честь ему и хвала.")


logger = Logs()
