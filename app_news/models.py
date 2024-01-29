from django.contrib.auth import get_user_model
from django.db import models


class News(models.Model):
    news_title = models.CharField(max_length=255, blank=True, null=True)
    news_title_uz = models.CharField(max_length=255, verbose_name="title_uz")
    news_title_en = models.CharField(max_length=255, verbose_name="title_en", blank=True, null=True)
    news_title_ru = models.CharField(max_length=255, verbose_name='title_ru', blank=True, null=True)

    news_desc = models.CharField(max_length=500, blank=True, null=True)
    news_desc_uz = models.CharField(max_length=500, verbose_name="News_desc_uz", blank=True, null=True)
    news_desc_en = models.CharField(max_length=500, verbose_name="News_desc_en", blank=True, null=True)
    news_desc_ru = models.CharField(max_length=500, verbose_name="News_desc_ru", blank=True, null=True)

    news_image = models.ImageField(upload_to='news/', verbose_name="News's image", blank=True, null=True)

    news_text = models.TextField(blank=True, null=True)
    news_text_uz = models.TextField(verbose_name="Yangilikning toliq matni")
    news_text_en = models.TextField(verbose_name="Yangilikningn inglizcha matni", blank=True, null=True)
    news_text_ru = models.TextField(verbose_name="Yangilikning ruscha matni", blank=True, null=True)

    news_datetime = models.DateTimeField(auto_now_add=True)
    news_views_count = models.IntegerField(verbose_name="views_count", default=0)
    news_source = models.URLField(verbose_name="Manba(agar mavjud bolsa)", blank=True, null=True)
    news_author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, default=5)

    class Meta:
        db_table = 'news'
        ordering = ('-news_datetime',)

    def __str__(self):
        return f"{self.id} {self.news_title_uz}"
