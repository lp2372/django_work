
from django.contrib import admin
from django.urls import path

from artBD.apps.article import views
from artBD.apps.article import bigdataGen
from artBD.apps.article import bigdataGen

urlpatterns = [
    path('artbd_article/<int:id>/change/', views.article),
    path('artbd_auction_result/<int:id>/change/', views.auction_detail),
    path('article/keyword/', views.ArticleKeyword.as_view()),
    path('auction/keyword/', views.AuctionKeyword.as_view()),
    path("",views.index),
    path("article/list/",views.ArticleListAPIview.as_view()),
    path("push/",views.ArticlePushAPIView.as_view()),
    path('api/<int:id>/', views.api),
    path('bigdatagen/keyword/<int:topic_id>', bigdataGen.keyword),

    #http://127.0.0.1:8000/admin/article/artbd_article/37718/change/
]
