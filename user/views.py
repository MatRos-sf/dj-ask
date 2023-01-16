from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Profile

@login_required
def home(request):

    rando_objects = Profile.objects.order_by('?')[:5]

    objects = Profile.objects.get(id=request.user.id)
    rando_friends_objects = objects.friends.order_by('?')[:5]

    context = {
        "rando": rando_objects,
        "rando_friends": rando_friends_objects
    }

    return render(request, 'user/home.html', context)

class ProfileDetailView(LoginRequiredMixin, DetailView):

    model = Profile
    template_name = "user/detail.html"


