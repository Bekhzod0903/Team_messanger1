from django.urls import path
<<<<<<< HEAD
from .views import HomeView, GroupView, send_message, UserMessagesView, SearchView

from .views import (HomeView, GroupView, send_message, UserMessagesView,
                    SearchView, notifications, EditMessageView, DeleteMessageView)
=======
from .views import home, GroupView, send_message, send_message_to_user, UserMessages, SearchView, notifications, \
    mark_as_read
>>>>>>> 4d2d9dda974b54333cf935bcdfc117861846d930

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('group/<int:pk>/', GroupView.as_view(), name='group'),
    path('message/', send_message, name='message'),
    # path('message/<int:pk>/', send_message_to_user, name='user'),
    path('message/<int:pk>/user/', UserMessagesView.as_view(), name='to_user'),
    path('search/', SearchView.as_view(), name='search'),
    path('notifications/', notifications, name='notifications'),
<<<<<<< HEAD
    path('edit/<int:pk>/message', EditMessageView.as_view(), name='edit_message'),
    path('delete/<int:pk>/message', DeleteMessageView.as_view(), name='delete_message'),
=======
    path('notifications/<int:notification_id>/mark-as-read/', mark_as_read, name='mark_as_read'),
>>>>>>> 4d2d9dda974b54333cf935bcdfc117861846d930

    # path('group/<int:pk>/send/', SendMessageView.as_view(), name='send_message'),
]
