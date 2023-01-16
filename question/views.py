from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.views.generic import DetailView
from django.contrib.auth.decorators import login_required

from .models import Question
from .forms import QuestionForms, QuickQuestionForms

@login_required
def create_question(request):

    if request.method == 'POST':
        form = QuestionForms(request.POST)
        if form.is_valid():
            object = form.save(commit=False)
            object.sender = request.user.profile
            object.save()
            return redirect(object)

    else:
        form = QuestionForms()

    return render(request, "question/create.html", {"form": form})
@login_required
def del_question(request, pk):
    # delete question only user who create it
    objects = get_object_or_404(Question, pk=pk)
    if objects.sender.pk == request.user.pk:
        name_obj = objects.__str__()
        objects.delete()
        print(f'{name_obj}-- was deleted!')
        #message
        return redirect('home')
    else:
        print("You don't have permission")
        return HttpResponse("<h1>You don't have permission</h1>")


class DetailQuestionView(DetailView):

    model = Question
    template_name = 'question/detail.html'

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['form'] = QuickQuestionForms
    #     return context
    #
    # def post(self, request, *args, **kwargs):
    #     form = QuickQuestionForms(request.POST)
    #     if form.is_valid():
    #         print(self.pk_url_kwarg)
