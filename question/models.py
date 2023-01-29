from django.db import models
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.utils.translation import gettext_lazy as _

from user.models import Profile

class Notification(models.Model):
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='n_sender')
    recipient = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='n_recipient')
    action = models.CharField(max_length=300)

    created = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created']


class Question(models.Model):
    STATUS_CHOICES = (
        (1, _('Yes')),
        (2, _('No'))
    )
    question = models.TextField(max_length=500)
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="sender")
    receiver = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="questions")

    anonymous = models.BooleanField(default=False, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    is_answer = models.SmallIntegerField(choices=STATUS_CHOICES, default=2)
    def who_ask(self):
        if self.anonymous:  return "anonymous"
        else:               return self.sender.user.username

    def answered(self):
        self.is_answer = 1
    def answered_default(self):
        self.is_answer=2

    def __str__(self):

        return f"Q{self.id}: {self.who_ask()} to {self.receiver.user.username}"

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('question:detail', kwargs={'pk' : self.pk})

    def get_answer(self):
        if self.is_answer == 2:
            return None
        return self.answer_set.first().answer

    def can_edit(self):
        return not self.answer_set.exists()




class Answer(models.Model):

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.TextField(max_length=500)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, null=True)

    def notification_info(self, user):
        info = f"'{user} answered for your question: {self.question.question[:50]}...'"
        return info

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        if self.question.answer_set.exists():
            raise ValidationError("This question already has an answer.")
        if self.user.id == self.question.sender.id:
            raise ValidationError("The sender of the question can't answer to his own question.")
        if self.user.user.id != self.question.receiver.id:
            raise ValidationError("Only the receiver of the question can answer it.")

        super(Answer,self).save(force_insert, force_update, using, update_fields)
        # notification
        sender = self.question.sender
        notification = Notification(
            recipient = sender,
            sender = self.user,
            action = self.notification_info(self.user)
        )
        notification.save()


