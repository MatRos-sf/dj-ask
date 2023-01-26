from django.urls import path, include
from django.contrib.auth import views as auth_views

from .views import (
    create_question, DetailQuestionView, del_question,
    create_answer, del_answer, random_question, edit_question, sample,
    random_question_with_pk
)

app_name='question'

urlpatterns = [
    path('create/to<int:pk>/',create_question , name='create'),
    path('edit/<int:pk>/', edit_question, name='edit'),
    path('<int:pk>/', DetailQuestionView.as_view(), name='detail'),
    path('<int:pk>/delete/', del_question, name='delete'),

    #answer
    path("<int:pk>/create-answer/", create_answer, name='answer-create'),
    path("answer/<int:pk>/delete/", del_answer , name='answer-delete'),
    path('<int:pk>/delete/', del_question, name='delete'),

    #answer random
    path('random/<str:name>/', random_question, name='random'),
    path('random-pk/<int:pk>/', random_question_with_pk, name='random-pk'),
    path('sample/', sample, name='sample')
]
