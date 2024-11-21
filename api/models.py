import uuid
from django.contrib.auth.models import User
from django.db import models


class Attribute(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField()

    def __str__(self):
        return self.name


class Group(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  # Using UUID for primary key
    attributes = models.ManyToManyField(Attribute, related_name='groups')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Group {self.id}"


class UserAttribute(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_attributes')
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE, related_name='user_attributes')
    value = models.CharField(max_length=255,default="")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.attribute.name}"
