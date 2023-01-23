from django.urls import path, include
from django.contrib.auth import views as auth_views

from .views import (
    create_question, DetailQuestionView, del_question,
    create_answer, del_answer, random_question
)

app_name='question'

urlpatterns = [
    path('create/',create_question , name='create'),
    path('<int:pk>/', DetailQuestionView.as_view(), name='detail'),

    path("<int:pk>/answer/", create_answer, name='answer-create'),
    path("answer/<int:pk>/delete/", del_answer , name='answer-delete'),
    path('<int:pk>/delete/', del_question, name='delete'),

    path('random/<str:name>/', random_question, name='random')
]
