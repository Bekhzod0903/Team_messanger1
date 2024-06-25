from django.contrib import admin
from .models import CustomUser
# Register your models here.

from .models import Subscription

admin.site.register(Subscription)
admin.site.register(CustomUser)