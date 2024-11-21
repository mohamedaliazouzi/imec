from django.contrib import admin

from api.models import Attribute, Group, UserAttribute

# Register your models here.
admin.site.register(Attribute)
admin.site.register(Group)
admin.site.register(UserAttribute)

