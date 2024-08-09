from lib.post import create_post, search_post, like_post, post_comment
from lib.group import create_group
from lib.user import create_user
from lib.group_membership import create_group_membership

create_map = {
    "user": create_user,
    "post": create_post,
    "group": create_group,
    "group_membership": create_group_membership
}

update_map = {
    "like_post": like_post,
    "comment_post": post_comment
}

search_map = {
    "post": search_post
}