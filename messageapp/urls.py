from django.urls import path
from .views import home, GroupView,get_home_page
urlpatterns = [
    path('', home, name='home'),
    path('group/<int:pk>/', GroupView.as_view(), name='group'),
    path('', get_home_page, name='get_home_page'),
    # path('group/<int:pk>/send/', SendMessageView.as_view(), name='send_message'),
]
