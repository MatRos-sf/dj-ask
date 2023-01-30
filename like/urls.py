from django.urls import path, include
from django.contrib.auth import views as auth_views

from .views import like_question

app_name='like'

urlpatterns = [
    path('<int:question_pk>/like', like_question, name='like')

]
