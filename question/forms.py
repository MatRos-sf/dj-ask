from django import forms

from .models import Question, Answer

class QuestionForms(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['question', 'anonymous']

class QuickQuestionForms(forms.Form):

    question = forms.CharField(widget=forms.Textarea(attrs={'rows':3, 'class':'form-control'}))
    anonymous = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))

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
