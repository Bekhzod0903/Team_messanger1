from django.contrib import admin
from .models import Group, Message, UserMessage


# Register your models here.
admin.site.register(Group)

admin.site.register(Message)
admin.site.register(UserMessage)
