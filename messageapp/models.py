from django.db import models

# Create your models here.
class Group(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

class Contact(models.Model):
    name = models.CharField(max_length=100)




class Message(models.Model):
    text = models.CharField(max_length=100000)
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    audio = models.FileField(upload_to='audios/', null=True, blank=True)
    video = models.FileField(upload_to='videos/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    group = models.ForeignKey(Group, on_delete=models.DO_NOTHING)
    user = models.ForeignKey('users.CustomUser', on_delete=models.DO_NOTHING)

