from django.db import models

from django.contrib.auth.models import AbstractUser
# Create your models here.


class CustomUser(AbstractUser):
    image = models.ImageField(upload_to='users_image/', blank=True, null=True, default='default_img/user_img.png')


    class Meta:
        db_table = 'custom_user'

    def __str__(self):
        return f"Username: {self.username}"

from django.conf import settings
from django.db import models

class Subscription(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='subscriptions', on_delete=models.CASCADE)
    subscriber = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='subscribers', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.subscriber.username} is subscribed to {self.user.username}"
