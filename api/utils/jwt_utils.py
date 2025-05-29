import jwt
from datetime import datetime, timedelta
from django.conf import settings

JWT_SECRET = settings.JWT_SECRET
JWT_ALGORITHM = settings.JWT_ALGORITHM


def generate_token():
    payload = {
        "iss": "mi-backend-django",  # transmitter
        "exp": datetime.utcnow() + timedelta(minutes=5),  # expiration time
        "iat": datetime.utcnow(),  # transmitted at
    }

    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token
