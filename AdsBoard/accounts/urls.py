from django.urls import path
from .views import SignUp
from django.contrib.auth import logout

urlpatterns = [
    path('signup/', SignUp.as_view(), name='signup'),
]