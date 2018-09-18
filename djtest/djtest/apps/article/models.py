from django.db import models

# Create your models here.

class ArtBD_domain(models.Model):
    name = models.CharField(max_length=100,null=False,verbose_name='网站')
    domain = models.CharField(max_length=100,null=False,verbose_name='域名')
    ordernum = models.IntegerField(default='100')
    status = models.IntegerField(default='0',verbose_name='状态')

    class Meta:
        # 指定表名
        db_table = 'artBD_domain'
        verbose_name = '域名'
        verbose_name_plural = verbose_name

class ArtBD_topic(models.Model):
    name = models.CharField(max_length=100, null=False,verbose_name="栏目")
    url = models.CharField(max_length=100, null=False,verbose_name='链接')
    ordernum = models.SmallIntegerField(default='10')
    status = models.IntegerField(default='0',verbose_name='状态')
    domain = models.ForeignKey('ArtBD_domain',on_delete=models.CASCADE,verbose_name='域名') # 默认级联删除

    class Meta:
        # 指定表名
        db_table = 'artBD_topic'
        verbose_name = '专栏'
        verbose_name_plural = verbose_name

class ArtBD_article(models.Model):
    spider_name = models.CharField(max_length=100,null=True,verbose_name='爬虫名')
    module = models.CharField(max_length=100,null=True)
    md5_url = models.CharField(max_length=100,null=True)
    url = models.CharField(max_length=100,null=True,verbose_name='链接')
    thumb_img = models.CharField(max_length=100,null=True)
    addtime = models.DateTimeField(null=True,verbose_name='发布时间')
    title = models.CharField(max_length=100,null=True,verbose_name='标题')
    author = models.CharField(max_length=100,null=True,verbose_name='作者')
    keyword = models.CharField(max_length=100,null=True)
    descrip = models.CharField(max_length=1024,null=True,verbose_name='摘要')
    content = models.TextField(null=True,verbose_name='内容')
    status = models.SmallIntegerField(default='0',verbose_name='状态')
    create_time = models.DateTimeField(auto_now_add = True,verbose_name='添加时间')
    pageviews = models.IntegerField(default='0',verbose_name='点击量')
    comments = models.IntegerField(default='0',verbose_name='评论量')
    topic = models.ForeignKey('ArtBD_topic',on_delete=models.CASCADE,verbose_name='专栏')

    class Meta:
        # 指定表名
        db_table = 'artBD_article'
        verbose_name = '艺术文章'
        verbose_name_plural = verbose_name

class ArtBD_auction_result(models.Model):
    spider_name = models.CharField(max_length=100, null=True,verbose_name='爬虫名')
    module = models.CharField(max_length=100, null=True)
    md5_url = models.CharField(max_length=100, null=True)
    url = models.CharField(max_length=100, null=True,verbose_name='链接')
    thumb_img = models.CharField(max_length=100, null=True)
    addtime = models.DateTimeField(null=True,verbose_name='发布时间')
    title = models.CharField(max_length=100, null=True,verbose_name='标题')
    author = models.CharField(max_length=100, null=True,verbose_name='作者')
    keyword = models.CharField(max_length=100, null=True,verbose_name='分类')
    descrip = models.CharField(max_length=1024, null=True,verbose_name='摘要')
    content = models.TextField(null=True,verbose_name='内容')
    status = models.SmallIntegerField(default='0',verbose_name='状态')
    create_time = models.DateTimeField(auto_now_add=True,verbose_name='添加时间')
    pageviews = models.IntegerField(default='0',verbose_name='点击量')
    comments = models.IntegerField(default='0',verbose_name='评论量')
    topic = models.ForeignKey('ArtBD_topic', on_delete=models.CASCADE,verbose_name='专栏')
    material = models.CharField(max_length=100,null=True,verbose_name='材质')
    size = models.CharField(max_length=100,null=True,verbose_name='尺寸')
    final_price = models.IntegerField(null=True,verbose_name='成交价(RMB)')
    refer_price1 = models.IntegerField(null=True,verbose_name='参考最低价(RMB)')
    refer_price2 = models.IntegerField(null=True,verbose_name='参考最高价(RMB)')

    class Meta:
        # 指定表名
        db_table = 'artBD_auction_result'
        verbose_name = '艺术作品'
        verbose_name_plural = verbose_name


class ArtBD_Keyword(models.Model):
    name = models.CharField(max_length=32,null= False)
    weight = models.SmallIntegerField(null=False,default='1')
    status = models.SmallIntegerField(null=False,default='0')

    class Meta:
        db_table = 'artBD_keyword'

class ArtBD_Article_Keyword(models.Model):

    name = models.CharField(max_length=32)
    times = models.SmallIntegerField(null=False,default='1')
    article = models.ForeignKey('ArtBD_article',on_delete=models.CASCADE)

    class Meta:
        db_table = 'artBD_article_keyword'

#  CREATE TABLE `artBD_article_keyword` (
#   `id` bigint(20) NOT NULL AUTO_INCREMENT,
#   `article_id` bigint(20) NOT NULL,
#   `name` varchar(32) NOT NULL,
#   `times` smallint(6) NOT NULL DEFAULT '1',
#   PRIMARY KEY (`id`),
#   KEY `article_id` (`article_id`)
# ) ENGINE=MyISAM DEFAULT CHARSET=utf8




