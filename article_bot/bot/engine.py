import re

from aiogram import Bot, Dispatcher, types
from aiogram.types import ContentTypes, ChatType
from aiogram.types import Message

from config import config
from repo.crud_logic import BlackListTable, MessageTable, GroupsTable
import common_methods.logs as logger
from common_methods.message_toolkit import message_handler
from common_methods.files_toolkit import fetch_bot_replies

bot: Bot = Bot(token=config.article_bot_token)
dp: Dispatcher = Dispatcher(bot)
moderation: BlackListTable = BlackListTable()
bot_replies: callable = fetch_bot_replies()
kb: list[list[types.KeyboardButton]] = [
        [types.KeyboardButton(text="Письма Б.Ю. Кагарлицкому")],
        [types.KeyboardButton(text="Отправить статью на публикацию")],
        [types.KeyboardButton(text="Ваши политические питомцы")],
        [types.KeyboardButton(text="Хочу помочь Рабкору")],
        [types.KeyboardButton(text="Обратная связь")],
        [types.KeyboardButton(text="Прочее")]]

keyboard: types.ReplyKeyboardMarkup = types.ReplyKeyboardMarkup(keyboard=kb,
                                                                resize_keyboard=True)


async def moderate(message: Message) -> None:
    """This function prevents user from sending message that contains swear words, and reminds them to use correct language."""
    await bot.send_message(chat_id=message.from_user.id,
                           text=bot_replies.moderation)
    logger.swear_words(user_id=message.from_user.id, message=message.caption)


async def easter_egg(message: Message) -> None:
    """This is an easter egg for eager users!"""
    await bot.send_message(chat_id=message.from_user.id,
                           text=bot_replies.easter_egg)
    logger.easter_egg_was_found(user_id=message.from_user.id,
                                first_name=message.from_user.first_name,
                                last_name=message.from_user.last_name)


async def check_user_message(message: Message, text: str | None):
    """Ensures that user had sent a message that doesn't contain Russian swear words in the writers' chat"""
    with open("static/bad_words", "r") as file:
        swear_list = file.read().splitlines()
    if text:
        text = text.lower()
        for word in re.findall(r'\w+', text):
            if word in swear_list:
                await moderate(message=message)
                return "Error"


@dp.message_handler(commands=['start'])
async def greetings(message: Message) -> None:
    """This function sends greetings message with instructions about communication with admins"""
    if str(message.chat.id) not in config.chats_ids:
        GroupsTable().create_new_user(user_id=message.from_user.id)
        await bot.send_message(chat_id=message.from_user.id,
                               text=bot_replies.greetings,
                               reply_markup=keyboard)
    return


async def reply_to_user(message: Message) -> None:
    """This function allows admins' communication with user"""
    user_id = MessageTable().get_user_id(message_id=message.reply_to_message.message_id)
    await bot.copy_message(chat_id=user_id,
                           from_chat_id=message.chat.id,
                           message_id=message.message_id)
    logger.admin_replied(user_id=message.from_user.id,
                         first_name=message.from_user.first_name)


@dp.message_handler(content_types=[*ContentTypes.DOCUMENT,
                                   *ContentTypes.AUDIO,
                                   *ContentTypes.VIDEO,
                                   *ContentTypes.PHOTO,
                                   *ContentTypes.VOICE,
                                   *ContentTypes.VIDEO_NOTE,
                                   *ContentTypes.TEXT])
async def message_regulator(message: Message) -> None:
    """This function sends article to the editors' chat"""
    text: str = message_handler.find_text(message=message)
    if answer := message_handler.check_group(message=message,
                                             text=text):
        await send_button_message(chat_id=message.from_user.id, text=answer)
        return
    if "/ban" in text and str(message.chat.id) in config.chats_ids and message.reply_to_message.from_user.is_bot is True:
        await ban_user(message=message)
        return
    elif "/unban" in text and str(message.chat.id) in config.chats_ids and message.reply_to_message.from_user.is_bot is True:
        await unban_user(message=message)
        return
    elif message.reply_to_message \
            and str(message.chat.id) in config.chats_ids \
            and message.reply_to_message.from_user.is_bot is True\
            and not message.voice\
            and not message.video_note:
        await reply_to_user(message=message)
        return
    elif "/help_admin" in text and str(message.chat.id) in config.chats_ids:
        await documentation(message=message)
        return
    elif str(message.chat.id) not in config.chats_ids:
        await communicate_with_admins(message=message)
        return


async def send_button_message(chat_id, text):
    await bot.send_message(chat_id=chat_id,
                           text=text,
                           parse_mode="HTML")


async def communicate_with_admins(message: Message) -> str | None:
    """This function forwards document with article from user to the editors' chat"""
    text = ""
    if message.text:
        text = message.text
    elif message.caption:
        text = message.caption
    error = await check_user_message(message=message, text=text)
    if error:
        return
    table_response = GroupsTable().get_group_id(user_id=message.from_user.id)
    button_type = table_response.get("button")
    group_id = table_response.get("group_id")
    await bot.send_message(chat_id=message.from_user.id,
                           text=bot_replies.article_received)
    await bot.send_message(chat_id=group_id,
                           text=f"Нам пишет <b>{message.from_user.first_name}, {button_type}</b>",
                           parse_mode="HTML")
    message_id = await bot.copy_message(chat_id=group_id,
                                        from_chat_id=message.from_user.id,
                                        message_id=message.message_id)
    MessageTable().create_new_message(user_id=message.from_user.id,
                                      message_id=message_id.message_id)
    logger.user_sent_article(user_id=message.from_user.id,
                             first_name=message.from_user.first_name,
                             last_name=message.from_user.last_name)


async def ban_user(message: Message) -> None:
    """This function bans user"""
    user_id = MessageTable().get_user_id(message_id=message.reply_to_message.message_id)
    moderation.ban_user(user_id=user_id)
    await bot.send_message(chat_id=user_id,
                           text=bot_replies.you_are_banned)
    logger.user_was_banned(user_id=user_id)


async def unban_user(message: Message) -> None:
    """This function unbans user"""
    user_id = MessageTable().get_user_id(message_id=message.reply_to_message.message_id)
    moderation.unban_user(user_id=user_id)
    await bot.send_message(chat_id=user_id,
                           text=bot_replies.you_are_unbanned)
    logger.user_was_unbanned(user_id=user_id)


@dp.message_handler(commands=['help_admin'])
async def documentation(message: Message) -> None:
    """This function sends documentation in the editors' chat"""
    await bot.send_message(chat_id=config.writers_chat_id,
                           text=bot_replies.documentation)
    logger.documentation_was_requested(user_id=message.from_user.id)


