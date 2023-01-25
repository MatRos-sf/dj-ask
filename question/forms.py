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

class FriendQuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['question', 'receiver', 'anonymous']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(FriendQuestionForm, self).__init__(*args, **kwargs)
        if self.user:
            self.fields['receiver'].queryset = self.user.profile.friends.all()
