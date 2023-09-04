import typing

import boto3

from config import config


class BlackListTable:
    """Allows us to execute crud logic with dynamodb table"""
    dynamodb = boto3.client("dynamodb")

    def ban_user(self, user_id: int) -> None:
        """Places user's id inside black list's table"""
        item = {"user_id": {"N": user_id}}
        self.dynamodb.put_item(
            TableName=config.black_list_table,
            Item=item
        )

    def unban_user(self, user_id: int) -> None:
        """Removes user's id from black list's table"""
        self.dynamodb.delete_item(
            TableName=config.black_list_table,
            Key={
                "user_id": {"N": user_id}
            }
        )

    def check_user(self, user_id: str) -> typing.Optional[dict]:
        """Checks whether user's id inside black list's table"""
        response = self.dynamodb.get_item(
            TableName=config.black_list_table,
            Key={
                "user_id": {"N": user_id}
            }
        )
        return response.get("Item")


class GroupsTable:
    dynamodb = boto3.client("dynamodb")
    primary_key = "user_id"
    group_id = "group_id"
    button = "button"

    def create_new_user(self, user_id: str) -> None:
        """Creates new record of user with fake id"""
        item = {self.primary_key: {"S": str(user_id)},
                self.group_id: {"S": "-1001892897937"},
                self.button: {"S": "Прочее"}}
        self.dynamodb.put_item(
            TableName=config.linked_chats_table,
            Item=item
        )

    def change_group(self, user_id: int, group_id: int, button_type: str) -> typing.Optional[dict]:
        """Change group to which user will write"""
        update_expression = f'SET {self.group_id} = :new_group_value, {self.button} = :new_button_value'
        expression_attribute_values = {
            ':new_group_value': {"S": str(group_id)},
            ':new_button_value': {"S": button_type}
        }
        response = self.dynamodb.update_item(
            TableName=config.linked_chats_table,
            Key={
                self.primary_key: {'S': str(user_id)}
            },
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_attribute_values
        )
        return response

    def get_group_id(self, user_id):
        response = self.dynamodb.get_item(
            TableName=config.linked_chats_table,
            Key={
                self.primary_key: {"S": str(user_id)}
            }
        )
        response = response.get("Item")
        group_id = response["group_id"]["S"]
        button = response["button"]["S"]
        return {"group_id": group_id,
                "button": button}


class MessageTable:
    dynamodb = boto3.client("dynamodb")
    primary_key = "message_id"
    user_id = "user_id"

    def create_new_message(self, user_id: str, message_id: str) -> None:
        """Creates new record of user with fake id"""
        item = {self.primary_key: {"S": str(message_id)},
                self.user_id: {"S": str(user_id)}}
        self.dynamodb.put_item(
            TableName=config.user_messages_table,
            Item=item
        )

    def get_user_id(self, message_id: str) -> typing.Optional[dict]:
        """Checks whether user's id inside black list's table"""
        print("Vot takoy message id " + str(message_id))
        response = self.dynamodb.get_item(
            TableName=config.user_messages_table,
            Key={
                self.primary_key: {"S": str(message_id)}
            }
        )
        response = response.get("Item")
        user_id = response["user_id"]["S"]
        return user_id
