from django.shortcuts import redirect, render
from django.views import View
from .models import Group, Message
from django.http import JsonResponse
from .forms import GroupForm, MessageForm
from django.shortcuts import render, get_object_or_404
from .forms import SearchForm

# Create your views here.


def home(request):
    groups = Group.objects.all()
    return render(request, 'home.html', {'groups': groups})


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
  




def home(request):
    search_form = SearchForm(request.GET or None)
    groups = Group.objects.all()

    if search_form.is_valid():
        query = search_form.cleaned_data['query']
        groups = groups.filter(name__icontains=query)

    return render(request, 'base.html', {'groups': groups, 'search_form': search_form})



# class SendMessageView(View):
#     def get(self, request, pk):
#         group = Group.objects.get(id=pk)
#         message_form = MessageForm()
#         return render(request,'group.html', {'message_form': message_form, 'group': group})
    
    