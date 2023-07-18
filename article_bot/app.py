import json
import asyncio

from aiogram import types

from repo.black_list import check_blacklist
from bot.engine import dp


def lambda_handler(event, context):
    """Request from telegram is passed to this function, and then it is
    redirected to bot itself, which will proceed it, and either return 200 or any error"""
    content = json.loads(event["body"])
    if "message" in content.keys():
        if check_blacklist(user_id=content["message"]["from"]["id"]):
            update = types.Update(**content)
            asyncio.run(dp.process_update(update))
    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "OK"
        }),
    }
