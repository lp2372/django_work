import json

import re
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.template import loader
from django.views import View

import jieba
import jieba.analyse

from artBD.apps.article.models import ArtBD_domain,ArtBD_article, ArtBD_auction_result, ArtBD_Article_Keyword, \
    ArtBD_Auction_Result_Keyword

def index(request):
    return redirect("/admin")

def keyword(request, topic_id):
    articles = ArtBD_article.objects.filter(topic_id=topic_id)
    for article in articles:
        id = article.id
        content = article.content

        tags = jieba.analyse.extract_tags(content, topK=20, withWeight=True, allowPOS=('n','nr','ns'))
        for tag in tags:
            ArtBD_Article_Keyword.objects.create(article_id=id,name=tag[0],weight=int(float(tag[1])*1000))

    return HttpResponse(len(articles))
