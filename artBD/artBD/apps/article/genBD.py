import json

import re
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
    context = obj.content.replace("'", "")
    title = obj.title
    title = title.replace("'", "").strip()
    descrip = obj.descrip
    descrip = descrip.replace(")",'').replace("(",'').replace("'",'').strip()
    time = obj.addtime

    content = {'title':title,'descrip':descrip,'time':time,'context': context,"id":id}

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
    else:
        addtime = addtime.strftime("%Y") + '年'

    content = {'title':title,'author':author,'keyword':keyword,'descrip':descrip,'addtime':addtime,
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
    elif id == 5:
        articles = ArtBD_article.objects.filter(status=2)
        data = []
        for article in articles:
            title = article.title[1:-1]
            author= article.author[1:-1]
            keyword= article.keyword[1:-1]
            descrip= article.descrip[2:-2]
            url= article.url[1:-1]

            if article.addtime is None:
                addtime = ''
            else:
                addtime = article.addtime.strftime("%Y-%m-%d")

            item = {'id': article.id,
                    'title': title,
                    'author': author,
                    'keyword': keyword,
                    'descrip': descrip,
                    'url': url,
                    'addtime': addtime,
                    'thumb_img': article.thumb_img,
                    }
            data.append(item)
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
