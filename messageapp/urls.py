from django.urls import path
from .views import (
    HomeView,
    GroupView,
    send_message,
    UserMessagesView,
    SearchView,
    notifications,
    EditMessageView,
    DeleteMessageView,
    mark_as_read
)

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('group/<int:pk>/', GroupView.as_view(), name='group'),
    path('message/', send_message, name='message'),
    path('message/<int:pk>/user/', UserMessagesView.as_view(), name='to_user'),
    path('search/', SearchView.as_view(), name='search'),
    path('notifications/', notifications, name='notifications'),
    path('edit/<int:pk>/message', EditMessageView.as_view(), name='edit_message'),
    path('delete/<int:pk>/message', DeleteMessageView.as_view(), name='delete_message'),
    path('notifications/<int:notification_id>/mark-as-read/', mark_as_read, name='mark_as_read'),
]
