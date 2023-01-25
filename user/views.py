from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Profile
from .forms import UserRegisterForm

from question.forms import QuickQuestionForms
from question.models import Question

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')

    else:
        form = UserRegisterForm()
    return render(request, "user/register.html", {'form': form})

@login_required
def home(request):

    rando_objects = Profile.objects.exclude(pk=request.user.id).order_by('?')[:5]

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

        print(context)
        return context

    def post(self, request, pk):
        if request.method == 'POST':
            form = QuickQuestionForms(request.POST)
            if form.is_valid():
                cd = form.cleaned_data
                if request.user.profile.id != pk:
                    Question.objects.create(
                        question=cd['question'],
                        sender= request.user.profile,
                        receiver_id =pk,
                        anonymous= cd['anonymous']
                    )
                    messages.success(request, 'Your question has been sent!')
                    return redirect('detail', pk=pk)
                else:
                    messages.error(request, "You can't ask question to yourself!")
                    return redirect('detail', pk=pk)


