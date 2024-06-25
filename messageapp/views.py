from django.conf import settings
from django.shortcuts import redirect, render
from django.views import View
from .models import Group, Message, UserMessage
from django.http import JsonResponse
from .forms import GroupForm, MessageForm, UserMessageForm
from django.shortcuts import render, get_object_or_404
from .forms import SearchForm
from users.models import CustomUser
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Notification
# Create your views here.


def home(request):
    groups = Group.objects.all()
    users = CustomUser.objects.all()
    return render(request, 'home.html', {'groups': groups, 'users': users})


class GroupView(View):
    def get(self, request, pk):
        group = Group.objects.get(id=pk)
        messages = Message.objects.filter(group=group)
        message_form = MessageForm()
        # return render(request,'group.html', {'message_form': message_form, 'group': group})
        return render(request, 'group.html', {'group': group,'messages': messages, 'message_form': message_form,})
    
    def post(self, request, pk):
        group = Group.objects.get(id=pk)
        message_form =MessageForm(request.POST, request.FILES)
        if message_form.is_valid():
            message = message_form.save(commit=False)
            message.user = request.user
            message.group = group
            message.save()
            return redirect('group', pk=group.id)
        else:
            context = {'message_form': message_form, 'group': group}

            return render(request,'group.html', context=context)
  




# def home_o(request):
#     search_form = SearchForm(request.GET or None)
#
#     if search_form.is_valid():
#         query = search_form.cleaned_data['query']
#         groups = groups.filter(name__icontains=query)
#
#     return render(request, 'base.html', {'search_form': search_form})



@login_required
def send_message(request):
    if request.method == 'POST':
        form = MessageForm(request.POST, request.FILES)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            if 'attachment' in request.FILES:
                message.attachment = request.FILES['attachment']
            message.save()
            return redirect('group')
    else:
        form = MessageForm()
    return render(request, 'send_message.html', {'form': form})


@login_required
def send_message_to_user(request, pk):
    user = get_object_or_404(CustomUser, id=pk)
    if request.method == 'POST':
        form = UserMessageForm(request.POST, request.FILES)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.receiver = user
            if 'attachment' in request.FILES:
                message.attachment = request.FILES['attachment']
            message.save()
            return redirect('user_messages', pk=user.id)
    else:
        form = MessageForm()
    return render(request, 'send_message_to_user.html', {'form': form, 'user': user})


class UserMessages(View):
    def get(self, request, pk):
        user = get_object_or_404(CustomUser, id=pk)
        messages = UserMessage.objects.filter(
            (Q(sender=request.user) & Q(receiver=user)) | (Q(sender=user) & Q(receiver=request.user))
        ).order_by('created_at')
        form = MessageForm()
        return render(request, 'user_messages.html', {'messages': messages, 'user': user, 'form': form})

    def post(self, request, pk):
        user = get_object_or_404(CustomUser, id=pk)
        form = MessageForm(request.POST, request.FILES)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.receiver = user
            message.save()
            return redirect('user_messages', pk=pk)
        messages = UserMessage.objects.filter(
            (Q(sender=request.user) & Q(receiver=user)) | (Q(sender=user) & Q(receiver=request.user))
        ).order_by('created_at')
        return render(request, 'user_messages.html', {'messages': messages, 'user': user, 'form': form})


class SearchView(View):
    def get(self, request):
        query = request.GET.get('q', '')
        if query:
            users = CustomUser.objects.filter(
                Q(username__icontains=query) |
                Q(first_name__icontains=query) |
                Q(last_name__icontains=query)
            )
        else:
            users = CustomUser.objects.none()

        context = {
            'users': users,
            'query': query
        }
        return render(request, 'search.html', context=context)

@login_required
def notifications(request):
    user = request.user
    notifications = Notification.objects.filter(user=user, read=False)
    print(f"User: {user}, Notifications: {notifications}")  # Debug print statement
    return render(request, 'notifications.html', {'notifications': notifications})


