from django import forms
from config.models import MessageBlog

class MessageForm(forms.ModelForm):
    class Meta:
        model = MessageBlog
        fields = ('name',)
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'name',
                'placeholder': 'Name'
            })
        }