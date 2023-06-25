from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = "users"

urlpatterns = [
    path("signup/", views.signupuser, name="signup"),
    path("signin/", views.signinuser, name="signin"),
    path("signout/", views.signoutuser, name="signout"),
    #----------------------------------------------------
   path('password_reset/', 
         auth_views.PasswordResetView.as_view(success_url='done'), 
         name='password_reset'),
    path('password_reset/done/', 
         auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', 
         auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete')
]
