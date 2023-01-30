from django import template

from question.models import Question
register = template.Library()

@register.simple_tag(takes_context=True)
def is_liked(context, question, user):

    is_like = question.like_set.filter(user=user)
    print(is_like)
    return is_like.exists()