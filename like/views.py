from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse

from .models import Like
from question.models import Question, Notification
@login_required
def like_question(request, question_pk):

    profile = request.user.profile
    question = Question.objects.get(pk=question_pk)
    like, created = Like.objects.get_or_create(user=profile, question=question)
    if not created:
        like.delete()
    elif created:
        recipient = question.sender
        print(recipient)
        Notification.objects.create(
            sender = profile,
            recipient = recipient,
            action = f"{profile} liked {question.question[:15]}"
        )

    return redirect(profile)
