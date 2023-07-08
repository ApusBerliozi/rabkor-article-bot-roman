import typing

import boto3

from config import config


class ArticleBotCrud(object):
    """Allows us to execute crud logic with dynamodb table"""
    dynamodb = boto3.client("dynamodb")

    def ban_user(self, user_id: int) -> None:
        """Places user's id inside black list's table"""
        item = {"user_id": {"N": user_id}}
        response = self.dynamodb.put_item(
            TableName=config.table_name,
            Item=item
        )

    def unban_user(self, user_id: int) -> None:
        """Removes user's id from black list's table"""
        response = self.dynamodb.delete_item(
            TableName=config.table_name,
            Key={
                "user_id": {"N": user_id}
            }
        )

    def check_user(self, user_id: str) -> typing.Optional[dict]:
        """Checks whether user's id inside black list's table"""
        response = self.dynamodb.query(
            TableName=config.table_name,
            KeyConditionExpression="user_id = :id",
            ExpressionAttributeValues={":id": {"N": user_id}}
        )
        return response.get("Items")
