from datetime import datetime
from lib.model import Group


def create_group(request_data, session):
    group_obj = Group(
        name=request_data['name'],
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )

    session.add(group_obj)
    session.flush()
    session.refresh(group_obj)
    return group_obj

