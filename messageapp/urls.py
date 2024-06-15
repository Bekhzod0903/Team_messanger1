from django.urls import path
from .views import home, GroupView
urlpatterns = [
    path('', home, name='home'),
    path('group/<int:pk>/', GroupView.as_view(), name='group'),
    # path('group/<int:pk>/send/', SendMessageView.as_view(), name='send_message'),
]
