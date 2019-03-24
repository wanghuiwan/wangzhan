from django import forms
from .models import Topic, Entry


class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['text']
        labels = {'text': ''}


class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['text']
        labels = {'text': ''}
        # 将输入框变宽来适应大量文本录入
        widgets = {'text': forms.Textarea(attrs={'cols': 80})}









