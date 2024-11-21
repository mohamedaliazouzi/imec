from celery import shared_task
from .models import User, UserAttribute, Group


@shared_task
def group_users():
    users = User.objects.all()
    user_attributes_map = {
        user.id: list(UserAttribute.objects.filter(user=user).values_list('attribute_id', flat=True))
        for user in users
    }
    user_group_map = {}
    for user_id, attributes in user_attributes_map.items():
        for other_user_id, other_attributes in user_attributes_map.items():
            if user_id == other_user_id:
                continue

            common_attributes = set(attributes).intersection(set(other_attributes))

            if len(common_attributes) >= 3:
                group_id = user_group_map.get(user_id) or user_group_map.get(other_user_id)
                if not group_id:
                    group = Group.objects.create()
                    group_id = group.id

                user_group_map[user_id] = group_id
                user_group_map[other_user_id] = group_id

    for user_id, group_id in user_group_map.items():
        group = Group.objects.get(id=group_id)
        user = User.objects.get(id=user_id)
        group.attributes.add(*user_attributes_map[user_id])  # Associate attributes to the group

    return "Users have been grouped successfully!"
