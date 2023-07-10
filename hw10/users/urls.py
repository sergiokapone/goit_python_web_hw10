from django.urls import path
from django.contrib.auth import views as auth_views


from . import views

app_name = "users"

urlpatterns = [
    path("signup/", views.signupuser, name="signup"),
    path("signin/", views.signinuser, name="signin"),
    path("signout/", views.signoutuser, name="signout"),
    #----------------------------------------------------
#    path('password_reset/', 
#          auth_views.PasswordResetView.as_view(success_url='done'), 
#          name='password_reset'),
#     path('password_reset/done/', 
#          auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
#     path('reset/<uidb64>/<token>/', 
#          auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
#     path('reset/done/', 
#          auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    #----------------------------------------------------
    path('reset-password/', 
          views.ResetPasswordView.as_view(), 
          name='password_reset'),
    path('reset-password/done/', 
          auth_views.PasswordResetDoneView.as_view(
             template_name='users/password_reset_done.html'),
          name='password_reset_done'),
    path('reset-password/confirm/<uidb64>/<token>/',
          auth_views.PasswordResetConfirmView.as_view(
             template_name='users/password_reset_confirm.html',
             success_url='/users/reset-password/complete/'),
          name='password_reset_confirm'),
    path('reset-password/complete/',
          auth_views.PasswordResetCompleteView.as_view(
             template_name='users/password_reset_complete.html'),
          name='password_reset_complete'),
]
