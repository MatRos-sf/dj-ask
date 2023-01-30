from django import template

from question.models import Question
register = template.Library()

@register.simple_tag
def is_liked(question, user):

    is_like = question.like_set.filter(user=user)
    return is_like.exists()