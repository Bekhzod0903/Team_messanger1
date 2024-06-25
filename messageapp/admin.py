from django.contrib import admin
from .models import Group, Message, UserMessage,Notification


# Register your models here.
admin.site.register(Group)
admin.site.register(Notification)

admin.site.register(Message)
admin.site.register(UserMessage)
