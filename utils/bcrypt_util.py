import bcrypt


class BcryptUtil:
    @staticmethod
    def hash_password(password):
        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

    @staticmethod
    def check_password(password, hashed_password):
        return bcrypt.checkpw(password.encode("utf-8"), hashed_password)
