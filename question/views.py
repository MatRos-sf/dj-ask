from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.views.generic import DetailView, CreateView
from django.contrib.auth.decorators import login_required

from .models import Question, Answer
from .forms import QuestionForms, QuickQuestionForms, AnswerForms

from user.models import Profile

@login_required
def create_question(request,pk):

    if request.method == 'POST':
        form = QuestionForms(request.POST)
        if form.is_valid():
            object = form.save(commit=False)
            object.sender = request.user.profile
            object.receiver = Profile.objects.get(id=pk)
            object.save()
            return redirect(object)

    else:
        form = QuestionForms()

    return render(request, "question/create.html", {"form": form})

class DetailQuestionView(LoginRequiredMixin, DetailView):

    model = Question
    template_name = 'question/detail.html'


@login_required
def del_question(request, pk):
    # delete question only user who create it
    objects = get_object_or_404(Question, pk=pk)
    if objects.sender.pk == request.user.pk and objects.can_edit():
        name_obj = objects.__str__()
        objects.delete()
        messages.success(request, f'{name_obj}-- was deleted!')
        return redirect('home')
    else:
        messages.error(request, "You don't have permission")
        return redirect('home')

@login_required
def edit_question(request, pk):
    obj = get_object_or_404(Question, pk=pk)
    receiver = obj.receiver
    if obj.can_edit() and request.user.pk == obj.sender.pk:
        form = QuestionForms(instance=obj)
        if request.method == 'POST':
            form = QuestionForms(request.POST)
            if form.is_valid():
                object = form.save(commit=False)
                object.sender = request.user.profile


                object.receiver = receiver
                object.save()
                return redirect(object)
        return render(request, "question/create.html", {"form": form})
    return render(request, "question/info.html", {'info': 'Only the sender of the question can edit it.'})

# ANSWER
@login_required
def create_answer(request, pk):
    object = get_object_or_404(Question, pk=pk)
    form = AnswerForms()
    if request.method == 'POST':
        form = AnswerForms(request.POST)
        if form.is_valid():
            obj_form = form.save(commit=False)
            obj_form.question = object
            obj_form.user = request.user.profile

            obj_form.save()
            return redirect('home')



    return render(request, "question/create.html", {
        'form': form,
        'object': object
    })

@login_required
def del_answer(request, pk):
    # delete question only user who create it
    objects = get_object_or_404(Answer, pk=pk)
    if objects.user.pk == request.user.pk:
        name_obj = objects.__str__()
        objects.delete()
        print(f'{name_obj}-- was deleted!')
        # message
        return redirect('home')
    else:
        print("You don't have permission")
        return HttpResponse("<h1>You don't have permission</h1>")



# random function
def random_question(request, name):

    if name.lower() == 'rando':
        from user.models import Profile
        import json
        from random import choice

        object = Profile.objects.exclude(pk=request.user.profile.pk).order_by('?')[0]
        with open("random_question.data", "r") as f:
            qs = json.load(f)
            q = choice(qs)

        Question.objects.create(
            question = q,
            sender = request.user.profile,
            receiver = object
        )
        print('rando ask')
        return redirect('home')

    elif name.lower() == 'friends':
        user_rando_friends = request.user.profile.friends.all().order_by('?')[0]
        Question.objects.create(
            question = "What's up?",
            sender = request.user.profile,
            receiver = user_rando_friends
        )
        print('randoo friends')
        return redirect('home')

