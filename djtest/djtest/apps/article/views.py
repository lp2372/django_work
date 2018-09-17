import json

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import loader

from djtest.apps.article.models import ArtBD_domain,ArtBD_article, ArtBD_auction_result


def index(request):
    return redirect("/admin")

def test(request):
    context = {'name': 'django'}
    # 参数1：请求对象
    # 参数2：模块路径
    # 参数3：字典数据

    obj = ArtBD_article.objects.get(id=1)
    content = obj.content.replace("'","")

    content = {'name':content}

    # 获取模板对象
    template = loader.get_template('index.html')  # type:
    print(template)
    # 渲染得到字符串
    html_str = template.render(content)
    print(html_str)
    # 响应请求
    return HttpResponse(html_str)

def article(request,id):
    obj = ArtBD_article.objects.get(id =id)
    context = obj.content.replace("'", "")
    title = obj.title
    title = title.replace("'", "").strip()
    descrip = obj.descrip
    descrip = descrip.replace(")",'').replace("(",'').replace("'",'').strip()
    time = obj.addtime

    content = {'title':title,'descrip':descrip,'time':time,'context': context}

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
               'thumb_img':thumb_img}
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
    elif id == 3:
        data = {'errorcode': id, 'detail': 'Get success'}
    else:
        data = {}

    response = HttpResponse(json.dumps(data), content_type="application/json")
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "*"

    return response
