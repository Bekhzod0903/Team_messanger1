from django.forms import ModelForm
from django import forms
from .models import Group, Message

class GroupForm(ModelForm):
    class Meta:
        model = Group
        fields = '__all__'
    
class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = ['text', 'image', 'audio', 'video']

class SearchForm(forms.Form):
    query = forms.CharField(label='Search', max_length=100)