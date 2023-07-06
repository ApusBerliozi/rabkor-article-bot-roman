
def find_chat_id(message: str) -> str:
    chat_id = ""
    index = message.find("[")+1
    while message[index]!="]":
        chat_id = chat_id + message[index]
        index += 1
    return chat_id
