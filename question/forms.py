from django import forms

from .models import Question, Answer

class QuestionForms(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['question', 'anonymous']

class QuickQuestionForms(forms.Form):

    question = forms.CharField()
    anonymous = forms.BooleanField(required=False)
    class Meta:
        fields = ['question', 'anonymous']

class AnswerForms(forms.ModelForm):

    class Meta:
        model = Answer
        fields = ('answer',)