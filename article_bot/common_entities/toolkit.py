
class MessageHandler(object):
    """Contains functions that work with messages"""

    def find_id(self, message: str) -> str:
        """Finds user's id that is placed inside [] brackets"""
        chat_id = ""
        index = message.find("[")+1
        while message[index] != "]":
            chat_id = chat_id + message[index]
            index += 1
        return chat_id


message_handler = MessageHandler()
