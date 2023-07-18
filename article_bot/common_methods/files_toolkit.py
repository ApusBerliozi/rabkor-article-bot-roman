import yaml

from common_entities.bot_replies import BotReplies


def fetch_bot_replies():
    with open("static/bot_replies.yaml", 'r') as file:
        replies = yaml.safe_load(file)
    return BotReplies(**replies)

