from aiogram.types import Message

from repo.crud_logic import GroupsTable

from config import config


class MessageHandler:
    """Contains functions that work with messages"""

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(MessageHandler, cls).__new__(cls)
        return cls.instance

    @staticmethod
    def find_id(message: str) -> str:
        """Finds user's id that is placed inside [] brackets"""
        chat_id = ""
        index = message.find("[")+1
        while message[index] != "]":
            chat_id = chat_id + message[index]
            index += 1
        return chat_id

    @staticmethod
    def check_group(text: str,
                    message: Message):
        if text == "Письма Б.Ю. Кагарлицкому":
            GroupsTable().change_group(user_id=message.from_user.id,
                                       group_id=config.communication_chat_id,
                                       button_type="Письма Б.Ю.")
            return """<b>Ваши письма важны не только для Бориса, но и для нас. Чтобы отправить ваше письмо редакции:
1) Прикрепите скан с ответом от Б.Ю. Кагарлицкого
2) Текстом укажите ваше письмо, которое вы писали
3) Если вы также отправляли какие-то фото с письмом, то также их прикрепите</b>"""
        elif text == "Фотографии котиков":
            GroupsTable().change_group(user_id=message.from_user.id,
                                       group_id=config.communication_chat_id,
                                       button_type="Фотографии котиков")
            return "Вы выбрали чат с котиками! Отправляйте фотографии своих милых животных сколько угодно"
        elif text == "Отправить статью на публикацию":
            GroupsTable().change_group(user_id=message.from_user.id,
                                       group_id=config.writers_chat_id,
                                       button_type="Статья на публикацию")
            return """<b>Вы хотите отправить вашу статью для публикации на сайте Рабкора.
Прикрепите, пожалуйста, текстовый файл с вашей статьёй. Обязательно также укажите:
1) Как вас подписать (если вы хотите публиковаться анонимно, то также укажите это)
2) Ваши контакты для связи</b>"""
        elif text == "Ваши политические питомцы":
            GroupsTable().change_group(user_id=message.from_user.id,
                                       group_id=config.communication_chat_id,
                                       button_type="Политические питомцы")
            return "<b>Отправьте фото вашего питомца и расскажите немного о нём. Мы обязательно опубликуем!</b>"
        elif text == """Хочу помочь Рабкору""":
            GroupsTable().change_group(user_id=message.from_user.id,
                                       group_id=config.interaction_chat_id,
                                       button_type="Помощь Рабкору")
            return """<b>Мы ценим любую помощь! Если у вас есть возможность помочь финансово, то вы можете перевести любую сумму по следующим реквизитам:
2200700600473069 - Тинькофф
5269880012324208 - Фридом банк (для иностранных переводов) (Kagarlitskaya Kseniia)
Также, можно отправить через Donation Alerts
(https://www.donationalerts.com/r/bkagarlitsky)
Также, имеется патреон
(https://www.patreon.com/freedom_kagarlitsky)
Если же вы хотите помочь Рабкору иначе, то напишите прямо здесь, как бы вы хотели помочь?</b>"""
        elif text == "Обратная связь":
            GroupsTable().change_group(user_id=message.from_user.id,
                                       group_id=config.interaction_chat_id,
                                       button_type="Обратная связь")
            return """<b>Обратная связь - важная часть любой демократизации. Поэтому, если вас что-то не устраивает в работе Рабкора, или вы хотели бы что-то улучшить, то напишите нам прямо сюда.
Предупреждаем: нецензурная брань будет фильтроваться и такие сообщения отправлены не будут!</b>"""
        elif text == "Прочее":
            GroupsTable().change_group(user_id=message.from_user.id,
                                       group_id=config.interaction_chat_id,
                                       button_type="Прочее")
            return """<b>Если ни один из пунктов вам не подошёл, то напишите нам, что бы вы хотели сказать?</b>"""
        else:
            return None
    @staticmethod
    def find_text(message: Message):
        text = ""
        if message.text:
            text = message.text
        elif message.caption:
            text = message.caption
        elif message.reply_to_message:
            text = message.reply_to_message.text
        return text


message_handler = MessageHandler()
