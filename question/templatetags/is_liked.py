from django import template

from question.models import Question
register = template.Library()

@register.simple_tag
def is_liked(question_id, user_id):
    print('*'*100)
    question = Question.objects.get(id=question_id)
    likes = question.like_set.filter(user_id=user_id)
    return likes.exists()