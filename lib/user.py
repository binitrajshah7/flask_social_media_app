from datetime import datetime
from lib.model import User
from lib.utils import hash_password


def create_user(request_data, session):
    user_obj = User(
        username=request_data['username'],
        password=hash_password(request_data['password']),
        email=request_data['email'],
        is_active=request_data.get('is_active', True),
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )

    session.add(user_obj)
    session.flush()
    session.refresh(user_obj)
    return user_obj
