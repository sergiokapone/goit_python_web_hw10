from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
    path("signup/", views.signupuser, name="signup"),
    path("signin/", views.signinuser, name="signin"),
    path("signout/", views.signoutuser, name="signout"),
]
