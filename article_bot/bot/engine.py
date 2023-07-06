from aiogram import Bot

from config.config import config

from common_entities.find_id import find_chat_id

from repo.black_list import check_blacklist


class ArticleBotEngine(object):
    bot = Bot(token=config.article_bot_token)

    def _choose_function(self, message):
        if "document" in message.keys():
            return self._forward_document
        if "text" in message.keys():
            if "/start" in message["text"]:
                return self._greetings
            if "/article" in message["text"]:
                return self._send_article
            if "/reply" in message["text"]:
                return self._reply_to_user
            if "/ban" in message["text"]:
                return self._ban_user
            if "/unban" in message["text"]:
                return self._unban_user

    @check_blacklist
    async def direct_request(self, telegram_request):
        function = self._choose_function(message=telegram_request["message"])
        if function is not None:
            await function(telegram_request["message"])

    async def _greetings(self, telegram_request):
        await self.bot.send_message(chat_id=telegram_request["chat"]["id"],
                                    text="""Здравстуйте! Спасибо что написали нам. \n\nЕсли вы хотите отправить нам текстовое сообщение содержащее статью или ссылку на неё, пожалуйста использзуйте команду /article.
                                    \nЕсли вы хотите отправить нам документ который содержит статью, просто прикрепите его к сообщению.
                                    \nВ случае если мы захотим с вами связаться, наши редакторы ответят вам через бота.""")

    async def _reply_to_user(self, telegram_request):
        chat_id = find_chat_id(message=telegram_request["text"])
        text = telegram_request["text"]
        text = text.replace("/reply", "")
        text = text.replace("["+chat_id+"]", "")
        await self.bot.send_message(chat_id=chat_id,
                                    text=text)

    async def _send_article(self, telegram_request):
        user_first_name = telegram_request["from"]["first_name"]
        user_last_name = telegram_request["from"]["last_name"]
        user_id = telegram_request["from"]["id"]
        chat_id = telegram_request["chat"]["id"]
        message_text = telegram_request["text"]
        message_text = message_text.replace("/article", "")
        await self.bot.send_message(chat_id=chat_id,
                                    text="Спасибо за вашу статью! Наши редакторы обязательно её просмотрят")
        await self.bot.send_message(chat_id=config.writers_chat_id,
                                    text=f"""Нам пишет {user_first_name}, {user_last_name} \nid пользователя [{user_id}] \n
                                    """ + message_text)

    async def _forward_document(self, telegram_request):
        chat_id = telegram_request["chat"]["id"]
        user_first_name = telegram_request["from"]["first_name"]
        user_last_name = telegram_request["from"]["last_name"]
        user_id = telegram_request["from"]["id"]
        await self.bot.send_message(chat_id=chat_id,
                                    text="Спасибо за вашу статью! Наши редакторы обязательно её просмотрят")
        await self.bot.send_message(chat_id=config.writers_chat_id,
                                    text=f"""Нам пишет {user_first_name} {user_last_name} \nid пользователя [{user_id}] \n
                                    """)
        await self.bot.forward_message(chat_id=config.writers_chat_id,
                                       from_chat_id=telegram_request["chat"]["id"],
                                       message_id=telegram_request["message_id"])

    async def _ban_user(self, telegram_request):
        user_id = find_chat_id(message=telegram_request["text"])
        chat_id = find_chat_id(message=telegram_request["text"])
        await self.bot.ban_chat_member(user_id=user_id,
                                       chat_id=chat_id)

    async def _unban_user(self, telegram_request):
        user_id = find_chat_id(message=telegram_request["text"])
        chat_id = find_chat_id(message=telegram_request["text"])
        await self.bot.unban_chat_member(user_id=user_id,
                                         chat_id=chat_id)
