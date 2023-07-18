from dataclasses import dataclass


@dataclass
class BotReplies:
    """Config class, that contains main bot_token, writers_chat_id, and table's name, that contains ids of users
    that are banned"""
    greetings: str
    article_received: str
    news_received: str
    you_are_banned: str
    you_are_unbanned: str
    documentation: str
    missing_brackets: str
    empty_message: str
    moderation: str
    easter_egg: str

