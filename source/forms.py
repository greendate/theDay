from django import forms
from django.forms import ModelForm, Textarea, TextInput, IntegerField, DateField, TimeField, ChoiceField, RadioSelect, NumberInput, DateInput, TimeInput, URLInput
from .models import UserInfo, Event, Image, Status, Comment
import datetime

class UserEditForm(forms.ModelForm):

    class Meta:
        model = UserInfo
        fields = ('telegram_alias', 'messenger_alias', 'interests_description', 'picture_url')

        widgets = {
            'telegram_alias': TextInput(attrs={'id': 'telegram_alias', 'placeholder': 'telegram'}),
            'messenger_alias': TextInput(attrs={'id': 'messenger_alias', 'placeholder': 'messenger'}),
            'interests_description':  Textarea(attrs={'id': 'interests', 'placeholder': 'List some of your favourite topics..'}),
        }


class Create(forms.ModelForm):

    class Meta:
        model = Event
        fields = ('names', 'date', 'when', 'where', 'our_story', 'picture_url')
        # date = forms.DateField(widget=forms.SelectDateWidget())
        widgets = {
            'names': TextInput(attrs={'id': 'name', 'placeholder': 'e.g Janny & Tom'}),
            'date': DateInput(attrs={'type': 'date'}),
            'when':  TimeInput(attrs={'type': 'time'}),
            'where': TextInput(attrs={'id': 'where', 'placeholder': 'e.g Kazan City Hall'}),
            'our_story': Textarea(attrs={'id': 'story', 'placeholder': 'Our story..'}),
        }

class ImageForm(forms.ModelForm):

    class Meta:
        model = Image
        fields = ['picture', 'description']
        widgets = {
            'our_story': Textarea(attrs={'id': 'description', 'placeholder': 'Caption..'}),
        }


class StatusForm(forms.ModelForm):
    class Meta:
        model = Status
        fields = ['status_text']
        widgets = {
            'status_text': Textarea(attrs={'id': 'status_text', 'placeholder': 'Status: ..'}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']
        widgets = {
            'comment': Textarea(attrs={'id': 'comment', 'placeholder': 'Comment..'}),
        }
