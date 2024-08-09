from datetime import datetime
from lib.model import GroupMembership
from lib.utils import logger


def create_group_membership(request_data, session):

    existing_membership = session.query(GroupMembership.id).filter(
        GroupMembership.user_id == request_data['c_user_id'],
        GroupMembership.group_id == request_data['group_id'],
        GroupMembership.soft_delete == False
    ).first()

    if existing_membership:
        logger.info(f"User is already a member of this group. {existing_membership._asdict()}")
        raise Exception("User is already a member of this group.")

    group_membership_obj = GroupMembership(
        user_id=request_data['user_id'],
        group_id=request_data['group_id'],
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )

    session.add(group_membership_obj)
    session.flush()
    session.refresh(group_membership_obj)
    return group_membership_obj
