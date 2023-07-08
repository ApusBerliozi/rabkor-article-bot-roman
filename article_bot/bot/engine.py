from aiogram import Bot

from config import config

from common_entities.toolkit import message_handler

from repo.black_list import check_blacklist

from repo.crud_logic import ArticleBotCrud

from common_entities.validators import check_admin_message

from common_entities.validators import censure_message

from common_entities.logs import logger


class ArticleBotEngine(object):
    """Contains methods for proper bot's functioning. Communicates with outter wordspace via direct_request method.
    In order to initiate class properly, requires telegram_request object, that is basicly a message which is sent by telegram
    as POST request."""
    def __init__(self, telegram_request: dict):
        self.bot = Bot(token=config.article_bot_token)
        self.crud_logic = ArticleBotCrud()
        self.message = telegram_request["message"]
        self.user_chat_id = telegram_request["chat"]["id"]
        self.user_id = telegram_request["from"]["id"]
        self.user_first_name = telegram_request["from"]["first_name"]
        self.user_last_name = telegram_request["from"]["last_name"]
        self.message_text = telegram_request["message"]["text"] if "text" in self.message.keys() else ""
        self.message_id = telegram_request["message_id"]
        self.functions_mapper = {"/start": self._greetings,
                                 "/article": self._send_article,
                                 "/reply": self._reply_to_user,
                                 "/ban": self._ban_user,
                                 "/unban": self._unban_user,
                                 "/help_admin_12": self._documentation}

    @check_blacklist
    async def direct_request(self) -> None:
        """Define which function will be called by searching for commands (that are keys in self.functions_mapper) in
        message's text."""
        if "document" in self.message.keys() and self.user_chat_id != config.writers_chat_id:
            await self._forward_document()
        if "text" in self.message.keys():
            for key in self.functions_mapper:
                if key in self.message_text:
                    func = self.functions_mapper.get(key)
                    await func()

    async def _greetings(self) -> None:
        """This function sends greetings message with instructions about communication with admins"""
        await self.bot.send_message(chat_id=self.user_chat_id,
                                    text="""Здравстуйте! Спасибо что написали нам. \n\nЕсли вы хотите отправить нам текстовое сообщение содержащее статью или ссылку на неё, пожалуйста используйте команду /article.
                                    \nЕсли вы хотите отправить нам документ который содержит статью, просто прикрепите его к сообщению.
                                    \nВ случае если мы захотим с вами связаться, наши редакторы ответят вам через бота.
                                    \n Пожалуйста, воздержитесь от метарных слов, в противном случае ваше сообщение не будет отправлено""")

    @check_admin_message
    async def _reply_to_user(self) -> None:
        """This function allows admins' communication with user"""
        chat_id = message_handler.find_id(message=self.message_text)
        text = self.message_text
        text = text.replace("/reply", "")
        text = text.replace("["+chat_id+"]", "")
        await self.bot.send_message(chat_id=chat_id,
                                    text=text)

    @censure_message
    async def _send_article(self) -> None:
        """This function sends article to the writers' chat"""

        message_text = self.message_text
        message_text = message_text.replace("/article", "")
        await self.bot.send_message(chat_id=self.user_chat_id,
                                    text="Спасибо за вашу статью! Наши редакторы обязательно её просмотрят")
        await self.bot.send_message(chat_id=config.writers_chat_id,
                                    text=f"""Нам пишет {self.user_first_name}, {self.user_last_name} \nid пользователя [{self.user_id}] \n
                                    """ + message_text)
        logger.user_sent_article(user_id=self.user_id,
                                 first_name=self.user_first_name,
                                 last_name=self.user_last_name,
                                 message=self.message_text)

    @censure_message
    async def _forward_document(self) -> None:
        """This function forwards document with article from user to the writers' chat"""
        await self.bot.send_message(chat_id=self.user_chat_id,
                                    text="Спасибо за вашу статью! Наши редакторы обязательно её просмотрят")
        await self.bot.send_message(chat_id=config.writers_chat_id,
                                    text=f"""Нам пишет {self.user_first_name} {self.user_last_name} \nid пользователя [{self.user_id}] \n
                                    """)
        await self.bot.forward_message(chat_id=config.writers_chat_id,
                                       from_chat_id=self.user_chat_id,
                                       message_id=self.message_id)

    @check_admin_message
    async def _ban_user(self) -> None:
        """This function bans user"""
        user_id = message_handler.find_id(message=self.message_text)
        self.crud_logic.ban_user(user_id=user_id)
        logger.user_was_banned(user_id=user_id)
        await self.bot.send_message(chat_id=user_id,
                                    text="Вы были забанены сообществом Рабкор за нарушение правил. Возможность присылать статьи отключена")

    @check_admin_message
    async def _unban_user(self) -> None:
        """This function unbans user"""
        user_id = message_handler.find_id(message=self.message_text)
        self.crud_logic.unban_user(user_id=user_id)
        logger.user_was_unbanned(user_id=user_id)
        await self.bot.send_message(chat_id=user_id,
                                    text="Вы были разбанены сообществом Рабкор. Возможность присылать статьи вновь доступна.")

    async def _documentation(self) -> None:
        """This function sends documentation in the writers chat"""

        logger.user_sent_article(user_id=self.user_id,
                                 first_name=self.user_first_name,
                                 last_name=self.user_last_name,
                                 message=self.message_text if self.message_text else "Документ был отправлен без сопроводительного текста")
        await self.bot.send_message(chat_id=config.writers_chat_id,
                                    text="""Доступные команды:
                                    /start - Стартовое приветствие пользователя
                                    /ban - Забанить пользователя. id нужно разместить в [] скобках (например [11111111])
                                    /unban - Разбанить пользователя. id также необходимо поместить в квадратные скобки
                                    /reply - Ответить пользователю. id необходимо разместить в квадратные скобки
                                    /help_admin_12 - Получить данное сообщение повторно.""")

    async def _missing_brackets(self) -> None:
        """This function reminds to the admins that inorder to communicate with user, they should enclose they id in square brackets"""
        await self.bot.send_message(chat_id=config.writers_chat_id,
                                    text="Пожалуйста, поместите id пользователя в квадратные скобки (например [11123231])")

    async def _empty_message(self) -> None:
        """This function reminds to the admins that they shouldn't send empty message"""
        await self.bot.send_message(chat_id=config.writers_chat_id,
                                    text="Пожалуйста не отправляйте пустое сообщение")

    async def _censure(self) -> None:
        """This function prevents user from sending message that contains swear words, and reminds them to use correct language."""
        await self.bot.send_message(chat_id=self.user_chat_id,
                                    text="Пожалуйста воздрежитесь от применения матерных слов. Мы понимаем что текущая остановка может провоцировать, но давайте оставаться в рамках")
