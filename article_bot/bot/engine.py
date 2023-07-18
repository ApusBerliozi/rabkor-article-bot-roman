import re

from aiogram import Bot, Dispatcher
from aiogram.types import ContentType
from aiogram.types import Message

from config import config
from repo.crud_logic import ArticleBotCrud
import common_methods.logs as logger
from common_methods.message_toolkit import message_handler
from common_methods.files_toolkit import fetch_bot_replies

bot = Bot(token=config.article_bot_token)
dp = Dispatcher(bot)
crud_logic = ArticleBotCrud()
bot_replies = fetch_bot_replies()


async def missing_brackets(message: Message) -> None:
    """This function reminds to the admins that inorder to communicate with user, they should enclose they id in square brackets"""
    await bot.send_message(chat_id=config.writers_chat_id,
                           text=bot_replies.missing_brackets)
    logger.brackets_error(user_id=message.from_user.id)


async def empty_message(message: Message) -> None:
    """This function reminds to the admins that they shouldn't send empty message"""
    await bot.send_message(chat_id=message.from_user.id,
                           text=bot_replies.empty_message)
    logger.empty_message_error(user_id=message.from_user.id)


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


async def check_admin_message(message: Message, text: str):
    """Ensures that admins had sent a proper message to the bot"""
    if str(message.chat.id) != config.writers_chat_id:
        await logger.permission_denied(user_id=message.from_user.id)
        return "Error"
    if text == "" or text == len(text) * text[0]:
        await empty_message(message=message)
        return "Error"
    open_bracket = text.find("[")
    close_bracket = text.find("]")
    if close_bracket == -1 or open_bracket == -1:
        await missing_brackets(message=message)
        return "Error"


async def check_user_message(message: Message, text: str):
    """Ensures that user had sent a message that doesn't contain Russian swear words in the writers' chat"""
    with open("static/bad_words", "r") as file:
        swear_list = file.read().splitlines()
    if text:
        if text == "" or text == len(text) * text[0]:
            await empty_message(message=message)
            return "Error"
        text = text.lower()
        for word in re.findall(r'\w+', text):
            if word in swear_list:
                await moderate(message=message)
                return "Error"


@dp.message_handler(commands=['start'])
async def greetings(message: Message) -> None:
    """This function sends greetings message with instructions about communication with admins"""
    await bot.send_message(chat_id=message.chat.id,
                           text=bot_replies.greetings)


@dp.message_handler(commands=['reply'])
async def reply_to_user(message: Message) -> None:
    """This function allows admins' communication with user"""
    text = message.text.replace("/reply", "")
    error = await check_admin_message(message=message, text=text)
    if error:
        return None
    chat_id = message_handler.find_id(message=message.text)
    text = text.replace("["+chat_id+"]", "")
    await bot.send_message(chat_id=chat_id,
                           text=text)
    logger.admin_replied(user_id=message.from_user.id,
                         first_name=message.from_user.first_name,
                         last_name=message.from_user.last_name,
                         message=text)


@dp.message_handler(commands=["article"])
async def send_article(message: Message) -> None:
    """This function sends article to the editors' chat"""
    text = message.text.replace("/article", "")
    error = await check_user_message(message=message, text=text)
    if error:
        return None
    await bot.send_message(chat_id=message.from_user.id,
                           text=bot_replies.article_received)
    await bot.send_message(chat_id=config.writers_chat_id,
                           text=f"Нам пишет {message.from_user.first_name} {message.from_user.last_name} \n"\
                                f"ID пользователя <b>[{message.from_user.id}]</b> \n" + text,
                           parse_mode="HTML")
    logger.user_sent_article(user_id=message.from_user.id,
                             first_name=message.from_user.first_name,
                             last_name=message.from_user.last_name)


@dp.message_handler(content_types=ContentType.DOCUMENT)
async def forward_document(message: Message) -> None:
    """This function forwards document with article from user to the editors' chat"""
    error = await check_user_message(message=message, text=message.caption)
    if error:
        return None
    await bot.send_message(chat_id=message.from_user.id,
                           text=bot_replies.article_received)
    await bot.send_message(chat_id=config.writers_chat_id,
                           text=f"Нам пишет {message.from_user.first_name} {message.from_user.last_name} \n"\
                                f"ID пользователя <b>[{message.from_user.id}]</b> \n",
                           parse_mode="HTML")
    await bot.forward_message(chat_id=config.writers_chat_id,
                              from_chat_id=message.from_user.id,
                              message_id=message.message_id)
    logger.user_sent_article(user_id=message.from_user.id,
                             first_name=message.from_user.first_name,
                             last_name=message.from_user.last_name)


@dp.message_handler(commands=['ban'])
async def ban_user(message: Message) -> None:
    """This function bans user"""
    error = await check_admin_message(message=message,
                                      text=message.text)
    if error:
        return None
    user_id = message_handler.find_id(message=message.text)
    crud_logic.ban_user(user_id=user_id)
    await bot.send_message(chat_id=user_id,
                           text=bot_replies.you_are_banned)
    logger.user_was_banned(user_id=user_id)


@dp.message_handler(commands=['unban'])
async def unban_user(message: Message) -> None:
    """This function unbans user"""
    error = await check_admin_message(message=message, text=message.text)
    if error:
        return None
    user_id = message_handler.find_id(message=message.text)
    crud_logic.unban_user(user_id=user_id)
    await bot.send_message(chat_id=user_id,
                           text=bot_replies.you_are_unbanned)
    logger.user_was_unbanned(user_id=user_id)


@dp.message_handler(commands='help_admin')
async def documentation(message: Message) -> None:
    """This function sends documentation in the editors' chat"""
    await bot.send_message(chat_id=config.writers_chat_id,
                           text=bot_replies.documentation)
    logger.documentation_was_requested(user_id=message.from_user.id)


@dp.message_handler(commands=["news"])
async def send_news(message: Message) -> None:
    """This function sends received piece of news to admin"""
    text = message.text.replace("/news", "")
    error = await check_user_message(message=message, text=text)
    if error:
        return None
    await bot.send_message(chat_id=message.from_user.id,
                           text=bot_replies.news_received)
    await bot.send_message(chat_id=config.news_chat_id,
                           text=f"Нам пишет {message.from_user.first_name} {message.from_user.last_name} \n"\
         f"ID пользователя <b>[{message.from_user.id}]</b> \n" + text,
                           parse_mode="HTML")
    logger.news_were_sent(user_id=message.from_user.id,
                          first_name=message.from_user.first_name,
                          last_name=message.from_user.last_name)

