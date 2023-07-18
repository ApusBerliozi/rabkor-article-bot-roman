from dataclasses import dataclass


@dataclass
class Config:
    """Config class, that contains main bot_token, writers_chat_id, and table's name, that contains ids of users
    that are banned"""
    article_bot_token: str
    writers_chat_id: str
    news_chat_id: str
    table_name: str
