import json
import asyncio
from bot.engine import ArticleBotEngine


def lambda_handler(event, context):
    """Request from telegram is passed to this function, and then it is
    redirected to bot itself, which will proceed it, and either return 200 or any error"""
    print(json.loads(event["body"]))
    content = json.loads(event["body"])
    if "message" in content.keys():
        asyncio.run(ArticleBotEngine(content).direct_request())
    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "OK"
        }),
    }
