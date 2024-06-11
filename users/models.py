from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

class CustomUser(AbstractUser):
    image = models.ImageField(upload_to='users_image/', blank=True, null=True, default='default_img/user_img.png')

    # Override the groups field to avoid conflicts
    groups = models.ManyToManyField(
        Group,
        related_name='customuser_set',  # Change this to avoid conflicts
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_query_name='customuser'
    )

    # Override the user_permissions field to avoid conflicts
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='customuser_permissions',  # Change this to avoid conflicts
        blank=True,
        help_text='Specific permissions for this user.',
        related_query_name='customuser'
    )

    class Meta:
        db_table = 'customuser'

    def __str__(self):
        return self.username
