from dataclasses import dataclass


@dataclass
class BotReplies:
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

