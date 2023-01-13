from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Profile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    friends = models.ForeignKey("self", on_delete=models.CASCADE, blank=True, null=True)
    description = models.TextField(max_length=500, blank=True, null=True)
    def qty_asked(self):
        """
        return how many question you asked
        """
        return self.sender.count()

    def qty_answered(self):
        """
        return how many question you answered
        """
        return self.answer_set.count()