from django.shortcuts import redirect, render
from django.views import View
from .models import Group, Message, UserMessage
from django.http import JsonResponse
from .forms import GroupForm, MessageForm, UserMessageForm, EditMessageForm
from django.shortcuts import render, get_object_or_404
from .forms import SearchForm
from users.models import CustomUser
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth import get_user_model
from .models import Notification
from django.contrib import messages
from django.http import HttpResponseForbidden
# from .models import Notification
# Create your views here.


class HomeView(View):
    def get(self, request):
        groups = Group.objects.all()
        owner = request.user
        users = get_user_model().objects.exclude(id=owner.id)
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

            return render(request, 'group.html', context=context)
  




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


# @login_required
# def send_message_to_user(request, pk):
#     user = get_object_or_404(CustomUser, id=pk)
#     if request.method == 'POST':
#         form = UserMessageForm(request.POST, request.FILES)
#         if form.is_valid():
#             message = form.save(commit=False)
#             message.sender = request.user
#             message.receiver = user
#             if 'attachment' in request.FILES:
#                 message.attachment = request.FILES['attachment']
#             message.save()
#             return redirect('user_messages', pk=user.id)
#     else:
#         form = MessageForm()
#     return render(request, 'send_message_to_user.html', {'form': form, 'user': user})


class UserMessagesView(View):
    def get(self, request, pk):
        user = get_object_or_404(CustomUser, id=pk)
        send_message = UserMessage.objects.filter(
            (Q(sender=request.user) & Q(receiver=user)) | (Q(sender=user) & Q(receiver=request.user))
        ).order_by('-created_at')
        form = UserMessageForm()

        other_users = CustomUser.objects.exclude(id=request.user.id)
        user_last_messages = []
        for other_user in other_users:
            last_message = UserMessage.objects.filter(
                (Q(sender=request.user) & Q(receiver=other_user)) | (Q(sender=other_user) & Q(receiver=request.user))
            ).order_by('-created_at').first()
            user_last_messages.append((other_user, last_message))

        context = {
            'user': user,
            'form': form,
            'send_message': send_message,
            'user_last_messages': user_last_messages,
        }
        return render(request, 'user_messages.html', context=context)

    def post(self, request, pk):
        user = get_object_or_404(CustomUser, id=pk)
        form = UserMessageForm(request.POST, request.FILES)
        if form.is_valid():
            send_message = form.save(commit=False)
            send_message.sender = request.user
            send_message.receiver = user
            send_message.save()
            return redirect('to_user', pk=pk)

        send_message = UserMessage.objects.filter(
            (Q(sender=request.user) & Q(receiver=user)) | (Q(sender=user) & Q(receiver=request.user))
        ).order_by('-created_at')

        other_users = CustomUser.objects.exclude(id=request.user.id)
        user_last_messages = []
        for other_user in other_users:
            last_message = UserMessage.objects.filter(
                (Q(sender=request.user) & Q(receiver=other_user)) | (Q(sender=other_user) & Q(receiver=request.user))
            ).order_by('-created_at').first()
            user_last_messages.append((other_user, last_message))

        context = {
            'user': user,
            'form': form,
            'send_message': send_message,
            'user_last_messages': user_last_messages,
        }
        return render(request, 'Chat/user_messages.html', context=context)

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

from django.shortcuts import render
from .models import Notification

def notifications(request):
    notifications = Notification.objects.filter(user=request.user).order_by('-timestamp')
    return render(request, 'notifications.html', {'notifications': notifications})


class EditMessageView(View):
    def get(self, request, pk):
        message = get_object_or_404(UserMessage, pk=pk)
        if not message.user_auth(request.user):
            messages.error(request, "You can't edit this message!")
            return redirect('to_user', pk=message.receiver.pk)

        edit_message_form = EditMessageForm(instance=message)
        context = {
            'edit_message_form': edit_message_form,
            'message': message,
        }
        return render(request, 'edit_message.html', context=context)

    def post(self, request, pk):
        message = get_object_or_404(UserMessage, pk=pk)
        if not message.user_auth(request.user):
            messages.error(request, "You can't edit this message!")
            return redirect('to_user', pk=message.receiver.pk)

        edit_message_form = EditMessageForm(request.POST, instance=message)
        if edit_message_form.is_valid():
            edit_message_form.save()
            messages.success(request, "Message edited successfully.")
            return redirect('to_user', pk=message.receiver.pk)

        context = {
            'edit_message_form': edit_message_form,
            'message': message,
        }
        return render(request, 'edit_message.html', context=context)


class DeleteMessageView(View):
    def post(self, request, pk):
        message = get_object_or_404(UserMessage, pk=pk)
        if message.sender == request.user:
            message.delete()
            return redirect('to_user', pk=message.receiver.pk)
        else:
            return HttpResponseForbidden('Siz bu xabarni o\'chira olmaysiz!')
def mark_as_read(request, notification_id):
    notification = Notification.objects.get(id=notification_id)
    notification.is_read = True
    notification.save()
    return redirect('notifications')
