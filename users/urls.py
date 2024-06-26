from django.urls import path
from .views import (
    RegisterView,
    LoginView,
    LogoutView,
    ProfileUpdateView,
    ProfileView,
    subscribe,
    unsubscribe,
)

app_name = 'users'
urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/<str:username>/', ProfileView.as_view(), name='profile'),
    path('profile/update/', ProfileUpdateView.as_view(), name='profile_update'),
    path('subscribe/<int:user_id>/', subscribe, name='subscribe'),
    path('unsubscribe/<int:user_id>/', unsubscribe, name='unsubscribe'),
]
