from django import forms

from .models import Question, Answer

class QuestionForms(forms.ModelForm):


    class Meta:
        model = Question
        fields = ['question', 'receiver', 'anonymous']

class QuickQuestionForms(forms.Form):

    question = forms.TextInput()
    anonymous = forms.BooleanField()
    class Meta:
        fields = ['question', 'anonymous']