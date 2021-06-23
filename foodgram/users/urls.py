from django.urls import path

from . import views


urlpatterns = [
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('logged-out/', views.logged_out, name='logged_out')
]
