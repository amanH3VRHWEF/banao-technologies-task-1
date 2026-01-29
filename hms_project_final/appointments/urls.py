from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'), # This is the home page
    path('signup/', views.signup_view, name='signup'),
]