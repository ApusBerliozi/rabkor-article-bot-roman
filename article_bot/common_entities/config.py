from dataclasses import dataclass


@dataclass
class Config:
    """Config class, that contains main bot_token, writers_chat_id, and table's name, that contains ids of users
    that are banned"""
    article_bot_token: str
    writers_chat_id: int
    black_list_table: str
    interaction_chat_id: int
    communication_chat_id: int
    user_messages_table: str
    linked_chats_table: str
    chats_ids: list
