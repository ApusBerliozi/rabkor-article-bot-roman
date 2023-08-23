import logging

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")


def user_is_banned(user_id: str) -> None:
    """Informs you that user who is trying to send a message is banned"""
    logging.info(f"Пользователь с id {user_id} является забаненным.")


async def permission_denied(user_id: str) -> None:
    """Informs you that user that doesn't have permissions tried to use admins' toolkit"""
    logging.info(f"Пользователь с id {user_id} пытался отправлять команды вне админского чата")


def user_was_banned(user_id: str) -> None:
    """Informs you that user was banned"""
    logging.info(f"Пользователь с id {user_id} был забанен")


def user_was_unbanned(user_id: str) -> None:
    """Informs you that user was unbanned"""
    logging.info(f"Пользователь с id {user_id} был разбанен")


def user_sent_article(user_id: str, first_name: str, last_name: str) -> None:
    """Informs you that user sent an article"""
    logging.info(f"Пользователь {first_name} {last_name} с id {user_id} отправил статью.")


def admin_replied(user_id: str, first_name: str) -> None:
    """Informs you that admin replied to user"""
    logging.info(f"Администратор ответил пользователю {first_name}  с id {user_id} .")


def empty_message_error(user_id: str) -> None:
    """Informs you that someone tried to send an empty message"""
    logging.error(f"Пользователь {user_id} отправил пустое сообщение")


def brackets_error(user_id: str) -> None:
    """Informs you that someone tried to send an empty message"""
    logging.error(f"Админ {user_id} отправил id пользователя без квадратных скобок")


def swear_words(user_id: str, message: str) -> None:
    """Informs you that user sent a message with swear words"""
    logging.warning(f"Пользователь {user_id} отправил нам сообщение с матом! Вот текст: {message}")


def documentation_was_requested(user_id: str) -> None:
    """Informs you that someone requested documentation"""
    logging.warning(f"Пользователь {user_id} запросил документацию")


def news_were_sent(user_id: str, first_name: str, last_name: str) -> None:
    """Informs you that user sent piece of news"""
    logging.info(f"Пользователь {first_name} {last_name} с id {user_id} отправил нам сообщение с новостями")


def easter_egg_was_found(user_id: str, first_name: str, last_name: str):
    """Informs you that someone had found an easter egg!"""
    logging.info(f"Пользователь {first_name} {last_name} с id {user_id} нашёл пасхальное яйцо! Честь ему и хвала.")

