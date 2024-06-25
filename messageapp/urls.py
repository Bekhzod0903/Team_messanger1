from django.urls import path
from .views import HomeView, GroupView, send_message, UserMessagesView, SearchView

from .views import (HomeView, GroupView, send_message, UserMessagesView,
                    SearchView, notifications, EditMessageView, DeleteMessageView)

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('group/<int:pk>/', GroupView.as_view(), name='group'),
    path('message/', send_message, name='message'),
    # path('message/<int:pk>/', send_message_to_user, name='user'),
    path('message/<int:pk>/user/', UserMessagesView.as_view(), name='to_user'),
    path('search/', SearchView.as_view(), name='search'),
    path('notifications/', notifications, name='notifications'),
    path('edit/<int:pk>/message', EditMessageView.as_view(), name='edit_message'),
    path('delete/<int:pk>/message', DeleteMessageView.as_view(), name='delete_message'),

    # path('group/<int:pk>/send/', SendMessageView.as_view(), name='send_message'),
]
