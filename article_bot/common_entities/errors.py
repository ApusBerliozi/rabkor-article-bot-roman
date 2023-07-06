class UserInBlackList(Exception):
    def __init__(self):
        self.message = "User in the blacklist"
