from django.urls import path
from .views import home, GroupView, send_message, send_message_to_user, UserMessages, SearchView, notifications, \
    mark_as_read

urlpatterns = [
    path('', home, name='home'),
    path('group/<int:pk>/', GroupView.as_view(), name='group'),
    path('message/', send_message, name='message'),
    path('message/<int:pk>/', send_message_to_user, name='user'),
    path('message/<int:pk>/user/', UserMessages.as_view(), name='user_messages'),
    path('search/', SearchView.as_view(), name='search'),
    path('notifications/', notifications, name='notifications'),
    path('notifications/<int:notification_id>/mark-as-read/', mark_as_read, name='mark_as_read'),

    # path('group/<int:pk>/send/', SendMessageView.as_view(), name='send_message'),
]
