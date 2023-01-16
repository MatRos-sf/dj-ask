from django.db.models.signals import post_save, pre_delete
from django.contrib.auth.models import User
from django.dispatch import receiver

from .models import Question, Answer

@receiver(post_save, sender=Answer)
def create_answer(sender, instance, created, **kwargs):
    if created:
        instance.question.answered()
        instance.question.save()

@receiver(pre_delete, sender=Answer)
def delete_answer(sender, instance, **kwargs):

    instance.question.answered_default()
    instance.question.save()

