import psycopg2

from config.config import config

from common_entities.errors import UserInBlackList
import boto3


def check_blacklist(func):

    async def wrapper(*args):
        telegram_request = args[-1]
        dynamodb = boto3.client(config.db_client)
        response = dynamodb.query(
            TableName=config.table_name,
            KeyConditionExpression="user_id = :id",
            ExpressionAttributeValues={
                ":id": {"N": str(telegram_request["message"]["from"]["id"])}
            }
        )
        results = response.get('user_id')
        if results:
            raise UserInBlackList
        return await func(*args)
    return wrapper

