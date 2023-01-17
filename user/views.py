from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Profile
from question.forms import QuickQuestionForms
from question.models import Question

@login_required
def home(request):

    rando_objects = Profile.objects.order_by('?')[:5]

    objects = Profile.objects.get(id=request.user.id)
    rando_friends_objects = objects.friends.order_by('?')[:5]

    context = {
        "rando": rando_objects,
        "rando_friends": rando_friends_objects
    }

    return render(request, 'user/home.html', context)

class ProfileDetailView(LoginRequiredMixin, DetailView):

    model = Profile
    template_name = "user/detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        question_with_answer = self.object.questions.filter(is_answer=1).order_by('-created')
        context['questions'] = question_with_answer
        context['form'] = QuickQuestionForms
        return context

    def post(self, request, pk):

        if request.method == 'POST':
            form = QuickQuestionForms(request.POST)
            if form.is_valid():
                cd = form.cleaned_data
                Question.objects.create(
                    question=cd['question'],
                    sender= request.user.profile,
                    receiver_id =pk,
                    anonymous= cd['anonymous']
                )
                return HttpResponse("<h1>Esssa</h1>")



