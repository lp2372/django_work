from django.contrib import admin
from article.models import ArtBD_domain,ArtBD_auction_result,ArtBD_topic,ArtBD_article
# Register your models here.

#关联对象
class DomainSubInline(admin.TabularInline):
    model = ArtBD_topic
    extra = 5 #默认显示条目的数量

@admin.register(ArtBD_domain)
class DomainAdmin(admin.ModelAdmin):
    list_display = ['name','domain']  #设置要显示在列表中的字段
    list_per_page = 10
    # 显示顶部操作栏
    actions_on_top = True
    # 显示底部操作栏
    actions_on_bottom = True
    inlines = [DomainSubInline] # 关联对象
    search_fields = ['name','domain']
    readonly_fields = ('name','domain','status','ordernum')  # 只读
    exclude = ['status','ordernum']     # 不显示
    fields = ['name','domain']


class TopicSubInline(admin.TabularInline):
    model = [ArtBD_article]
    extra = 5  # 默认显示条目的数量
@admin.register(ArtBD_topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ['name','url','domain']
    list_per_page = 10
    # inlines = [TopicSubInline]
    readonly_fields = ['name','url','ordernum']
    exclude = ['status', 'ordernum']
    search_fields = ['name','url']
    # fk_fields 设置显示外键字段
    fk_fields = ('domain',)
    # fields = ['name','url']

@admin.register(ArtBD_auction_result)
class AuctionResultAdmin(admin.ModelAdmin):


    # 显示顶部操作栏
    actions_on_top = True
    # 显示底部操作栏
    actions_on_bottom = True
    list_display = ['title','author','keyword','material','size','final_price','refer_price1','refer_price2','pageviews','comments']
    list_per_page = 10
    search_fields = ['title', 'author', 'keyword', 'final_price']



@admin.register(ArtBD_article)
class ArticleAdmin(admin.ModelAdmin):

    # 显示顶部操作栏
    actions_on_top = True
    # 显示底部操作栏
    actions_on_bottom = True
    list_display = ['title','author','descrip','addtime','pageviews','comments','url']
    list_per_page = 10
    search_fields = ['title','author','descrip','addtime','pageviews','comments']

admin.site.site_title = '亚特网'
admin.site.site_header = '亚特网'
admin.site.index_title = '亚特网后台管理系统'
# admin.site.register(ArtBD_domain,DomainAdmin)
# admin.site.register(ArtBD_auction_result)
# admin.site.register(ArtBD_topic,TopicAdmin)
# admin.site.register(ArtBD_article)