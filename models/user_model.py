class UserModel:
    def __init__(self, username, password, balance):
        self.username = username
        self.password = password
        self.balance = balance

    def get_username(self):
        return self.username

    def get_password(self):
        return self.password

    def get_balance(self):
        return self.balance

    def set_balance(self, balance):
        self.balance = balance

    def __str__(self):
        return f"UserModel(username={self.username}, password={self.password}, balance={self.balance})"

    def __repr__(self):
        return f"UserModel(username={self.username}, password={self.password}, balance={self.balance})"
