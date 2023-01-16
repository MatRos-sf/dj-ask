from django.urls import path, include
from django.contrib.auth import views as auth_views

from .views import home, ProfileDetailView


urlpatterns = [
    path('', home, name='home'),

    path('login/', auth_views.LoginView.as_view(template_name='user/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('profile/<int:pk>/', ProfileDetailView.as_view(), name='detail')

]
