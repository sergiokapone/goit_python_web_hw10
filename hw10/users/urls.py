from django.urls import path
from . import views

app_name = 'quotes'

urlpatterns = [
    path('users/', views.main, name ='root'),
]
