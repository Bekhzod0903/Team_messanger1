from django.db import models
from django.conf import settings
from django.contrib.auth.models import User


# Create your models here.
class Group(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'groups'

class Contact(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'contacts'




class Message(models.Model):
    # sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='message_sender')
    # receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='message_receiver')
    text = models.TextField(blank=True, null=True)
    attachment = models.FileField(upload_to='attachments/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    group = models.ForeignKey(Group, on_delete=models.DO_NOTHING)
    user = models.ForeignKey('users.CustomUser', on_delete=models.DO_NOTHING)


    def __str__(self):
        return self.text
    
    class Meta:
        db_table = 'messages'

class UserMessage(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='message_sender')
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='message_receiver')
    text = models.TextField(blank=True, null=True)
    attachment = models.FileField(upload_to='attachments/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.text} | {self.sender} -> {self.receiver}"

    def user_auth(self, user):
        return self.sender == user

    def edit_message(self, text):
        self.text = text
        text.save()




# from django.db import models
# from django.conf import settings
#
# class Notification(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     message = models.CharField(max_length=250)
#     timestamp = models.DateTimeField(auto_now_add=True)
#     read = models.BooleanField(default=False)
#
#     def __str__(self):
#         return f'Notification for {self.user.username} at {self.timestamp}'

from django.db import models
from django.conf import settings

class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-timestamp']
