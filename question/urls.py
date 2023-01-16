from django.urls import path, include
from django.contrib.auth import views as auth_views

from .views import create_question, DetailQuestionView, del_question

app_name='question'

urlpatterns = [
    path('create/',create_question , name='create'),
    path('<int:pk>/', DetailQuestionView.as_view(), name='detail'),

    path('<int:pk>/delete/', del_question, name='delete')
]
