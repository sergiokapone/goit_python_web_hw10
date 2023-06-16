from django.urls import path
from . import views

app_name = 'quotes'

urlpatterns = [
    path('', views.main, name ='root'),
    path('<int:page>', 
         views.main, 
         name ='root_paginate'),
    path('tag/<str:tag_name>/page/<int:page>/', 
         views.quotes_by_tag, 
         name='quotes_by_tag'),
    path('author/<author_fullname>/', 
         views.author_page, 
         name='author_page')
]
