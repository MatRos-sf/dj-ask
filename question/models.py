from django.db import models
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.utils.translation import gettext_lazy as _

from user.models import Profile
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
class Answer(models.Model):

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.TextField(max_length=500)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, null=True)

    def clean(self):
        if self.user.id == self.question.receiver.id:
            id_q = self.question.id
            get_obj = Question.objects.get(id=id_q)
            if get_obj.answer_set.count() > 0:
                raise ValidationError(_("My error: You answered for this question"))
        else:
            raise ValidationError(_("My error: You don't have permission "))
        super(Answer, self).clean()

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        self.clean()
        super(Answer,self).save(force_insert, force_update, using, update_fields)
    #     # add some information about error
    #     if self.user.id == self.question.receiver.id:
    #         id_q = self.question.id
    #         get_obj = Question.objects.get(id=id_q)
    #         if get_obj.answer_set.count() == 0:
    #             super(Answer,self).save(force_insert, force_update, using, update_fields)
    #         else:
    #             raise ValidationError('My error: You answered for this question!')
    #     else:
    #         raise ValidationError("My error: Wrong receiver")
        # raise ValidationError("You don't want permission ")
        # # it's must show any error
