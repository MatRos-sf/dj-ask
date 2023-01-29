from django import template
from user.models import Profile
register = template.Library()

@register.simple_tag()
def qty_notification(pk):

    obj = Profile.objects.get(pk=pk)
    noti = obj.n_recipient.filter(read=False).count()

    return noti
