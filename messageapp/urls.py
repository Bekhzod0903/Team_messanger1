from django.urls import path
from .views import HomeView, GroupView, send_message, UserMessagesView, SearchView


urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('group/<int:pk>/', GroupView.as_view(), name='group'),
    path('message/', send_message, name='message'),
    # path('message/<int:pk>/', send_message_to_user, name='user'),
    path('message/<int:pk>/user/', UserMessagesView.as_view(), name='to_user'),
    path('search/', SearchView.as_view(), name='search'),
    # path('group/<int:pk>/send/', SendMessageView.as_view(), name='send_message'),
]
