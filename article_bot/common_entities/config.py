from dataclasses import dataclass


@dataclass
class Config(object):
    article_bot_token: str
    writers_chat_id: str
    db_client: str
    table_name: str
