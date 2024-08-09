from lib.model import Post, User, GroupMembership, Like, Comment
from datetime import datetime


def create_post(request_data, session):
    post_obj = Post(
        content=request_data['content'],
        user_id=request_data['user_id'],
        group_id=request_data['group_id'],
        timestamp=datetime.utcnow(),
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )

    session.add(post_obj)
    session.flush()
    session.refresh(post_obj)
    return post_obj


def search_post(session, filter_data, limit, offset):
    q = session.query(
        Post.id,
        Post.content,
        Post.timestamp,
        Post.user_id,
        Post.group_id,
        Post.created_at,
        Post.updated_at,
        Post.soft_delete,
    )
    q = q.join(GroupMembership, Post.group_id == GroupMembership.group_id)
    q = q.filter(GroupMembership.user_id == filter_data['user_id'])
    q = q.filter(Post.soft_delete==False)

    return q.limit(limit).offset(offset).all(), q.count()


from sqlalchemy.exc import IntegrityError
from datetime import datetime


def like_post(request_data, session):
    post_id = request_data['post_id']
    user_id = request_data['user_id']

    like_exists = session.query(Like).filter_by(post_id=post_id, user_id=user_id).first()
    if like_exists:
        raise Exception("You have already liked this post.")

    like_obj = Like(
        post_id=post_id,
        user_id=user_id,
        created_at=datetime.utcnow()
    )

    session.add(like_obj)

    post_obj = session.query(Post).filter_by(id=post_id).first()
    if not post_obj:
        raise Exception("Post not found.")
    post_obj.like_count += 1

    try:
        session.commit()
        return post_obj
    except IntegrityError:
        session.rollback()
        raise Exception("An error occurred while liking the post.")


def post_comment(request_data, session):
    post_id = request_data['post_id']
    user_id = request_data['user_id']
    content = request_data['content']

    post_obj = session.query(Post).filter_by(id=post_id).first()
    if not post_obj:
        raise Exception("Post not found.")

    comment_obj = Comment(
        post_id=post_id,
        user_id=user_id,
        content=content,
        created_at=datetime.utcnow()
    )

    session.add(comment_obj)
    post_obj.comment_count += 1

    try:
        session.commit()
        return comment_obj
    except IntegrityError:
        session.rollback()
        raise Exception("An error occurred while posting the comment.")

