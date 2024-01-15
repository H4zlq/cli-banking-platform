class User:
    def __init__(self, id, username, password, account_type_id, balance):
        self.id = id
        self.username = username
        self.password = password
        self.account_type_id = account_type_id
        self.balance = balance

    def get_id(self):
        return self.id

    def get_username(self):
        return self.username

    def get_password(self):
        return self.password

    def get_account_type_id(self):
        return self.account_type_id

    def get_balance(self):
        return self.balance

    def __str__(self):
        return f"UserModel(id={self.id}, username={self.username}, password={self.password}, balance={self.balance})"

    def __repr__(self) -> str:
        return self.__str__()
