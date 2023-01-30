from django.db import models

from user.models import Profile
from question.models import Question

class Like(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
