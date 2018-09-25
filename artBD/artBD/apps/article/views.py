import json
import re
from datetime import datetime
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.template import loader
from django.views import View

from artBD.apps.article.models import ArtBD_domain,ArtBD_article, ArtBD_auction_result, ArtBD_Article_Keyword, \
    ArtBD_Auction_Result_Keyword


def index(request):
    return redirect("/admin")


def article(request,id):
    obj = ArtBD_article.objects.get(id =id)
    context = obj.content
    title = obj.title
    title = title
    descrip = obj.descrip
    descrip = descrip
    time = obj.addtime
    url = obj.url
    content = {'url':url,'title':title,'descrip':descrip,'time':time,'context': context,"id":id}

    # 获取模板对象
    # template = loader.get_template('index.html')  # type:
    # template = loader.get_template('artron.html')  # type:
    #
    # # 渲染得到字符串
    # html_str = template.render(content,title,descrip)


    # 响应请求
    return render(request, 'artron.html', content)



def auction_detail(request,id):
    """显示艺术作品详情"""
    obj = ArtBD_auction_result.objects.get(id=id)
    title = obj.title
    author = obj.author
    keyword = obj.keyword
    descrip = obj.descrip
    material = obj.material
    size = obj.size
    final_price = obj.final_price
    url = obj.url
    if final_price == 0 or final_price is None:
        final_price = '--'
    else:
        final_price = 'RMB ' + str(final_price)
    refer_price1 = obj.refer_price1
    refer_price2 = obj.refer_price2
    refer_price = 'RMB ' + str(refer_price1) + "-" + str(refer_price2)
    addtime = obj.addtime
    md5_url = obj.md5_url
    topic_id = obj.topic.id
    domain = obj.topic.domain.domain

    thumb_img = "/imgs/" + domain + "/" + str(topic_id) + "/" + md5_url + "/thumb.jpg"

    if addtime is None:
        addtime = '未知'


    content = {'url':url,'title':title,'author':author,'keyword':keyword,'descrip':descrip,'addtime':addtime,
               'material':material,'size':size,'refer_price':refer_price,'final_price':final_price,
               'thumb_img':thumb_img,'id':id}
    return render(request, 'auctionDetail.html', content)

def api(request,id):
    if id == 1:
        data = {'国画': 21300, 
                '书法': 12333,
                '油画': 8982,
                '版画': 3090,
                '当代水墨': 2980,
                '古玩': 1000,
                }
    elif id == 2:
        data = {'李可染': 1300, 
                '黄永玉': 833,
                '范境': 382,
                '李一': 190,
                '孟庆占': 98,
                }
    elif id == 3:   # 网站热度百分比
        data = [ {'name':'雅昌网', 'value':33}, 
                 {'name':'嘉德拍卖', 'value':23},
                 {'name':'凤凰艺术', 'value':18},
                 {'name':'搜狐网', 'value':12},
                 {'name':'中国艺术网', 'value':7},
                 {'name':'环球艺术网', 'value':4},
                 {'name':'其它', 'value':3},
                ]
    elif id == 4:
        data = [ {'name':'北京','value': 1231}, 
                 {'name':'上海','value': 912},
                 {'name':'山东','value': 824},
                 {'name':'广东','value': 789},
                 {'name':'江苏','value': 756},
                 {'name':'浙江','value': 698},
                 {'name':'陕西','value': 624},
                 {'name':'云南','value': 576},
                 {'name':'湖北','value': 524},
                 {'name':'河南','value': 502},
                 {'name':'湖南','value': 478},
                 {'name':'安徽','value': 312},
                ]
    elif id == 7:
        data = {'time': ['四月', '五月', '六月', '七月', '八月', '九月'],
                'beian': [213, 324, 531, 612, 1215, 2121],
                'bidui': [12, 23, 55, 121, 211, 321],
                'chaxun': [2123, 2321, 3112, 3453, 4556, 5121],
                }
    elif id == 5:
        articles = ArtBD_article.objects.filter(status=2).order_by('-create_time')
        data = []
        for article in articles:
            title = article.title.strip()
            author= article.author
            keyword= article.keyword
            descrip= article.descrip.strip()
            url= article.url
            # "/imgs/artron.net/4/96a25c8a786c6847710abb167f51877/thumb.jpg",
            topic_id = article.topic.id
            domain = article.topic.domain.domain
            md5_url = article.md5_url
            # print(topic_id,domain,md5_url)
            thumb_img = article.thumb_img
            if article.addtime is None:
                addtime = ''
            else:
                addtime = article.addtime

            item = {'id': article.id,
                    'title': title,
                    'author': author,
                    'keyword': keyword,
                    'descrip': descrip,
                    'url': url,
                    'addtime': addtime,
                    'thumb_img': thumb_img,
                    }
            data.append(item)
    elif id == 6:
        category = request.GET.get('category')
        page = int(request.GET.get('page', '1'))
        kw = request.GET.get('kw')
        article_item_list = []
        auction_item_list = []
        article_total_page = '--'
        auction_total_page = '--'
        #文章
        article_obj_list = ArtBD_article.objects.filter(title__contains=kw)
        article_paginator = Paginator(article_obj_list, 10)  # Show 25 contacts per page
        article_total_page = article_paginator.num_pages
        article_count = article_paginator.count
        #作品
        auction_obj_list = ArtBD_auction_result.objects.filter(Q(title__contains=kw) | Q(author__contains=kw))
        auction_paginator = Paginator(auction_obj_list, 10)
        auction_total_page = auction_paginator.num_pages
        auction_count = auction_paginator.count

        if category == '文章':
            try:
                article_pagnation = article_paginator.page(page)
            except PageNotAnInteger:
                article_pagnation = article_paginator.page(1)
            except EmptyPage:
                article_pagnation = article_paginator.page(article_total_page)

            for article_obj in article_pagnation:
                dict_data = {}
                dict_data['title'] = article_obj.title.replace("'", "").strip()
                dict_data['category'] = article_obj.topic.name
                dict_data['descrip'] = article_obj.descrip.replace(")", '').replace("(", '').replace("'", '').strip()
                dict_data['pageviews'] = article_obj.pageviews
                dict_data['comments'] = article_obj.comments
                dict_data['link'] = article_obj.url.replace("'", "")
                dict_data['source'] = article_obj.topic.domain.name

                article_item_list.append(dict_data)

            auction_pagnation = auction_paginator.page(1)
            for auction_obj in auction_pagnation:
                data = {}
                data["title"] = auction_obj.title
                data["author"] = auction_obj.author
                data["keyword"] = auction_obj.keyword
                data["material"] = auction_obj.material
                data["size"] = auction_obj.size
                data["addtime"] = auction_obj.addtime
                data["finalprice"] = auction_obj.final_price
                if data["finalprice"] == 0 or data["finalprice"] is None:
                    data["finalprice"] = '--'
                if auction_obj.refer_price1 == 0 or auction_obj.refer_price1 is None:
                    data["refer_price"] = '--'
                else:
                    data["refer_price"] = str(auction_obj.refer_price1) + "-" + str(auction_obj.refer_price2)
                data["pageviews"] = auction_obj.pageviews
                data["comments"] = auction_obj.comments
                data["link"] = auction_obj.url
                data["source"] = auction_obj.topic.domain.name
                auction_item_list.append(data)
        elif category == '作品':

            try:
                auction_pagnation = auction_paginator.page(page)
            except PageNotAnInteger:
                auction_pagnation = auction_paginator.page(1)
            except EmptyPage:
                auction_pagnation = auction_paginator.page(auction_total_page)

            for auction_obj in auction_pagnation:
                data = {}
                data["title"] = auction_obj.title
                data["author"] = auction_obj.author
                data["keyword"] = auction_obj.keyword
                data["material"] = auction_obj.material
                data["size"] = auction_obj.size
                data["addtime"] = auction_obj.addtime
                data["finalprice"] = auction_obj.final_price
                if data["finalprice"] == 0 or data["finalprice"] is None:
                    data["finalprice"] = '--'
                if auction_obj.refer_price1 == 0 or auction_obj.refer_price1 is None:
                    data["refer_price"] = '--'
                else:
                    data["refer_price"] = str(auction_obj.refer_price1) + "-" + str(auction_obj.refer_price2)
                data["pageviews"] = auction_obj.pageviews
                data["comments"] = auction_obj.comments
                data["link"] = auction_obj.url
                data["source"] = auction_obj.topic.domain.name
                auction_item_list.append(data)

            article_pagnation = article_paginator.page(1)
            for article_obj in article_pagnation:
                dict_data = {}
                dict_data['title'] = article_obj.title.replace("'", "").strip()
                dict_data['category'] = article_obj.topic.name
                dict_data['descrip'] = article_obj.descrip.replace(")", '').replace("(", '').replace("'", '').strip()
                dict_data['pageviews'] = article_obj.pageviews
                dict_data['comments'] = article_obj.comments
                dict_data['link'] = article_obj.url.replace("'", "")
                dict_data['source'] = article_obj.topic.domain.name

                article_item_list.append(dict_data)

        elif category is None:
            article_pagnation = article_paginator.page(1)
            for article_obj in article_pagnation:
                dict_data = {}
                dict_data['title'] = article_obj.title.replace("'", "").strip()
                dict_data['category'] = article_obj.topic.name
                dict_data['descrip'] = article_obj.descrip.replace(")", '').replace("(", '').replace("'", '').strip()
                dict_data['pageviews'] = article_obj.pageviews
                dict_data['comments'] = article_obj.comments
                dict_data['link'] = article_obj.url.replace("'", "")
                dict_data['source'] = article_obj.topic.domain.name

                article_item_list.append(dict_data)
            auction_pagnation = auction_paginator.page(1)
            for auction_obj in auction_pagnation:
                data = {}
                data["title"] = auction_obj.title
                data["author"] = auction_obj.author
                data["keyword"] = auction_obj.keyword
                data["material"] = auction_obj.material
                data["size"] = auction_obj.size
                data["addtime"] = auction_obj.addtime
                data["finalprice"] = auction_obj.final_price
                if data["finalprice"] == 0 or data["finalprice"] is None:
                    data["finalprice"] = '--'
                if auction_obj.refer_price1 == 0 or auction_obj.refer_price1 is None:
                    data["refer_price"] = '--'
                else:
                    data["refer_price"] = str(auction_obj.refer_price1) + "-" + str(auction_obj.refer_price2)
                data["pageviews"] = auction_obj.pageviews
                data["comments"] = auction_obj.comments
                data["link"] = auction_obj.url
                data["source"] = auction_obj.topic.domain.name
                auction_item_list.append(data)



        page_info = {'current_page': page, 'article_total_page': article_total_page,
                     'auction_total_page': auction_total_page,'article_count':article_count,'auction_count':auction_count,"page_size": 10}
        outputHead = {
            "resultMessage": "成功"
        }
        data = {
            'outputHead': outputHead, 'outputdata': {'page_info': page_info,
                                                     'all_items': {'auction_item_list': auction_item_list,
                                                                   'article_item_list': article_item_list}}
        }
    else:
        data = {}

    response = HttpResponse(json.dumps(data), content_type="application/json")
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "*"
    return response

class ArticleKeyword(View):
    """增加以及显示文章关键字词"""
    def post(self,request):
        """增加文章关键字"""
        id = request.POST.get("id") # 文章ｉｄ
        keyword = request.POST.get("keyword")
        keyword_list = re.findall("[\u4e00-\u9fa5]+",keyword)

        # print(keyword_list)

        for keyword in keyword_list:
            try:

                keyword_obj = ArtBD_Article_Keyword.objects.get(article=id, name=keyword)
            except:
                #发生异常说明关键字不存在
                obj = ArtBD_article.objects.get(id =id)
                ArtBD_Article_Keyword.objects.create(name=keyword,article =obj)



        return JsonResponse({'success': 'ok'})


    def get(self,request):
        """显示文章关键字"""
        id = request.GET.get("id")
        article_obj = ArtBD_article.objects.get(id=id)
        keyword_obj = article_obj.artbd_article_keyword_set.all()
        keyword_list = []
        for obj in keyword_obj:
            keyword_list.append(obj.name)

        return JsonResponse(keyword_list,safe=False)


class AuctionKeyword(View):
    """增加以及显示艺术作品关键字词"""

    def post(self, request):
        """增加文章关键字"""
        id = request.POST.get("id")  # 作品ｉｄ
        keyword = request.POST.get("keyword")
        keyword_list = re.findall("[\u4e00-\u9fa5]+", keyword)

        print(keyword_list)

        for keyword in keyword_list:
            try:

                keyword_obj = ArtBD_Auction_Result_Keyword.objects.get(auction_result=id, name=keyword)
            except:
                # 发生异常说明关键字不存在
                obj = ArtBD_auction_result.objects.get(id=id)
                ArtBD_Auction_Result_Keyword.objects.create(name=keyword, auction_result=obj)

        return JsonResponse({'success': 'ok'})

    def get(self, request):
        """显示文章关键字"""
        id = request.GET.get("id")
        auction_result_obj = ArtBD_auction_result.objects.get(id=id)
        keyword_obj = auction_result_obj.artbd_auction_result_keyword_set.all()
        keyword_list = []
        for obj in keyword_obj:
            keyword_list.append(obj.name)

        return JsonResponse(keyword_list, safe=False)
class ArticleListAPIview(View):
    """显示文章作品列表"""
    def get(self,request):
        category = request.GET.get('category')
        page = int(request.GET.get('page','1'))
        kw = request.GET.get('kw')
        article_item_list = []
        auction_item_list = []
        article_total_page = '--'
        auction_total_page = '--'

        if category == '文章' or category is None:
            article_obj_list = ArtBD_article.objects.filter(title__contains=kw)

            article_paginator = Paginator(article_obj_list, 10)  # Show 25 contacts per page
            article_total_page = article_paginator.num_pages
            try:
                article_pagnation = article_paginator.page(page)
            except PageNotAnInteger:
                article_pagnation = article_paginator.page(1)
            except EmptyPage:
                article_pagnation = article_paginator.page(article_total_page)

            for article_obj in article_pagnation:
                dict_data = {}
                dict_data['title'] = article_obj.title.replace("'", "").strip()
                dict_data['category'] = article_obj.topic.name
                dict_data['descrip'] = article_obj.descrip.replace(")",'').replace("(",'').replace("'",'').strip()
                dict_data['pageviews'] = article_obj.pageviews
                dict_data['comments'] = article_obj.comments
                dict_data['link'] = article_obj.url.replace("'","")
                dict_data['source'] = article_obj.topic.domain.name

                article_item_list.append(dict_data)
        if category == '作品' or category is None :
            auction_obj_list = ArtBD_auction_result.objects.filter(Q(title__contains=kw) | Q(author__contains=kw))
            auction_paginator = Paginator(auction_obj_list, 10)
            auction_total_page = auction_paginator.num_pages
            try:
                auction_pagnation = auction_paginator.page(page)
            except PageNotAnInteger:
                auction_pagnation = auction_paginator.page(1)
            except EmptyPage:
                auction_pagnation = auction_paginator.page(auction_total_page)


            for auction_obj in auction_pagnation:
                data = {}
                data["title"] = auction_obj.title
                data["author"] = auction_obj.author
                data["keyword"] = auction_obj.keyword
                data["material"] = auction_obj.material
                data["size"] = auction_obj.size
                data["addtime"] = auction_obj.addtime
                data["finalprice"] = auction_obj.final_price
                if data["finalprice"] == 0 or data["finalprice"] is None:
                    data["finalprice"] = '--'
                if auction_obj.refer_price1 == 0 or auction_obj.refer_price1 is None:
                    data["refer_price"] = '--'
                else:
                    data["refer_price"] =  str(auction_obj.refer_price1) + "-" + str(auction_obj.refer_price2)
                data["pageviews"] = auction_obj.pageviews
                data["comments"] = auction_obj.comments
                data["link"] = auction_obj.url
                data["source"] = auction_obj.topic.domain.name
                auction_item_list.append(data)

        page_info = {'current_page':page,'article_total_page':article_total_page,'auction_total_page':auction_total_page,"page_size":10}
        outputHead={
            "resultMessage": "成功"
        }
        output_data = {
            'outputHead':outputHead,'outputdata':{'page_info':page_info,'all_items':{'auction_item_list':auction_item_list,'article_item_list':article_item_list}}
        }

        response = HttpResponse(json.dumps(output_data), content_type="application/json")
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
        response["Access-Control-Max-Age"] = "1000"
        response["Access-Control-Allow-Headers"] = "*"
        return response

class ArticlePushAPIView(View):
    """文章推送
    """
    def get(self,request):
        id = request.GET.get('id')
        obj = ArtBD_article.objects.get(id = id)
        obj.status = 2
        obj.create_time = datetime.now()
        obj.save()
        return JsonResponse({'success': 'ok'})
