from django import forms
from .models import Conference, Question

class ConferenceForm(forms.ModelForm):
    class Meta:
        model = Conference
        fields = ['title', 'description']

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['name', 'text']
