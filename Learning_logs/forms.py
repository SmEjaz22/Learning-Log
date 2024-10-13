from django import forms
from .models import topic_ofinterest,Entry

class TopicForm(forms.ModelForm):
    class Meta:
        model = topic_ofinterest
        fields = ['text']
        labels = {'text': ''}
        
class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['text']
        labels = {'text': ''}
        widgets = {'text': forms.Textarea(attrs={'cols': 80})}