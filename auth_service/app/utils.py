import jwt
import datetime

SECRET_KEY = 'a4f809f6b3e2fa6e1d9f4c79f40f6b2e8e6f9e4f4c3b6e8b9f5f4e9f8f4f6f3f'


def generate_jwt(user_id):
    token = jwt.encode({
        'user_id': user_id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }, SECRET_KEY, algorithm="HS256")

    return token
