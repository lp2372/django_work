
from django.contrib import admin
from django.urls import path

from djtest.apps.article import views

urlpatterns = [
    path('artbd_article/<int:id>/change/', views.article),
    path('artbd_auction_result/<int:id>/change/', views.auction_detail),
    path("",views.index),

    path('test/', views.test),
    path('api/<int:id>', views.api),
    #http://127.0.0.1:8000/admin/article/artbd_article/37718/change/
]
