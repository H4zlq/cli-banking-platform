from services.user_service import UserService


class UserController:
    user_service = UserService()

    def __init__(self):
        super().__init__()

    def get_user(self, username):
        return self.user_service.get_user(username)

    def insert_user(self, user):
        return self.user_service.insert_user(user)
