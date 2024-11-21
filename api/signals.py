from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from api.tasks import group_users


@receiver(post_save, sender=User)
def trigger_grouping_task(sender, instance, created, **kwargs):
    if created:
        print('signal trigger_grouping_task')
        group_users.delay()
