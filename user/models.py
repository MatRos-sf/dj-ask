from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Profile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    friends = models.ManyToManyField("self", blank=True)
    description = models.TextField(max_length=500, blank=True, null=True)

    @property
    def qty_asked(self):
        """
        return how many question you asked
        """
        return self.sender.count()

    @property
    def qty_answered(self):
        """
        return how many question you answered
        """
        return self.answer_set.count()

    @property
    def qty_friends(self):
        """
        return how many friends do you have
        """
        return self.friends.count()

    def __str__(self):
        return self.user.username