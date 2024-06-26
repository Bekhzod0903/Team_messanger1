from django.shortcuts import render, redirect
from .forms import CustomUserForm, ProfileUpdateForm
from django.views import View
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib import messages
# from products.models import Logo
# from products.models import Products
from .models import CustomUser
from django.shortcuts import get_object_or_404
# Create your views here.


class RegisterView(View):
    def get(self, request):
        create_form = CustomUserForm()
        context = {
            'form': create_form
        }
        return render(request, 'register.html', context=context)

    def post(self, request):
        create_form = CustomUserForm(data=request.POST, files=request.FILES)
        if create_form.is_valid():
            create_form.save()
            return redirect('users:login')
        else:
            context = {
                'form': create_form
            }
            return render(request, 'register.html', context=context)


class LoginView(View):
    def get(self, request):
        create_form = AuthenticationForm()
        context = {
            'form': create_form
        }
        return render(request, 'login.html', context=context)

    def post(self, request):
        login_form = AuthenticationForm(data=request.POST)
        if login_form.is_valid():
            user = login_form.get_user()
            login(request, user)
            return redirect('home')
        else:

            context = {
                'form': login_form
            }
            return render(request, 'login.html', context=context)


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('home')


from django.shortcuts import get_object_or_404, render
from django.views import View
from django.contrib.auth import get_user_model
from .models import Subscription

User = get_user_model()

class ProfileView(View):
    def get(self, request, username):
        user = get_object_or_404(User, username=username)
        is_own_profile = (user == request.user)
        subscriptions = Subscription.objects.filter(subscriber=user)
        subscribers = Subscription.objects.filter(user=user)

        # Check if the profile owner is subscribed to the visiting user
        is_subscribed = Subscription.objects.filter(user=user, subscriber=request.user).exists()

        context = {
            'user': user,
            'is_own_profile': is_own_profile,
            'subscriptions': subscriptions,
            'subscribers': subscribers,
            'is_subscribed': is_subscribed,
        }
        return render(request, 'profile.html', context=context)



# class ProfileUpdateView(View):
#     def get(self, request):
#         update_form = ProfileUpdateForm(instance=request.user)
#         context = {
#             'form': update_form
#         }
#         return render(request, 'profile_update.html', context=context)

    def post(self, request, username):
        user = get_object_or_404(CustomUser, username=username)
        is_own_profile = (user == request.user)
        update_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if update_form.is_valid():
            update_form.save()
            return redirect('users:profile')
        else:
            context = {
                'form': update_form,
                'user': user,
                'is_own_profile': is_own_profile
            }
            messages.error(request,'Something went wrong')
            return render(request, 'profile_update.html', context=context)



from django.shortcuts import render, redirect
from django.views import View
from .forms import ProfileUpdateForm

class ProfileUpdateView(View):
    def get(self, request):
        update_form = ProfileUpdateForm(instance=request.user)
        context = {
            'form': update_form
        }
        return render(request, 'profile_update.html', context=context)

    def post(self, request):
        update_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if update_form.is_valid():
            update_form.save()
            # Redirect to profile page or another appropriate view upon successful update
            return redirect('users:profile', username=request.user.username)
        else:
            context = {
                'form': update_form
            }
            return render(request, 'profile_update.html', context=context)

from django.conf import settings
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, redirect
from .models import Subscription

User = get_user_model()

def subscribe(request, user_id):
    user = get_object_or_404(User, id=user_id)
    subscriber = request.user
    Subscription.objects.create(user=user, subscriber=subscriber)
    return redirect('users:profile', username=user.username)

def unsubscribe(request, user_id):
    user = get_object_or_404(User, id=user_id)
    subscriber = request.user
    Subscription.objects.filter(user=user, subscriber=subscriber).delete()
    return redirect('users:profile', username=user.username)
