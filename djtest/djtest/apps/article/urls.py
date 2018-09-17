from django.contrib import admin
from django.urls import include
from django.urls import path
from django.urls import re_path

from article import views
urlpatterns = [
    path('artbd_article/<int:id>/change/',views.article),
    path('artbd_auction_result/<int:id>/change/',views.AuctionDetail.as_view()),
    path("",views.index),

    path('api/<int:id>', views.api),

    #http://127.0.0.1:8000/admin/article/artbd_article/37718/change/
]